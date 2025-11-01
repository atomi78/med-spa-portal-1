"""
FastMCP Server for Miami Med Spa Management
Provides tools for managing appointments, clients, services, and staff.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Miami Med Spa Portal")

# Data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Data files
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"
CLIENTS_FILE = DATA_DIR / "clients.json"
SERVICES_FILE = DATA_DIR / "services.json"
STAFF_FILE = DATA_DIR / "staff.json"


# Helper functions for data persistence
def load_data(file_path: Path) -> dict:
    """Load data from JSON file."""
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}


def save_data(file_path: Path, data: dict) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def initialize_default_data():
    """Initialize default services and staff if not exists."""
    # Default services
    if not SERVICES_FILE.exists():
        default_services = {
            "SVC001": {
                "id": "SVC001",
                "name": "Botox Treatment",
                "category": "Injectables",
                "duration_minutes": 30,
                "price": 400.00,
                "description": "Wrinkle reduction with Botox injections"
            },
            "SVC002": {
                "id": "SVC002",
                "name": "Dermal Fillers",
                "category": "Injectables",
                "duration_minutes": 45,
                "price": 650.00,
                "description": "Volume restoration with hyaluronic acid fillers"
            },
            "SVC003": {
                "id": "SVC003",
                "name": "Hydrafacial",
                "category": "Facials",
                "duration_minutes": 60,
                "price": 250.00,
                "description": "Deep cleansing and hydration facial treatment"
            },
            "SVC004": {
                "id": "SVC004",
                "name": "Laser Hair Removal",
                "category": "Laser Treatments",
                "duration_minutes": 30,
                "price": 300.00,
                "description": "Permanent hair reduction using laser technology"
            },
            "SVC005": {
                "id": "SVC005",
                "name": "Chemical Peel",
                "category": "Skin Treatments",
                "duration_minutes": 45,
                "price": 200.00,
                "description": "Skin resurfacing treatment for improved texture and tone"
            },
            "SVC006": {
                "id": "SVC006",
                "name": "Microneedling",
                "category": "Skin Treatments",
                "duration_minutes": 60,
                "price": 350.00,
                "description": "Collagen induction therapy for skin rejuvenation"
            },
            "SVC007": {
                "id": "SVC007",
                "name": "CoolSculpting",
                "category": "Body Contouring",
                "duration_minutes": 90,
                "price": 800.00,
                "description": "Non-invasive fat reduction treatment"
            }
        }
        save_data(SERVICES_FILE, default_services)

    # Default staff
    if not STAFF_FILE.exists():
        default_staff = {
            "STF001": {
                "id": "STF001",
                "name": "Dr. Maria Rodriguez",
                "role": "Medical Director",
                "specialties": ["Injectables", "Laser Treatments"],
                "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "hours": {"start": "09:00", "end": "17:00"}
            },
            "STF002": {
                "id": "STF002",
                "name": "Sarah Johnson",
                "role": "Licensed Aesthetician",
                "specialties": ["Facials", "Skin Treatments"],
                "available_days": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "hours": {"start": "10:00", "end": "18:00"}
            },
            "STF003": {
                "id": "STF003",
                "name": "Jennifer Martinez",
                "role": "Nurse Practitioner",
                "specialties": ["Injectables", "Body Contouring"],
                "available_days": ["Monday", "Wednesday", "Friday", "Saturday"],
                "hours": {"start": "09:00", "end": "17:00"}
            }
        }
        save_data(STAFF_FILE, default_staff)


# Initialize default data on server start
initialize_default_data()


# ============================================================================
# APPOINTMENT MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def create_appointment(
    client_id: str,
    service_id: str,
    staff_id: str,
    date: str,
    time: str,
    notes: Optional[str] = ""
) -> str:
    """
    Create a new appointment for a client.

    Args:
        client_id: Client ID (e.g., 'CL001')
        service_id: Service ID (e.g., 'SVC001')
        staff_id: Staff member ID (e.g., 'STF001')
        date: Appointment date in YYYY-MM-DD format
        time: Appointment time in HH:MM format (24-hour)
        notes: Optional notes for the appointment

    Returns:
        Confirmation message with appointment ID
    """
    appointments = load_data(APPOINTMENTS_FILE)
    clients = load_data(CLIENTS_FILE)
    services = load_data(SERVICES_FILE)
    staff = load_data(STAFF_FILE)

    # Validate client, service, and staff exist
    if client_id not in clients:
        return f"Error: Client {client_id} not found"
    if service_id not in services:
        return f"Error: Service {service_id} not found"
    if staff_id not in staff:
        return f"Error: Staff member {staff_id} not found"

    # Generate new appointment ID
    apt_num = len(appointments) + 1
    apt_id = f"APT{apt_num:04d}"

    # Create appointment
    appointment = {
        "id": apt_id,
        "client_id": client_id,
        "client_name": clients[client_id]["name"],
        "service_id": service_id,
        "service_name": services[service_id]["name"],
        "staff_id": staff_id,
        "staff_name": staff[staff_id]["name"],
        "date": date,
        "time": time,
        "duration_minutes": services[service_id]["duration_minutes"],
        "price": services[service_id]["price"],
        "status": "scheduled",
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }

    appointments[apt_id] = appointment
    save_data(APPOINTMENTS_FILE, appointments)

    return f"✓ Appointment created successfully!\n\nID: {apt_id}\nClient: {clients[client_id]['name']}\nService: {services[service_id]['name']}\nProvider: {staff[staff_id]['name']}\nDate: {date} at {time}\nDuration: {services[service_id]['duration_minutes']} minutes\nPrice: ${services[service_id]['price']:.2f}"


@mcp.tool()
def list_appointments(
    date: Optional[str] = None,
    client_id: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    List appointments with optional filters.

    Args:
        date: Filter by date (YYYY-MM-DD format). If not provided, shows all dates
        client_id: Filter by client ID
        status: Filter by status (scheduled, completed, cancelled, no-show)

    Returns:
        Formatted list of appointments
    """
    appointments = load_data(APPOINTMENTS_FILE)

    if not appointments:
        return "No appointments found."

    # Filter appointments
    filtered = appointments.values()

    if date:
        filtered = [a for a in filtered if a["date"] == date]
    if client_id:
        filtered = [a for a in filtered if a["client_id"] == client_id]
    if status:
        filtered = [a for a in filtered if a["status"] == status]

    if not filtered:
        return "No appointments found matching the criteria."

    # Sort by date and time
    filtered = sorted(filtered, key=lambda x: (x["date"], x["time"]))

    # Format output
    result = f"Found {len(filtered)} appointment(s):\n\n"
    for apt in filtered:
        result += f"[{apt['id']}] {apt['date']} at {apt['time']}\n"
        result += f"  Client: {apt['client_name']} ({apt['client_id']})\n"
        result += f"  Service: {apt['service_name']}\n"
        result += f"  Provider: {apt['staff_name']}\n"
        result += f"  Duration: {apt['duration_minutes']} min | Price: ${apt['price']:.2f}\n"
        result += f"  Status: {apt['status'].upper()}\n"
        if apt.get('notes'):
            result += f"  Notes: {apt['notes']}\n"
        result += "\n"

    return result


