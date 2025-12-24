"""
Demo Script for Dual Modality Reasoning Agent
Runs the system without external API dependencies
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_core_functionality():
    """Test core functionality without external APIs."""
    print("🧪 Testing Core Functionality")
    print("=" * 40)
    
    try:
        # Test imports
        print("Testing imports...")
        from utils import detect_logical_keywords, validate_input
        from logic_reasoning import get_logic_reasoner
        from sample_problems import get_all_problems
        print("✅ All core modules imported successfully")
        
        # Test logic reasoning
        print("\nTesting logic reasoning...")
        reasoner = get_logic_reasoner()
        
        test_cases = [
            "If A then B",
            "A ∧ B",
            "A ∨ B",
            "If it rains, the ground is wet. It's raining. Is the ground wet?"
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"  Test {i}: {test_case}")
            result = reasoner.reason(test_case)
            print(f"    Success: {result['success']}")
            print(f"    Confidence: {result['confidence']:.2f}")
            if result['truth_table']:
                print(f"    Truth table generated: {len(result['truth_table'])} rows")
        
        # Test sample problems
        print("\nTesting sample problems...")
        problems = get_all_problems()
        print(f"✅ Loaded {len(problems)} sample problems")
        
        # Show problem categories
        categories = {}
        for problem in problems:
            cat = problem.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("Problem categories:")
        for cat, count in categories.items():
            print(f"  {cat}: {count} problems")
        
        print("\n✅ Core functionality test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def run_interactive_demo():
    """Run an interactive demo of the system."""
    print("\n🎮 Interactive Demo")
    print("=" * 30)
    
    try:
        from logic_reasoning import get_logic_reasoner
        from utils import detect_logical_keywords
        
        reasoner = get_logic_reasoner()
        
        print("Enter logical problems to analyze (type 'quit' to exit):")
        print("Examples:")
        print("  - If A then B")
        print("  - A ∧ B")
        print("  - If it rains, the ground is wet")
        print()
        
        while True:
            try:
                problem = input("Problem: ").strip()
                
                if problem.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not problem:
                    continue
                
                print(f"\nAnalyzing: {problem}")
                
                # Detect logical features
                features = detect_logical_keywords(problem)
                print(f"Features detected: {features}")
                
                # Analyze with logic reasoner
                result = reasoner.reason(problem)
                
                print(f"Success: {result['success']}")
                print(f"Confidence: {result['confidence']:.2f}")
                print(f"Result: {result['result']}")
                print(f"Conclusion: {result['conclusion']}")
                
                if result['truth_table']:
                    print(f"Truth table ({len(result['truth_table'])} rows):")
                    for i, row in enumerate(result['truth_table'][:5]):  # Show first 5 rows
                        print(f"  {i+1}: {row}")
                    if len(result['truth_table']) > 5:
                        print(f"  ... and {len(result['truth_table']) - 5} more rows")
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("Demo completed!")
        
    except Exception as e:
        print(f"❌ Interactive demo failed: {e}")

def show_sample_problems():
    """Display sample problems."""
    print("\n📚 Sample Problems")
    print("=" * 30)
    
    try:
        from sample_problems import get_problems_by_category
        
        categories = ['conditional', 'formal_logic', 'categorical']
        
        for category in categories:
            problems = get_problems_by_category(category)
            print(f"\n{category.upper()} PROBLEMS:")
            
            for i, problem in enumerate(problems[:3], 1):  # Show first 3
                print(f"{i}. {problem['problem']}")
                print(f"   Difficulty: {problem['difficulty']}")
                print(f"   Expected mode: {problem['expected_mode']}")
                print()
        
        print("Run the interactive demo to test these problems!")
        
    except Exception as e:
        print(f"❌ Error showing sample problems: {e}")

def main():
    """Main demo function."""
    print("🧠 Dual Modality Reasoning Agent - Demo")
    print("=" * 50)
    print("This demo shows the core functionality without external APIs.")
    print("The logic reasoning module works independently.")
    print()
    
    # Test core functionality
    if not test_core_functionality():
        print("❌ Core functionality test failed. Please check your installation.")
        return
    
    # Show sample problems
    show_sample_problems()
    
    # Ask if user wants interactive demo
    try:
        response = input("\nWould you like to run the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            run_interactive_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    
    print("\n🎉 Demo completed!")
    print("\nTo run the full Streamlit application:")
    print("1. Get a Google AI API key from: https://makersuite.google.com/app/apikey")
    print("2. Set it: export GOOGLE_AI_API_KEY='your_key'")
    print("3. Run: streamlit run main.py")

if __name__ == "__main__":
    main()
