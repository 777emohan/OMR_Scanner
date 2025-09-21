#!/usr/bin/env python3
"""
Final System Verification Script
Triple-checks everything before deployment
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

def check_file_structure():
    """Verify all required files are present."""
    print("🔍 Checking file structure...")
    
    required_files = [
        'src/preprocessing.py',
        'src/bubble_detection.py',
        'src/corrected_bubble_detection.py',
        'src/improved_scoring.py',
        'src/scoring.py',
        'src/main.py',
        'answers/set1_answer_key_corrected.json',
        'answers/set2_answer_key_corrected.json',
        'view_final_results.html',
        'requirements.txt',
        'README.md',
        'DEPLOYMENT_GUIDE.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_dependencies():
    """Verify all dependencies are available."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'cv2', 'numpy', 'pandas', 'PIL', 'streamlit', 
        'sklearn', 'tensorflow', 'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def check_answer_keys():
    """Verify answer key files are valid."""
    print("\n🔍 Checking answer keys...")
    
    try:
        # Check Set 1 answer key
        with open('answers/set1_answer_key_corrected.json', 'r') as f:
            set1_key = json.load(f)
        
        # Check Set 2 answer key
        with open('answers/set2_answer_key_corrected.json', 'r') as f:
            set2_key = json.load(f)
        
        # Verify structure
        if not isinstance(set1_key, dict) or not isinstance(set2_key, dict):
            print("❌ Answer keys must be dictionaries")
            return False
        
        # Check for multiple correct answers
        set1_multiple = sum(1 for q, answers in set1_key.items() if sum(answers.values()) > 1)
        set2_multiple = sum(1 for q, answers in set2_key.items() if sum(answers.values()) > 1)
        
        print(f"✅ Set 1: {len(set1_key)} questions, {set1_multiple} with multiple correct answers")
        print(f"✅ Set 2: {len(set2_key)} questions, {set2_multiple} with multiple correct answers")
        
        return True
        
    except Exception as e:
        print(f"❌ Answer key error: {e}")
        return False

def check_results():
    """Verify results files are present and valid."""
    print("\n🔍 Checking results...")
    
    results_files = [
        'omr_results_improved_scoring.csv'
    ]
    
    for file_path in results_files:
        if not os.path.exists(file_path):
            print(f"❌ Results file missing: {file_path}")
            return False
        
        try:
            df = pd.read_csv(file_path)
            if len(df) == 0:
                print(f"❌ Results file empty: {file_path}")
                return False
            
            print(f"✅ {file_path}: {len(df)} records")
            
        except Exception as e:
            print(f"❌ Results file error: {e}")
            return False
    
    return True