@mcp.tool()
def update_appointment_status(appointment_id: str, status: str, notes: Optional[str] = "") -> str:
    """
    Update the status of an appointment.

    Args:
        appointment_id: Appointment ID (e.g., 'APT0001')
        status: New status (scheduled, completed, cancelled, no-show)
        notes: Optional notes to add

    Returns:
        Confirmation message
    """
    appointments = load_data(APPOINTMENTS_FILE)

    if appointment_id not in appointments:
        return f"Error: Appointment {appointment_id} not found"

    valid_statuses = ["scheduled", "completed", "cancelled", "no-show"]
    if status not in valid_statuses:
        return f"Error: Invalid status. Must be one of: {', '.join(valid_statuses)}"

    appointments[appointment_id]["status"] = status
    if notes:
        appointments[appointment_id]["notes"] = notes
    appointments[appointment_id]["updated_at"] = datetime.now().isoformat()

    save_data(APPOINTMENTS_FILE, appointments)

    return f"✓ Appointment {appointment_id} status updated to: {status.upper()}"


@mcp.tool()
def cancel_appointment(appointment_id: str, reason: Optional[str] = "") -> str:
    """
    Cancel an appointment.

    Args:
        appointment_id: Appointment ID to cancel
        reason: Optional cancellation reason

    Returns:
        Confirmation message
    """
    return update_appointment_status(appointment_id, "cancelled", f"Cancellation reason: {reason}" if reason else "Cancelled")


