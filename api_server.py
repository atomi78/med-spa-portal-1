"""
REST API Server for Voice AI Integration
Wraps the FastMCP server tools as HTTP endpoints for voice AI platforms like Vapi.ai
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Import functions from server.py
sys.path.append(str(Path(__file__).parent))
from server import (
    load_data, save_data,
    APPOINTMENTS_FILE, CLIENTS_FILE, SERVICES_FILE, STAFF_FILE,
    initialize_default_data
)

app = FastAPI(title="Miami Med Spa Voice AI API", version="1.0.0")

# Enable CORS for voice AI platforms
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data
initialize_default_data()

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ServiceResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    duration_minutes: int
    description: str

class StaffResponse(BaseModel):
    id: str
    name: str
    role: str
    specialties: List[str]

class TimeSlot(BaseModel):
    time: str
    staff_id: str
    staff_name: str

class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[TimeSlot]

class BookingRequest(BaseModel):
    service_name: str
    date: str
    time: str
    client_name: str
    client_phone: str
    client_email: Optional[str] = ""
    staff_id: Optional[str] = None

class BookingResponse(BaseModel):
    success: bool
    appointment_id: Optional[str] = None
    message: str
    confirmation_details: Optional[dict] = None

# ============================================================================
# VOICE AI ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Miami Med Spa Voice AI API",
        "version": "1.0.0"
    }

@app.get("/services", response_model=List[ServiceResponse])
def get_services(category: Optional[str] = None):
    """
    Get list of available services for voice AI to read to caller.
    Optionally filter by category.
    """
    services = load_data(SERVICES_FILE)

    service_list = list(services.values())

    if category:
        service_list = [s for s in service_list if s['category'].lower() == category.lower()]

    return service_list

@app.get("/services/search")
def search_service(query: str):
    """
    Search for a service by name (fuzzy matching).
    Used when client says "I want Botox" or "facial"
    """
    services = load_data(SERVICES_FILE)
    query_lower = query.lower()

    # Try exact match first
    for service in services.values():
        if query_lower in service['name'].lower():
            return {
                "found": True,
                "service": service
            }

    # Try category match
    for service in services.values():
        if query_lower in service['category'].lower():
            return {
                "found": True,
                "service": service,
                "note": "Found by category"
            }

    return {
        "found": False,
        "message": f"No service found matching '{query}'"
    }

@app.get("/availability/{date}")
def check_availability(date: str, service_id: Optional[str] = None):
    """
    Check availability for a specific date.
    Returns available time slots with staff information.

    Format: YYYY-MM-DD
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    services = load_data(SERVICES_FILE)
    staff = load_data(STAFF_FILE)
    appointments = load_data(APPOINTMENTS_FILE)

    # Get service duration if specified
    duration = 60  # default
    if service_id and service_id in services:
        duration = services[service_id]['duration_minutes']

    # Find available staff for this day
    available_staff = {sid: s for sid, s in staff.items()
                      if day_name in s['available_days']}

    # Generate time slots
    available_slots = []

    for staff_id, staff_member in available_staff.items():
        # Get existing appointments for this staff on this date
        staff_appointments = [a for a in appointments.values()
                            if a['staff_id'] == staff_id
                            and a['date'] == date
                            and a['status'] == 'scheduled']

        # Generate possible slots (every 30 minutes)
        start_hour, start_min = map(int, staff_member['hours']['start'].split(':'))
        end_hour, end_min = map(int, staff_member['hours']['end'].split(':'))

        current_time = datetime.strptime(f"{start_hour:02d}:{start_min:02d}", "%H:%M")
        end_time = datetime.strptime(f"{end_hour:02d}:{end_min:02d}", "%H:%M")

        while current_time < end_time:
            slot_time = current_time.strftime("%H:%M")

            # Check if slot is available (not overlapping with existing appointments)
            is_available = True
            for apt in staff_appointments:
                apt_start = datetime.strptime(apt['time'], "%H:%M")
                apt_end = apt_start + timedelta(minutes=apt['duration_minutes'])

                if apt_start <= current_time < apt_end:
                    is_available = False
                    break

            if is_available:
                available_slots.append({
                    "time": slot_time,
                    "staff_id": staff_id,
                    "staff_name": staff_member['name']
                })

            # Move to next 30-minute slot
            current_time += timedelta(minutes=30)

    return {
        "date": date,
        "day_of_week": day_name,
        "available_slots": available_slots[:10]  # Limit to first 10 slots
    }

