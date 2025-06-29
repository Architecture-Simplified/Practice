#!/usr/bin/env python3
"""
Setup script for the development environment.
"""

import os
import subprocess
import sys

def create_virtual_environment():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created!")

def install_dependencies():
    """Install project dependencies."""
    print("Installing dependencies...")
    venv_python = os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed!")

def main():
    """Main setup function."""
    print("Setting up Python project...")
    create_virtual_environment()
    install_dependencies()
    print("Setup complete! Activate your virtual environment with:")
    if os.name == "nt":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")

if __name__ == "__main__":
    main()
