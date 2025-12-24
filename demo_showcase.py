"""
Demonstration Showcase for Dual Modality Reasoning Agent
Shows the system's capabilities for research presentation
"""

from logic_reasoning import get_logic_reasoner
from utils import detect_logical_keywords

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)

def print_result(problem, result, features):
    """Print a formatted result."""
    print(f"\nProblem: {problem}")
    print(f"Features: {[k for k, v in features.items() if v]}")
    print(f"Success: {'✅' if result['success'] else '❌'}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Conclusion: {result['conclusion']}")
    if result['truth_table']:
        print(f"Truth Table: {len(result['truth_table'])} rows")
        print("Sample rows:")
        for i, row in enumerate(result['truth_table'][:3]):
            print(f"  {i+1}. {row}")

def main():
    print_section("DUAL MODALITY REASONING AGENT DEMONSTRATION")
    print("Research-Grade AI System for Logical Reasoning")
    print("Integrating Formal Logic with Natural Language Processing")
    
    reasoner = get_logic_reasoner()
    
    # Demonstration problems
    demo_problems = [
        {
            "title": "Formal Logic Processing",
            "problems": [
                "A → B",
                "A ∧ B", 
                "A ∨ B",
                "(A ∧ B) ∨ (¬A ∧ C)"
            ]
        },
        {
            "title": "Conditional Logic Analysis",
            "problems": [
                "If A then B",
                "If it rains, the ground is wet",
                "If A implies B, and B implies C, does A imply C?"
            ]
        },
        {
            "title": "Complex Logical Expressions",
            "problems": [
                "Prove that (A → B) ∧ (B → C) implies (A → C)",
                "Is P ∨ ¬P always true?",
                "What is the truth value of (P ∧ Q) ∨ (¬P ∧ ¬Q)?"
            ]
        }
    ]
    
    for demo in demo_problems:
        print_section(f"{demo['title'].upper()}")
        
        for problem in demo['problems']:
            # Detect features
            features = detect_logical_keywords(problem)
            
            # Analyze
            result = reasoner.reason(problem)
            
            # Display result
            print_result(problem, result, features)
    
    print_section("SYSTEM CAPABILITIES SUMMARY")
    print("✅ Formal Logic Processing: SymPy integration")
    print("✅ Truth Table Generation: Automated for all expressions")
    print("✅ Feature Detection: Identifies logical patterns")
    print("✅ Confidence Scoring: Quantifies reasoning reliability")
    print("✅ Mode Selection: Intelligent approach selection")
    print("✅ Research-Grade Interface: Clean, professional design")
    
    print_section("ACCESS THE WEB INTERFACE")
    print("🌐 Open your browser and go to: http://localhost:8501")
    print("📱 Clean, minimal interface perfect for demonstrations")
    print("🎓 Research-grade design suitable for academic presentations")
    
    print("\n" + "="*60)
    print("🎉 DUAL MODALITY REASONING AGENT - READY FOR DEMO!")
    print("="*60)

if __name__ == "__main__":
    main()

