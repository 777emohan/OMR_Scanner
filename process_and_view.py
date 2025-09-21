#!/usr/bin/env python3
"""
Complete OMR Processing and Viewing Script
Handles everything from processing to HTML generation
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    required_files = [
        'src/preprocessing.py',
        'src/corrected_bubble_detection.py', 
        'src/scoring.py',
        'answers/set1_answer_key_corrected.json',
        'answers/set2_answer_key_corrected.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All requirements met")
    return True

def process_omr_sheets():
    """Process OMR sheets."""
    print("🔄 Processing OMR sheets...")
    
    # Check if we have the processing script
    if os.path.exists('process_sets.py'):
        try:
            result = subprocess.run([sys.executable, 'process_sets.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ OMR processing completed")
                return True
            else:
                print(f"❌ Processing failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Processing error: {e}")
            return False
    else:
        print("⚠️  Processing script not found, using existing results")
        return True

def generate_html():
    """Generate HTML results."""
    print("🔄 Generating HTML results...")
    
    try:
        result = subprocess.run([sys.executable, 'generate_results_html.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ HTML generated successfully")
            return True
        else:
            print(f"❌ HTML generation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ HTML generation error: {e}")
        return False

def open_results():
    """Open results in browser."""
    html_file = 'omr_results_dynamic.html'
    if os.path.exists(html_file):
        print(f"🌐 Opening {html_file} in browser...")
        try:
            webbrowser.open(f'file://{os.path.abspath(html_file)}')
            print("✅ Results opened in browser")
            return True
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"📁 Please open {html_file} manually")
            return False
    else:
        print(f"❌ HTML file not found: {html_file}")
        return False

def main():
    """Main processing function."""
    print("🚀 OMR Processing and Viewing System")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Process OMR sheets
    if not process_omr_sheets():
        print("⚠️  Using existing results")
    
    # Generate HTML
    if not generate_html():
        return 1
    
    # Open results
    open_results()
    
    print("\n🎉 Complete! Your OMR results are ready.")
    print("📊 The HTML file will automatically update when you add new data.")
    print("🔄 To update results: python update_results.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