# ============================================================================
# CLIENT MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def add_client(
    name: str,
    email: str,
    phone: str,
    date_of_birth: str,
    address: Optional[str] = "",
    emergency_contact: Optional[str] = "",
    medical_notes: Optional[str] = ""
) -> str:
    """
    Add a new client to the system.

    Args:
        name: Client's full name
        email: Client's email address
        phone: Client's phone number
        date_of_birth: Date of birth (YYYY-MM-DD)
        address: Optional physical address
        emergency_contact: Optional emergency contact info
        medical_notes: Optional medical history or allergies

    Returns:
        Confirmation with client ID
    """
    clients = load_data(CLIENTS_FILE)

    # Generate new client ID
    client_num = len(clients) + 1
    client_id = f"CL{client_num:04d}"

    client = {
        "id": client_id,
        "name": name,
        "email": email,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "address": address,
        "emergency_contact": emergency_contact,
        "medical_notes": medical_notes,
        "created_at": datetime.now().isoformat(),
        "total_visits": 0,
        "total_spent": 0.0
    }

    clients[client_id] = client
    save_data(CLIENTS_FILE, clients)

    return f"✓ Client added successfully!\n\nID: {client_id}\nName: {name}\nEmail: {email}\nPhone: {phone}"


@mcp.tool()
def get_client(client_id: str) -> str:
    """
    Get detailed information about a client.

    Args:
        client_id: Client ID (e.g., 'CL0001')

    Returns:
        Client details and appointment history
    """
    clients = load_data(CLIENTS_FILE)

    if client_id not in clients:
        return f"Error: Client {client_id} not found"

    client = clients[client_id]
    appointments = load_data(APPOINTMENTS_FILE)

    # Get client's appointments
    client_appointments = [a for a in appointments.values() if a["client_id"] == client_id]

    result = f"CLIENT PROFILE: {client['name']}\n"
    result += "=" * 50 + "\n\n"
    result += f"ID: {client['id']}\n"
    result += f"Email: {client['email']}\n"
    result += f"Phone: {client['phone']}\n"
    result += f"Date of Birth: {client['date_of_birth']}\n"

    if client.get('address'):
        result += f"Address: {client['address']}\n"
    if client.get('emergency_contact'):
        result += f"Emergency Contact: {client['emergency_contact']}\n"
    if client.get('medical_notes'):
        result += f"Medical Notes: {client['medical_notes']}\n"

    result += f"\nTotal Visits: {client['total_visits']}\n"
    result += f"Total Spent: ${client['total_spent']:.2f}\n"
    result += f"Client Since: {client['created_at'][:10]}\n"

    if client_appointments:
        result += f"\n\nAPPOINTMENT HISTORY ({len(client_appointments)} total):\n"
        result += "-" * 50 + "\n"
        for apt in sorted(client_appointments, key=lambda x: (x['date'], x['time']), reverse=True)[:5]:
            result += f"\n{apt['date']} - {apt['service_name']}\n"
            result += f"  Provider: {apt['staff_name']}\n"
            result += f"  Status: {apt['status'].upper()}\n"

    return result


@mcp.tool()
def list_clients(search: Optional[str] = None) -> str:
    """
    List all clients or search by name/email.

    Args:
        search: Optional search term to filter clients by name or email

    Returns:
        Formatted list of clients
    """
    clients = load_data(CLIENTS_FILE)

    if not clients:
        return "No clients found."

    filtered = clients.values()

    if search:
        search_lower = search.lower()
        filtered = [c for c in filtered if
                   search_lower in c['name'].lower() or
                   search_lower in c['email'].lower()]

    if not filtered:
        return f"No clients found matching '{search}'"

    filtered = sorted(filtered, key=lambda x: x['name'])

    result = f"Found {len(filtered)} client(s):\n\n"
    for client in filtered:
        result += f"[{client['id']}] {client['name']}\n"
        result += f"  Email: {client['email']} | Phone: {client['phone']}\n"
        result += f"  Visits: {client['total_visits']} | Total Spent: ${client['total_spent']:.2f}\n\n"

    return result


