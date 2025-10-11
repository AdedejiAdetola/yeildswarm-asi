#!/bin/bash
# Start YieldSwarm AI Backend Server

cd "$(dirname "$0")/.."
source venv/bin/activate
cd backend
python3 main.py
