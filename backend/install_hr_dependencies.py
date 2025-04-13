"""
Install HR Analytics Dependencies

This script installs the required dependencies for the HR Analytics module.
"""

import subprocess
import sys

def install_dependencies():
    """Install the required dependencies for HR Analytics"""
    print("Installing HR Analytics dependencies...")
    
    # List of dependencies to install
    dependencies = [
        "pandas>=2.0.0",
        "langchain>=0.0.267",
        "langchain-community>=0.0.1",
        "langchain-openai>=0.0.1",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "streamlit>=1.24.0"
    ]
    
    # Install each dependency
    for dependency in dependencies:
        print(f"Installing {dependency}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
            print(f"Successfully installed {dependency}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {dependency}: {e}")
    
    print("\nAll HR Analytics dependencies installed successfully!")

if __name__ == "__main__":
    install_dependencies()
