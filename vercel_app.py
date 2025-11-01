"""
Vercel-compatible entry point for the API server
"""
from api_server import app

# Vercel needs a variable named 'app' to be exported
# This is already done in api_server.py, but we create this file
# to ensure proper Vercel compatibility

# The app instance from api_server.py is automatically used by Vercel
