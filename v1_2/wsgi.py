#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app
from app import app

if __name__ == "__main__":
    app.run() 