@app.post("/book", response_model=BookingResponse)
def book_appointment(booking: BookingRequest):
    """
    Book an appointment from voice AI call.
    Creates client if new, then creates appointment.
    """
    try:
        clients = load_data(CLIENTS_FILE)
        services = load_data(SERVICES_FILE)
        staff = load_data(STAFF_FILE)
        appointments = load_data(APPOINTMENTS_FILE)

        # Find service by name
        service = None
        service_id = None
        for sid, svc in services.items():
            if booking.service_name.lower() in svc['name'].lower():
                service = svc
                service_id = sid
                break

        if not service:
            return BookingResponse(
                success=False,
                message=f"Service '{booking.service_name}' not found"
            )

        # Find or create client
        client_id = None
        for cid, client in clients.items():
            if client['phone'] == booking.client_phone:
                client_id = cid
                break

        if not client_id:
            # Create new client
            client_num = len(clients) + 1
            client_id = f"CL{client_num:04d}"

            clients[client_id] = {
                "id": client_id,
                "name": booking.client_name,
                "email": booking.client_email,
                "phone": booking.client_phone,
                "date_of_birth": "",
                "address": "",
                "emergency_contact": "",
                "medical_notes": "",
                "created_at": datetime.now().isoformat(),
                "total_visits": 0,
                "total_spent": 0.0
            }
            save_data(CLIENTS_FILE, clients)

        # Determine staff
        staff_id = booking.staff_id
        if not staff_id:
            # Find first available staff for this service
            for sid, s in staff.items():
                if service['category'] in s['specialties']:
                    staff_id = sid
                    break

        if not staff_id or staff_id not in staff:
            return BookingResponse(
                success=False,
                message="No staff available for this service"
            )

        # Create appointment
        apt_num = len(appointments) + 1
        apt_id = f"APT{apt_num:04d}"

        appointment = {
            "id": apt_id,
            "client_id": client_id,
            "client_name": clients[client_id]["name"],
            "service_id": service_id,
            "service_name": service["name"],
            "staff_id": staff_id,
            "staff_name": staff[staff_id]["name"],
            "date": booking.date,
            "time": booking.time,
            "duration_minutes": service["duration_minutes"],
            "price": service["price"],
            "status": "scheduled",
            "notes": "Booked via voice AI",
            "created_at": datetime.now().isoformat()
        }

        appointments[apt_id] = appointment
        save_data(APPOINTMENTS_FILE, appointments)

        # Update client stats
        clients[client_id]["total_visits"] += 1
        clients[client_id]["total_spent"] += service["price"]
        save_data(CLIENTS_FILE, clients)

        return BookingResponse(
            success=True,
            appointment_id=apt_id,
            message=f"Appointment booked successfully for {booking.client_name}",
            confirmation_details={
                "appointment_id": apt_id,
                "service": service["name"],
                "date": booking.date,
                "time": booking.time,
                "provider": staff[staff_id]["name"],
                "price": service["price"],
                "duration": service["duration_minutes"],
                "client_name": booking.client_name,
                "client_phone": booking.client_phone
            }
        )

    except Exception as e:
        return BookingResponse(
            success=False,
            message=f"Error booking appointment: {str(e)}"
        )

@app.get("/appointment/{appointment_id}")
def get_appointment(appointment_id: str):
    """Get appointment details"""
    appointments = load_data(APPOINTMENTS_FILE)

    if appointment_id not in appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointments[appointment_id]

@app.post("/appointment/{appointment_id}/cancel")
def cancel_appointment(appointment_id: str, reason: Optional[str] = "Cancelled via phone"):
    """Cancel an appointment"""
    appointments = load_data(APPOINTMENTS_FILE)

    if appointment_id not in appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointments[appointment_id]["status"] = "cancelled"
    appointments[appointment_id]["notes"] = reason
    appointments[appointment_id]["updated_at"] = datetime.now().isoformat()

    save_data(APPOINTMENTS_FILE, appointments)

    return {
        "success": True,
        "message": f"Appointment {appointment_id} cancelled",
        "appointment": appointments[appointment_id]
    }

@app.get("/staff/available")
def get_available_staff(specialty: Optional[str] = None):
    """Get list of staff, optionally filtered by specialty"""
    staff = load_data(STAFF_FILE)

    staff_list = list(staff.values())

    if specialty:
        staff_list = [s for s in staff_list if specialty in s['specialties']]

    return staff_list

# ============================================================================
# VOICE AI HELPER ENDPOINTS
# ============================================================================

@app.get("/voice/greeting")
def get_greeting():
    """Get greeting message for voice AI"""
    return {
        "message": "Thank you for calling Miami Med Spa. I'm your AI assistant and I can help you book treatments like Botox, dermal fillers, facials, laser hair removal, and more. What treatment are you interested in today?"
    }

@app.get("/voice/services-summary")
def get_services_summary():
    """Get a voice-friendly summary of services"""
    services = load_data(SERVICES_FILE)

    by_category = {}
    for service in services.values():
        cat = service['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(f"{service['name']} for ${service['price']}")

    summary = "We offer: "
    parts = []
    for category, items in by_category.items():
        parts.append(f"{category} including {', '.join(items)}")

    summary += "; ".join(parts)

    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
