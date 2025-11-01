# Miami Med Spa Portal - FastMCP Server

A comprehensive FastMCP server for managing a medical spa in Miami. This server provides AI assistants with tools to manage appointments, clients, services, and staff through the Model Context Protocol (MCP).

## 🎯 Two Ways to Use This System

### 1. 📞 **Voice AI Phone Assistant** (Recommended for Client Booking)
Let your clients call a phone number and book appointments by talking naturally with an AI receptionist. No forms, no apps - just call and book!

**Perfect for:** Clients on the go who want to book quickly

👉 **[See Voice AI Setup Guide](VOICE_AI_SETUP.md)** for complete instructions

### 2. 💬 **MCP Server for Claude Desktop** (For Business Management)
Use with Claude Desktop to manage your spa business, view schedules, and handle operations.

**Perfect for:** Spa owners and managers

---

## Features

### Appointment Management
- Create appointments with clients, services, and staff
- List appointments with filters (date, client, status)
- Update appointment status (scheduled, completed, cancelled, no-show)
- Cancel appointments with reasons
- Check availability for staff members
- Get daily schedules with revenue projections

### Client Management
- Add new clients with contact info and medical history
- View detailed client profiles with appointment history
- Search clients by name or email
- Track client visits and spending

### Service Catalog
- Pre-loaded with common med-spa services:
  - Botox & Dermal Fillers (Injectables)
  - Hydrafacials & Chemical Peels (Facials)
  - Laser Hair Removal (Laser Treatments)
  - Microneedling & CoolSculpting (Body Contouring)
- View services by category
- Get detailed service information with pricing

### Staff Management
- Manage staff members with specialties
- View staff schedules and availability
- Track staff appointments
- Filter staff by specialty

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd med-spa-portal-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using pyproject.toml:
```bash
pip install -e .
```

## Quick Start for Voice AI Phone System

Want clients to call and book via phone? Follow these steps:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the API server
./start_api.sh          # Mac/Linux
# OR
start_api.bat           # Windows

# 3. Follow the Voice AI Setup Guide
# See VOICE_AI_SETUP.md for complete instructions
```

Your API will be running at `http://localhost:8000`

Then follow **[VOICE_AI_SETUP.md](VOICE_AI_SETUP.md)** to:
- Deploy your API to the internet (Replit/Railway - free options available)
- Set up Vapi.ai voice assistant (~$0.05/min)
- Get a Miami phone number ($1-2/month)
- Go live with AI phone booking!

**Total setup time:** ~15 minutes
**Monthly cost:** ~$20-50 (based on call volume)

## Running the Server

### Option 1: Direct Execution
```bash
python server.py
```

### Option 2: Using FastMCP CLI
```bash
fastmcp run server.py
```

### Option 3: As MCP Server with Claude Desktop

Add to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "miami-medspa": {
      "command": "python",
      "args": ["/absolute/path/to/med-spa-portal-1/server.py"]
    }
  }
}
```

## Usage Examples

### Creating a Client
```python
# Use the add_client tool
add_client(
    name="Sofia Martinez",
    email="sofia.martinez@email.com",
    phone="305-555-0123",
    date_of_birth="1985-03-15",
    address="123 Ocean Drive, Miami Beach, FL 33139",
    medical_notes="No known allergies"
)
```

### Booking an Appointment
```python
# Use the create_appointment tool
create_appointment(
    client_id="CL0001",
    service_id="SVC001",  # Botox Treatment
    staff_id="STF001",    # Dr. Maria Rodriguez
    date="2025-11-15",
    time="14:00",
    notes="First-time Botox client"
)
```

### Viewing Daily Schedule
```python
# Use the get_daily_schedule tool
get_daily_schedule(date="2025-11-15")
```

### Checking Availability
```python
# Check availability for all staff on a date
check_availability(date="2025-11-15")

# Check availability for specific staff member
check_availability(date="2025-11-15", staff_id="STF001")
```

### Listing Services
```python
# List all services
list_services()

# List services by category
list_services(category="Injectables")
```

## Available Tools

### Appointment Tools
- `create_appointment` - Schedule a new appointment
- `list_appointments` - View appointments with filters
- `update_appointment_status` - Change appointment status
- `cancel_appointment` - Cancel an appointment
- `get_daily_schedule` - View complete daily schedule
- `check_availability` - Check staff availability

### Client Tools
- `add_client` - Register new client
- `get_client` - View client profile and history
- `list_clients` - Search and list clients

### Service Tools
- `list_services` - Browse service catalog
- `get_service` - View service details

### Staff Tools
- `list_staff` - View staff directory
- `get_staff` - View staff profile and schedule

## Data Storage

The server uses JSON files for data persistence:
- `data/appointments.json` - All appointments
- `data/clients.json` - Client records
- `data/services.json` - Service catalog
- `data/staff.json` - Staff directory

Data is automatically created in the `data/` directory when the server first runs.

## Default Services

The server comes pre-configured with these services:

| Service | Category | Duration | Price |
|---------|----------|----------|-------|
| Botox Treatment | Injectables | 30 min | $400 |
| Dermal Fillers | Injectables | 45 min | $650 |
| Hydrafacial | Facials | 60 min | $250 |
| Laser Hair Removal | Laser Treatments | 30 min | $300 |
| Chemical Peel | Skin Treatments | 45 min | $200 |
| Microneedling | Skin Treatments | 60 min | $350 |
| CoolSculpting | Body Contouring | 90 min | $800 |

## Default Staff

Pre-configured staff members:

- **Dr. Maria Rodriguez** - Medical Director (Injectables, Laser Treatments)
- **Sarah Johnson** - Licensed Aesthetician (Facials, Skin Treatments)
- **Jennifer Martinez** - Nurse Practitioner (Injectables, Body Contouring)

## Development

### Project Structure
```
med-spa-portal-1/
├── server.py              # Main FastMCP server
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── README.md             # This file
└── data/                 # Data storage (auto-created)
    ├── appointments.json
    ├── clients.json
    ├── services.json
    └── staff.json
```

### Adding New Services
Edit `data/services.json` or modify the `initialize_default_data()` function in `server.py`.

### Adding New Staff
Edit `data/staff.json` or modify the `initialize_default_data()` function in `server.py`.

## Use Cases

This MCP server enables AI assistants to:
- Schedule and manage appointments for clients
- Answer questions about services and pricing
- Check provider availability
- Track client history and preferences
- Generate daily schedules and reports
- Manage cancellations and rescheduling
- Provide service recommendations based on client needs

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Support

For questions or support, please open an issue in the repository.

---

Built with [FastMCP](https://github.com/jlowin/fastmcp) - A fast, Pythonic way to build MCP servers.