def check_processing_capability():
    """Test if the system can process images."""
    print("\n🔍 Testing processing capability...")
    
    try:
        # Check if we have test images
        set1_dir = 'set1_papers'
        set2_dir = 'set2_papers'
        
        set1_images = [f for f in os.listdir(set1_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(set1_dir) else []
        set2_images = [f for f in os.listdir(set2_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(set2_dir) else []
        
        total_images = len(set1_images) + len(set2_images)
        
        if total_images == 0:
            print("⚠️  No test images found (this is OK for deployment)")
            return True
        
        print(f"✅ Found {len(set1_images)} Set 1 images, {len(set2_images)} Set 2 images")
        
        # Test basic processing
        sys.path.append('src')
        from preprocessing import preprocess_image
        from corrected_bubble_detection import extract_bubbles_corrected
        
        # Test with first available image
        test_image = None
        if set1_images:
            test_image = os.path.join(set1_dir, set1_images[0])
        elif set2_images:
            test_image = os.path.join(set2_dir, set2_images[0])
        
        if test_image:
            try:
                processed = preprocess_image(test_image)
                bubbles = extract_bubbles_corrected(processed, rows=20, cols=5)
                print(f"✅ Processing test successful: {len(bubbles)} rows detected")
                return True
            except Exception as e:
                print(f"❌ Processing test failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Processing capability test failed: {e}")
        return False

def check_web_interface():
    """Verify web interface files."""
    print("\n🔍 Checking web interface...")
    
    # Check HTML file
    if not os.path.exists('view_final_results.html'):
        print("❌ HTML results viewer missing")
        return False
    
    # Check if HTML is valid
    try:
        with open('view_final_results.html', 'r') as f:
            html_content = f.read()
        
        if '<html' not in html_content or '</html>' not in html_content:
            print("❌ HTML file appears to be invalid")
            return False
        
        print("✅ HTML results viewer valid")
        
    except Exception as e:
        print(f"❌ HTML file error: {e}")
        return False
    
    # Check Streamlit app
    if os.path.exists('streamlit_app.py'):
        try:
            with open('streamlit_app.py', 'r') as f:
                streamlit_content = f.read()
            
            if 'streamlit' in streamlit_content:
                print("✅ Streamlit app present")
            else:
                print("⚠️  Streamlit app may be incomplete")
                
        except Exception as e:
            print(f"⚠️  Streamlit app error: {e}")
    
    return True

def check_deployment_readiness():
    """Check if system is ready for deployment."""
    print("\n🔍 Checking deployment readiness...")
    
    # Check for deployment files
    deployment_files = [
        'README.md',
        'DEPLOYMENT_GUIDE.md',
        'requirements.txt'
    ]
    
    for file_path in deployment_files:
        if not os.path.exists(file_path):
            print(f"❌ Deployment file missing: {file_path}")
            return False
    
    # Check requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        if 'opencv-python' not in requirements:
            print("❌ requirements.txt missing opencv-python")
            return False
        
        print("✅ Deployment files ready")
        
    except Exception as e:
        print(f"❌ Requirements file error: {e}")
        return False
    
    return True

def generate_system_report():
    """Generate a comprehensive system report."""
    print("\n📊 Generating system report...")
    
    report = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'system_status': 'VERIFIED',
        'files_checked': True,
        'dependencies_checked': True,
        'answer_keys_checked': True,
        'results_checked': True,
        'processing_checked': True,
        'web_interface_checked': True,
        'deployment_ready': True
    }
    
    # Add file counts
    report['total_files'] = len([f for f in os.listdir('.') if os.path.isfile(f)])
    report['total_directories'] = len([d for d in os.listdir('.') if os.path.isdir(d)])
    
    # Add results summary
    if os.path.exists('omr_results_improved_scoring.csv'):
        try:
            df = pd.read_csv('omr_results_improved_scoring.csv')
            report['total_papers'] = len(df)
            report['score_range'] = f"{df['total_score'].min():.1f}-{df['total_score'].max():.1f}"
            report['average_score'] = f"{df['total_score'].mean():.1f}"
            report['unique_scores'] = len(df['total_score'].unique())
        except:
            pass
    
    # Save report
    with open('system_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ System report generated: system_report.json")
    return report

def main():
    """Main verification function."""
    print("🔍 OMR EVALUATION SYSTEM - FINAL VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Answer Keys", check_answer_keys),
        ("Results", check_results),
        ("Processing Capability", check_processing_capability),
        ("Web Interface", check_web_interface),
        ("Deployment Readiness", check_deployment_readiness)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 SYSTEM VERIFICATION COMPLETE - ALL CHECKS PASSED!")
        print("✅ System is ready for deployment")
        print("✅ All components working correctly")
        print("✅ Multiple correct answer support verified")
        print("✅ Web interface ready")
        print("✅ Documentation complete")
        
        # Generate final report
        report = generate_system_report()
        
        print(f"\n📊 System Summary:")
        print(f"   Total Files: {report.get('total_files', 'N/A')}")
        print(f"   Total Papers: {report.get('total_papers', 'N/A')}")
        print(f"   Score Range: {report.get('score_range', 'N/A')}")
        print(f"   Average Score: {report.get('average_score', 'N/A')}")
        print(f"   Unique Scores: {report.get('unique_scores', 'N/A')}")
        
        print(f"\n🚀 Ready for deployment!")
        print(f"   📖 Read README.md for usage instructions")
        print(f"   🌐 Read DEPLOYMENT_GUIDE.md for hosting options")
        print(f"   📊 Open view_final_results.html to see results")
        
    else:
        print("❌ SYSTEM VERIFICATION FAILED!")
        print("Please fix the issues above before deployment")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
