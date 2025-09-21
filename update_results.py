#!/usr/bin/env python3
"""
Simple script to update HTML results
Usage: python update_results.py
"""

import subprocess
import sys
import os

def main():
    """Update the HTML results."""
    print("🔄 Updating OMR Results HTML...")
    
    # Check if results file exists
    if not os.path.exists('omr_results_final_corrected.csv'):
        print("❌ Results file not found. Please run the OMR processing first.")
        return 1
    
    # Run the HTML generator
    try:
        result = subprocess.run([sys.executable, 'generate_results_html.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ HTML results updated successfully!")
            print("📊 Open 'omr_results_dynamic.html' to view results")
            return 0
        else:
            print(f"❌ Error updating HTML: {result.stderr}")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
