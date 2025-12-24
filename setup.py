"""
Setup script for Dual Modality Reasoning Agent
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are available."""
    print("Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'sympy',
        'pandas',
        'numpy',
        'requests'
    ]
    
    optional_packages = [
        'google.generativeai'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (required)")
            missing_required.append(package)
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} (optional)")
        except ImportError:
            print(f"⚠️  {package} (optional - for Google Gemini API)")
            missing_optional.append(package)
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("The system will work with fallback reasoning, but Google Gemini API features won't be available.")
    
    return True

def test_basic_functionality():
    """Test basic system functionality."""
    print("\nTesting basic functionality...")
    
    try:
        # Test imports
        from utils import detect_logical_keywords
        from logic_reasoning import get_logic_reasoner
        from sample_problems import get_all_problems
        
        print("✅ Core modules import successfully")
        
        # Test logic reasoning
        reasoner = get_logic_reasoner()
        result = reasoner.reason("If A then B")
        print("✅ Logic reasoning works")
        
        # Test sample problems
        problems = get_all_problems()
        print(f"✅ Sample problems loaded ({len(problems)} problems)")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def setup_api_key():
    """Guide user through API key setup."""
    print("\n🔑 Google AI API Key Setup")
    print("=" * 30)
    
    print("To use natural language reasoning, you need a Google AI API key.")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create a new API key (free tier available)")
    print("3. Set it as an environment variable:")
    print("   export GOOGLE_AI_API_KEY='your_api_key_here'")
    print("\nOr enter it in the Streamlit interface when you run the app.")
    print("\nThe system will work without the API key using fallback reasoning.")

def main():
    """Main setup function."""
    print("🚀 Dual Modality Reasoning Agent - Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("Setup failed. Please fix dependency issues.")
        return
    
    # Test functionality
    if not test_basic_functionality():
        print("Setup completed but basic tests failed.")
        print("The system may still work - try running the app.")
    else:
        print("✅ Setup completed successfully!")
    
    # API key guidance
    setup_api_key()
    
    print("\n🎉 Setup Complete!")
    print("\nTo run the application:")
    print("streamlit run main.py")
    print("\nTo run tests:")
    print("python test_system.py")

if __name__ == "__main__":
    main()