# ============================================================================
# SERVICE CATALOG TOOLS
# ============================================================================

@mcp.tool()
def list_services(category: Optional[str] = None) -> str:
    """
    List all available services.

    Args:
        category: Optional category filter (Injectables, Facials, Laser Treatments, etc.)

    Returns:
        Formatted list of services with prices and details
    """
    services = load_data(SERVICES_FILE)

    if not services:
        return "No services found."

    filtered = services.values()

    if category:
        filtered = [s for s in filtered if s['category'].lower() == category.lower()]

    if not filtered:
        return f"No services found in category '{category}'"

    # Group by category
    by_category = {}
    for service in filtered:
        cat = service['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(service)

    result = "AVAILABLE SERVICES\n"
    result += "=" * 60 + "\n\n"

    for cat, services_list in sorted(by_category.items()):
        result += f"{cat.upper()}\n"
        result += "-" * 60 + "\n"
        for svc in sorted(services_list, key=lambda x: x['name']):
            result += f"\n[{svc['id']}] {svc['name']}\n"
            result += f"  Price: ${svc['price']:.2f} | Duration: {svc['duration_minutes']} minutes\n"
            result += f"  {svc['description']}\n"
        result += "\n"

    return result


@mcp.tool()
def get_service(service_id: str) -> str:
    """
    Get detailed information about a specific service.

    Args:
        service_id: Service ID (e.g., 'SVC001')

    Returns:
        Detailed service information
    """
    services = load_data(SERVICES_FILE)

    if service_id not in services:
        return f"Error: Service {service_id} not found"

    svc = services[service_id]

    result = f"SERVICE DETAILS\n"
    result += "=" * 50 + "\n\n"
    result += f"ID: {svc['id']}\n"
    result += f"Name: {svc['name']}\n"
    result += f"Category: {svc['category']}\n"
    result += f"Price: ${svc['price']:.2f}\n"
    result += f"Duration: {svc['duration_minutes']} minutes\n"
    result += f"Description: {svc['description']}\n"

    return result


# ============================================================================
# STAFF MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def list_staff(specialty: Optional[str] = None) -> str:
    """
    List all staff members.

    Args:
        specialty: Optional filter by specialty (Injectables, Facials, etc.)

    Returns:
        Formatted list of staff members
    """
    staff = load_data(STAFF_FILE)

    if not staff:
        return "No staff members found."

    filtered = staff.values()

    if specialty:
        filtered = [s for s in filtered if specialty in s['specialties']]

    if not filtered:
        return f"No staff members found with specialty '{specialty}'"

    result = f"STAFF DIRECTORY ({len(filtered)} members)\n"
    result += "=" * 60 + "\n\n"

    for member in sorted(filtered, key=lambda x: x['name']):
        result += f"[{member['id']}] {member['name']}\n"
        result += f"  Role: {member['role']}\n"
        result += f"  Specialties: {', '.join(member['specialties'])}\n"
        result += f"  Available: {', '.join(member['available_days'])}\n"
        result += f"  Hours: {member['hours']['start']} - {member['hours']['end']}\n\n"

    return result


@mcp.tool()
def get_staff(staff_id: str) -> str:
    """
    Get detailed information about a staff member.

    Args:
        staff_id: Staff ID (e.g., 'STF001')

    Returns:
        Staff member details and schedule
    """
    staff = load_data(STAFF_FILE)

    if staff_id not in staff:
        return f"Error: Staff member {staff_id} not found"

    member = staff[staff_id]
    appointments = load_data(APPOINTMENTS_FILE)

    # Get upcoming appointments for this staff member
    staff_appointments = [a for a in appointments.values()
                         if a["staff_id"] == staff_id and a["status"] == "scheduled"]

    result = f"STAFF PROFILE: {member['name']}\n"
    result += "=" * 50 + "\n\n"
    result += f"ID: {member['id']}\n"
    result += f"Role: {member['role']}\n"
    result += f"Specialties: {', '.join(member['specialties'])}\n"
    result += f"Available Days: {', '.join(member['available_days'])}\n"
    result += f"Working Hours: {member['hours']['start']} - {member['hours']['end']}\n"

    if staff_appointments:
        result += f"\n\nUPCOMING APPOINTMENTS ({len(staff_appointments)}):\n"
        result += "-" * 50 + "\n"
        for apt in sorted(staff_appointments, key=lambda x: (x['date'], x['time']))[:10]:
            result += f"\n{apt['date']} at {apt['time']} - {apt['service_name']}\n"
            result += f"  Client: {apt['client_name']}\n"
            result += f"  Duration: {apt['duration_minutes']} min\n"

    return result


# ============================================================================
# AVAILABILITY TOOLS
# ============================================================================

@mcp.tool()
def check_availability(date: str, staff_id: Optional[str] = None) -> str:
    """
    Check appointment availability for a specific date.

    Args:
        date: Date to check in YYYY-MM-DD format
        staff_id: Optional staff member ID to check specific provider availability

    Returns:
        Available time slots
    """
    appointments = load_data(APPOINTMENTS_FILE)
    staff = load_data(STAFF_FILE)

    # Get day of week
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD"

    # Filter staff by availability on this day
    available_staff = {sid: s for sid, s in staff.items()
                      if day_name in s['available_days']}

    if staff_id:
        if staff_id not in available_staff:
            return f"Error: Staff member {staff_id} is not available on {day_name}s"
        available_staff = {staff_id: available_staff[staff_id]}

    if not available_staff:
        return f"No staff members available on {day_name}s"

    result = f"AVAILABILITY FOR {date} ({day_name})\n"
    result += "=" * 60 + "\n\n"

    for sid, member in available_staff.items():
        # Get appointments for this staff member on this date
        staff_apts = [a for a in appointments.values()
                     if a["staff_id"] == sid and a["date"] == date and a["status"] == "scheduled"]

        result += f"{member['name']} ({member['role']})\n"
        result += f"Working hours: {member['hours']['start']} - {member['hours']['end']}\n"

        if staff_apts:
            result += f"Scheduled appointments ({len(staff_apts)}):\n"
            for apt in sorted(staff_apts, key=lambda x: x['time']):
                end_time = (datetime.strptime(apt['time'], "%H:%M") +
                           timedelta(minutes=apt['duration_minutes'])).strftime("%H:%M")
                result += f"  {apt['time']} - {end_time}: {apt['service_name']} ({apt['client_name']})\n"
        else:
            result += "No appointments scheduled - fully available\n"

        result += "\n"

    return result


# ============================================================================
# REPORTING TOOLS
# ============================================================================

@mcp.tool()
def get_daily_schedule(date: str) -> str:
    """
    Get complete schedule for a specific date.

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        Formatted daily schedule with all appointments
    """
    appointments = load_data(APPOINTMENTS_FILE)

    day_appointments = [a for a in appointments.values()
                       if a["date"] == date and a["status"] == "scheduled"]

    if not day_appointments:
        return f"No appointments scheduled for {date}"

    # Sort by time
    day_appointments = sorted(day_appointments, key=lambda x: x['time'])

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A, %B %d, %Y")
    except ValueError:
        day_name = date

    result = f"DAILY SCHEDULE - {day_name}\n"
    result += "=" * 70 + "\n\n"
    result += f"Total appointments: {len(day_appointments)}\n"

    total_revenue = sum(a['price'] for a in day_appointments)
    result += f"Expected revenue: ${total_revenue:.2f}\n\n"
    result += "-" * 70 + "\n\n"

    for apt in day_appointments:
        end_time = (datetime.strptime(apt['time'], "%H:%M") +
                   timedelta(minutes=apt['duration_minutes'])).strftime("%H:%M")

        result += f"{apt['time']} - {end_time}  [{apt['id']}]\n"
        result += f"  Service: {apt['service_name']} (${apt['price']:.2f})\n"
        result += f"  Client: {apt['client_name']} ({apt['client_id']})\n"
        result += f"  Provider: {apt['staff_name']}\n"
        if apt.get('notes'):
            result += f"  Notes: {apt['notes']}\n"
        result += "\n"

    return result


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
