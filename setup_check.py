"""
MediaPipe and dependencies diagnostic script.
Run this to verify that your environment is correctly set up.
"""

import os
import sys
import platform
import subprocess

print("=" * 60)
print("Face Detection App - Environment Setup Check")
print("=" * 60)

# Get system information
print(f"OS: {platform.system()} {platform.version()}")
print(f"Python: {sys.version}")
print(f"Python executable: {sys.executable}")
print("-" * 60)

# Check if running in a virtual environment
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
print(f"Running in virtual environment: {'Yes' if in_venv else 'No'}")

if not in_venv:
    print("WARNING: Not running in a virtual environment. It's recommended to use a virtual environment.")
    print("Create a virtual environment with: python -m venv venv")
    print("Activate it with: ")
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
print("-" * 60)

# Check for required packages
required_packages = {
    "Flask": "flask",
    "OpenCV": "opencv-python",
    "MediaPipe": "mediapipe==0.10.21",
    "NumPy": "numpy"
}

print("Checking required packages:")
for package_name, pip_name in required_packages.items():
    print(f"\n> Checking {package_name}...")
    try:
        if package_name == "Flask":
            import flask
            print(f"  - Flask version: {flask.__version__}")
        elif package_name == "OpenCV":
            import cv2
            print(f"  - OpenCV version: {cv2.__version__}")
        elif package_name == "MediaPipe":
            try:
                import mediapipe as mp
                print(f"  - MediaPipe version: {mp.__version__}")
                print("  - MediaPipe import successful!")
            except ImportError as e:
                print(f"  - MediaPipe import failed: {e}")
                print(f"  - Try reinstalling with: pip install {pip_name}")
                print("  - If that doesn't work, try completely removing and reinstalling:")
                print(f"    pip uninstall -y mediapipe && pip install {pip_name}")
        elif package_name == "NumPy":
            import numpy as np
            print(f"  - NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"  - {package_name} not found: {e}")
        print(f"  - Try installing with: pip install {pip_name}")

print("\n" + "=" * 60)
print("Setup check completed!")

# Provide next steps
print("\nNext steps:")
print("1. If any packages are missing, install them using the commands above.")
print("2. If MediaPipe is not working, try reinstalling it with the specific version:")
print("   pip install mediapipe==0.10.21")
print("3. Run the main application with: python app.py")
print("=" * 60) 