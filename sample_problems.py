"""
Sample Problems for Dual Modality Reasoning Agent
Collection of test problems for different reasoning types
"""

# Sample problems organized by category and difficulty
SAMPLE_PROBLEMS = {
    'conditional': [
        {
            'problem': "If it rains, the ground is wet. It's raining. Is the ground wet?",
            'difficulty': 'easy',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'yes'
        },
        {
            'problem': "If John studies, he passes. John studied. What happened?",
            'difficulty': 'easy',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'passed'
        },
        {
            'problem': "If the weather is nice, we go hiking. We didn't go hiking. What can we conclude?",
            'difficulty': 'medium',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'weather not nice'
        },
        {
            'problem': "If A implies B, and B implies C, does A imply C?",
            'difficulty': 'medium',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'yes'
        },
        {
            'problem': "If all dogs are animals and all animals need food, do all dogs need food?",
            'difficulty': 'easy',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'yes'
        }
    ],
    
    'categorical': [
        {
            'problem': "All birds can fly. Penguins are birds. Can penguins fly?",
            'difficulty': 'medium',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'no'
        },
        {
            'problem': "All humans are mortal. Socrates is human. Is Socrates mortal?",
            'difficulty': 'easy',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'yes'
        },
        {
            'problem': "Some students are athletes. All athletes are healthy. Are some students healthy?",
            'difficulty': 'hard',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'yes'
        },
        {
            'problem': "No cats are dogs. All dogs are mammals. Are any cats mammals?",
            'difficulty': 'medium',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'yes'
        },
        {
            'problem': "All roses are flowers. Some flowers are red. Are some roses red?",
            'difficulty': 'medium',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'possibly'
        }
    ],
    
    'formal_logic': [
        {
            'problem': "Prove that (A → B) ∧ (B → C) implies (A → C)",
            'difficulty': 'hard',
            'expected_mode': 'Logic Only',
            'expected_answer': 'true'
        },
        {
            'problem': "Is the statement 'P ∧ ¬P' always true or always false?",
            'difficulty': 'medium',
            'expected_mode': 'Logic Only',
            'expected_answer': 'false'
        },
        {
            'problem': "What is the truth value of (P ∨ Q) ∧ (¬P ∨ R) when P=True, Q=False, R=True?",
            'difficulty': 'medium',
            'expected_mode': 'Logic Only',
            'expected_answer': 'true'
        },
        {
            'problem': "Is (A → B) equivalent to (¬B → ¬A)?",
            'difficulty': 'hard',
            'expected_mode': 'Logic Only',
            'expected_answer': 'yes'
        },
        {
            'problem': "What is the truth value of P ∨ ¬P?",
            'difficulty': 'easy',
            'expected_mode': 'Logic Only',
            'expected_answer': 'true'
        },
        {
            'problem': "Is the statement '(P ∧ Q) ∨ (¬P ∧ ¬Q)' always true?",
            'difficulty': 'medium',
            'expected_mode': 'Logic Only',
            'expected_answer': 'no'
        }
    ],
    
    'mixed_reasoning': [
        {
            'problem': "If it's sunny, we go to the beach. If it's rainy, we stay home. It's neither sunny nor rainy. What do we do?",
            'difficulty': 'medium',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'unclear'
        },
        {
            'problem': "All mathematicians are logical. Some philosophers are mathematicians. Are some philosophers logical?",
            'difficulty': 'medium',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'yes'
        },
        {
            'problem': "If A implies B, and A is true, what can we say about B?",
            'difficulty': 'easy',
            'expected_mode': 'Dual Mode',
            'expected_answer': 'true'
        },
        {
            'problem': "Prove that ¬(P ∧ Q) is equivalent to (¬P ∨ ¬Q)",
            'difficulty': 'hard',
            'expected_mode': 'Logic Only',
            'expected_answer': 'true'
        },
        {
            'problem': "If all swans are white, and this is a swan, what color is it?",
            'difficulty': 'easy',
            'expected_mode': 'Natural Language Only',
            'expected_answer': 'white'
        }
    ]
}

def get_random_problem(category: str = None, difficulty: str = None):
    """
    Get a random problem from the sample problems.
    
    Args:
        category (str, optional): Problem category to filter by
        difficulty (str, optional): Difficulty level to filter by
        
    Returns:
        dict: Random problem
    """
    import random
    
    if category and category in SAMPLE_PROBLEMS:
        problems = SAMPLE_PROBLEMS[category]
    else:
        # Get all problems
        problems = []
        for cat_problems in SAMPLE_PROBLEMS.values():
            problems.extend(cat_problems)
    
    if difficulty:
        problems = [p for p in problems if p['difficulty'] == difficulty]
    
    if problems:
        return random.choice(problems)
    else:
        return None

def get_problems_by_category(category: str):
    """
    Get all problems from a specific category.
    
    Args:
        category (str): Problem category
        
    Returns:
        list: List of problems in the category
    """
    return SAMPLE_PROBLEMS.get(category, [])

def get_all_problems():
    """
    Get all sample problems.
    
    Returns:
        list: List of all problems
    """
    all_problems = []
    for problems in SAMPLE_PROBLEMS.values():
        all_problems.extend(problems)
    return all_problems

def get_problem_statistics():
    """
    Get statistics about the sample problems.
    
    Returns:
        dict: Problem statistics
    """
    stats = {}
    
    for category, problems in SAMPLE_PROBLEMS.items():
        stats[category] = {
            'count': len(problems),
            'difficulties': {}
        }
        
        for problem in problems:
            difficulty = problem['difficulty']
            if difficulty not in stats[category]['difficulties']:
                stats[category]['difficulties'][difficulty] = 0
            stats[category]['difficulties'][difficulty] += 1
    
    return stats

if __name__ == "__main__":
    # Display sample problems and statistics
    print("Sample Problems for Dual Modality Reasoning Agent")
    print("=" * 50)
    
    stats = get_problem_statistics()
    print(f"\nProblem Statistics:")
    for category, info in stats.items():
        print(f"\n{category.upper()}:")
        print(f"  Total problems: {info['count']}")
        for difficulty, count in info['difficulties'].items():
            print(f"  {difficulty}: {count}")
    
    print(f"\nTotal problems: {sum(info['count'] for info in stats.values())}")
    
    # Show a few example problems
    print(f"\nExample Problems:")
    for category in ['conditional', 'formal_logic']:
        problems = get_problems_by_category(category)
        if problems:
            print(f"\n{category.upper()}:")
            for problem in problems[:2]:  # Show first 2
                print(f"  - {problem['problem']}")
                print(f"    Difficulty: {problem['difficulty']}")
                print(f"    Expected mode: {problem['expected_mode']}")
                print(f"    Expected answer: {problem['expected_answer']}")
                print()

