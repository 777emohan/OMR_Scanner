#!/usr/bin/env python3
"""
Setup script for OMR Evaluation System
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages."""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\nCreating directories...")
    directories = ["data", "answers", "results", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_sample_data():
    """Create sample data files."""
    print("\nCreating sample data...")
    
    # Create sample answer key if it doesn't exist
    answer_key_file = "answers/sample_answer_key.json"
    if not os.path.exists(answer_key_file):
        try:
            from src.scoring import create_sample_answer_key
            create_sample_answer_key(answer_key_file, rows=20, cols=5)
            print(f"✓ Created sample answer key: {answer_key_file}")
        except Exception as e:
            print(f"⚠️  Could not create sample answer key: {e}")
    
    # Create a simple test image
    test_img_file = "data/test_sheet.jpg"
    if not os.path.exists(test_img_file):
        try:
            import cv2
            import numpy as np
            
            # Create a simple test OMR sheet
            img = np.ones((800, 1000), dtype=np.uint8) * 255
            
            # Draw some test bubbles
            for i in range(20):
                for j in range(5):
                    y1, y2 = i * 40, (i + 1) * 40
                    x1, x2 = j * 200, (j + 1) * 200
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    cv2.circle(img, center, 15, 0, -1)
            
            cv2.imwrite(test_img_file, img)
            print(f"✓ Created test image: {test_img_file}")
            
        except Exception as e:
            print(f"⚠️  Could not create test image: {e}")

def run_tests():
    """Run basic tests."""
    print("\nRunning tests...")
    try:
        subprocess.check_call([sys.executable, "test_omr.py"])
        print("✓ Tests completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  Test file not found, skipping tests")
        return True

def main():
    """Main setup function."""
    print("OMR Evaluation System - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create directories
    create_directories()
    
    # Create sample data
    create_sample_data()
    
    # Run tests
    if run_tests():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run the web interface: streamlit run streamlit_app.py")
        print("2. Or use the CLI: python src/main.py --help")
        print("3. Check the README.md for detailed usage instructions")
    else:
        print("\n⚠️  Setup completed with warnings. Please check the test results.")

if __name__ == "__main__":
    main()
