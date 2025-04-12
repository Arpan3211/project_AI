import subprocess
import sys
import os

def install_dependencies():
    """Install the required dependencies."""
    print("Installing dependencies...")
    
    # Get the requirements file path
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    try:
        # Run pip install
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
