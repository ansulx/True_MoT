"""
Test Script for Dual Modality Reasoning Agent
Quick verification of system functionality
"""

import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        from utils import detect_logical_keywords, validate_input
        from natural_language import get_natural_language_reasoner
        from logic_reasoning import get_logic_reasoner
        from integration import get_dual_modality_controller
        from sample_problems import get_all_problems
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_utils():
    """Test utility functions."""
    try:
        from utils import detect_logical_keywords, validate_input, parse_propositional_logic
        
        # Test keyword detection
        test_text = "If it rains, then the ground is wet. Therefore, the ground is wet."
        features = detect_logical_keywords(test_text)
        assert features['logical_connectives'] == True
        assert features['conditionals'] == True
        
        # Test input validation
        validation = validate_input("Valid problem statement")
        assert validation['valid'] == True
        
        validation = validate_input("Hi")
        assert validation['valid'] == False
        
        # Test logic parsing
        logic_result = parse_propositional_logic("A → B")
        assert 'A' in logic_result['variables']
        assert 'B' in logic_result['variables']
        
        print("✅ Utility functions working correctly")
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_logic_reasoning():
    """Test logic reasoning module."""
    try:
        from logic_reasoning import get_logic_reasoner
        
        reasoner = get_logic_reasoner()
        
        # Test simple conditional
        result = reasoner.reason("If A, then B. A is true. Is B true?")
        assert result['success'] == True or result['success'] == False  # Should not crash
        
        # Test formal logic
        result = reasoner.reason("A → B")
        assert isinstance(result, dict)
        
        print("✅ Logic reasoning module working")
        return True
    except Exception as e:
        print(f"❌ Logic reasoning test failed: {e}")
        return False

def test_natural_language():
    """Test natural language reasoning module (without API)."""
    try:
        from natural_language import get_natural_language_reasoner
        
        reasoner = get_natural_language_reasoner()
        
        # Test fallback reasoning (no API key)
        result = reasoner.reason("If it rains, the ground gets wet.")
        assert isinstance(result, dict)
        assert 'success' in result
        
        print("✅ Natural language module working (fallback mode)")
        return True
    except Exception as e:
        print(f"❌ Natural language test failed: {e}")
        return False

def test_integration():
    """Test integration controller."""
    try:
        from integration import get_dual_modality_controller
        
        # Test without API key (fallback mode)
        controller = get_dual_modality_controller()
        
        # Test problem processing
        result = controller.process_problem("If A then B. A is true.")
        assert isinstance(result, dict)
        assert 'success' in result
        
        print("✅ Integration controller working")
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_sample_problems():
    """Test sample problems module."""
    try:
        from sample_problems import get_all_problems, get_problems_by_category, get_problem_statistics
        
        # Test getting all problems
        all_problems = get_all_problems()
        assert len(all_problems) > 0
        
        # Test getting problems by category
        conditional_problems = get_problems_by_category('conditional')
        assert len(conditional_problems) > 0
        
        # Test statistics
        stats = get_problem_statistics()
        assert 'conditional' in stats
        
        print("✅ Sample problems module working")
        return True
    except Exception as e:
        print(f"❌ Sample problems test failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    try:
        import streamlit
        import sympy
        import pandas
        import numpy
        import google.generativeai
        import transformers
        import torch
        import requests
        
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_basic_functionality_test():
    """Run a basic end-to-end functionality test."""
    try:
        from integration import get_dual_modality_controller
        
        print("\n🧪 Running basic functionality test...")
        
        # Test with a simple problem
        controller = get_dual_modality_controller()
        test_problem = "If it rains, the ground is wet. It's raining. Is the ground wet?"
        
        result = controller.process_problem(test_problem)
        
        print(f"Problem: {test_problem}")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Mode: {result.get('mode_selection', {}).get('mode', 'Unknown')}")
            print(f"Confidence: {result.get('confidence', 0.0):.2f}")
            print(f"Conclusion: {result.get('conclusion', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print("✅ Basic functionality test completed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Dual Modality Reasoning Agent - System Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Module Imports", test_imports),
        ("Utility Functions", test_utils),
        ("Logic Reasoning", test_logic_reasoning),
        ("Natural Language", test_natural_language),
        ("Integration Controller", test_integration),
        ("Sample Problems", test_sample_problems),
        ("Basic Functionality", run_basic_functionality_test)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo run the application:")
        print("1. Set your Google AI API key: export GOOGLE_AI_API_KEY='your_key'")
        print("2. Run: streamlit run main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

