"""
Setup script for Face Detection App.

This script helps set up the environment correctly, including installing dependencies
and checking if everything is properly configured.
"""

import os
import sys
import subprocess
import platform

def run_command(command):
    """Run a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def main():
    print("=" * 70)
    print("Face Detection App - Setup Script")
    print("=" * 70)
    
    # Check if running in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"Running in virtual environment: {'Yes' if in_venv else 'No'}")
    
    if not in_venv:
        print("\nWARNING: You are not running in a virtual environment.")
        create_venv = input("Do you want to create and activate a virtual environment now? (y/n): ").lower().strip()
        
        if create_venv == 'y':
            print("\nCreating virtual environment...")
            success, output = run_command("python -m venv venv")
            
            if success:
                print("Virtual environment created successfully!")
                print("\nPlease activate the virtual environment and run this script again:")
                if platform.system() == 'Windows':
                    print(r"venv\Scripts\activate")
                else:
                    print("source venv/bin/activate")
                return
            else:
                print(f"Failed to create virtual environment: {output}")
                proceed = input("Do you want to proceed without a virtual environment? (y/n): ").lower().strip()
                if proceed != 'y':
                    print("Setup aborted. Please create a virtual environment manually and try again.")
                    return
        else:
            print("Proceeding without a virtual environment...")
    
    # Upgrading pip
    print("\nUpgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Installing dependencies
    print("\nInstalling dependencies from requirements.txt...")
    success, output = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    if not success:
        print(f"Error installing dependencies: {output}")
        print("\nAttempting to install MediaPipe specifically...")
        run_command(f"{sys.executable} -m pip install mediapipe==0.10.21")
    
    # Verify installation by running the setup check
    print("\nVerifying installation...")
    if os.path.exists("setup_check.py"):
        run_command(f"{sys.executable} setup_check.py")
    
    print("\n" + "=" * 70)
    print("Setup completed! You can now run the application with:")
    print(f"{sys.executable} app.py")
    print("=" * 70)

if __name__ == "__main__":
    main() 