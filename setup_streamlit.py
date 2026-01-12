#!/usr/bin/env python3
"""
Quick setup and launcher for the Streamlit UI
Run this script to install dependencies and launch the Streamlit app
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Ensure Python 3.11 or higher is being used"""
    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 11):
        print(f"❌ Python 3.11+ required. You have Python {version_info.major}.{version_info.minor}")
        sys.exit(1)
    print(f"✅ Python {version_info.major}.{version_info.minor} detected")

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if not env_path.exists():
        print("\n⚠️  WARNING: .env file not found!")
        print("   You need to create a .env file with your API keys.")
        print("   Example:")
        print("   --------")
        print("   GOOGLE_API_KEY=your_key_here")
        print("   --------")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✅ .env file found")

def install_dependencies():
    """Install required packages from pyproject.toml"""
    print("\n📦 Installing dependencies...")
    try:
        # Install in editable mode which installs from pyproject.toml
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Failed to install dependencies")
            print(result.stderr)
            sys.exit(1)
        
        print("✅ Dependencies installed successfully")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def launch_streamlit():
    """Launch the Streamlit app"""
    print("\n🚀 Launching Streamlit app...")
    print("   The app will open in your browser at http://localhost:8501")
    print("   Press Ctrl+C to stop the app\n")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
            check=True
        )
    except subprocess.CalledProcessError:
        print("\n❌ Failed to launch Streamlit app")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Streamlit app stopped")

def main():
    """Main setup and launch flow"""
    print("\n" + "="*50)
    print("   🤖 AI Agent Debugger - Streamlit Setup")
    print("="*50 + "\n")
    
    check_python_version()
    check_env_file()
    install_dependencies()
    
    # Ask if user wants to launch now
    response = input("\nLaunch Streamlit app now? (y/n): ")
    if response.lower() == 'y':
        launch_streamlit()
    else:
        print("\n✅ Setup complete! To launch the app later, run:")
        print("   streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
