#!/bin/bash
# Install backend dependencies

echo "🔧 Installing backend dependencies..."

# Activate venv
source venv/bin/activate

# Install packages
pip install fastapi==0.109.0
pip install "uvicorn[standard]==0.27.0"
pip install httpx==0.26.0
pip install pydantic==2.5.3
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install websockets==12.0

echo "✅ Dependencies installed!"
echo ""
echo "Now run: python run_backend.py"
