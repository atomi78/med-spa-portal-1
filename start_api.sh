#!/bin/bash

echo "🚀 Starting Miami Med Spa Voice AI API Server..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✓ Dependencies ready"
echo ""
echo "🌐 Starting API server on http://0.0.0.0:8000"
echo ""
echo "API will be available at:"
echo "  - Health check: http://localhost:8000/"
echo "  - Services: http://localhost:8000/services"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 api_server.py
