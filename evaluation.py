"""
Evaluation System for Dual Modality Reasoning Agent
Tests the agent on predefined problems and generates performance metrics
"""

import time
import pandas as pd
import logging
from typing import Dict, Any, List, Tuple
from integration import get_dual_modality_controller
from natural_language import get_natural_language_reasoner
from logic_reasoning import get_logic_reasoner

logger = logging.getLogger(__name__)

class EvaluationSuite:
    """Evaluation suite for testing the dual modality reasoning agent."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the evaluation suite.
        
        Args:
            api_key (str, optional): Google AI API key for testing
        """
        self.controller = get_dual_modality_controller(api_key)
        self.nl_reasoner = get_natural_language_reasoner(api_key)
        self.logic_reasoner = get_logic_reasoner()
        
        # Test problems with expected answers
        self.test_problems = [
            {
                'id': 1,
                'problem': "If it rains, the ground is wet. It's raining. Is the ground wet?",
                'expected_mode': 'Dual Mode',
                'expected_answer': 'yes',
                'category': 'conditional',
                'difficulty': 'easy'
            },
            {
                'id': 2,
                'problem': "All birds can fly. Penguins are birds. Can penguins fly?",
                'expected_mode': 'Natural Language Only',
                'expected_answer': 'no',
                'category': 'categorical',
                'difficulty': 'medium'
            },
            {
                'id': 3,
                'problem': "Prove that (A → B) ∧ (B → C) implies (A → C)",
                'expected_mode': 'Logic Only',
                'expected_answer': 'true',
                'category': 'formal_logic',
                'difficulty': 'hard'
            },
            {
                'id': 4,
                'problem': "If John studies, he passes. John studied. What happened?",
                'expected_mode': 'Dual Mode',
                'expected_answer': 'passed',
                'category': 'conditional',
                'difficulty': 'easy'
            },
            {
                'id': 5,
                'problem': "Is the statement 'P ∧ ¬P' always true or always false?",
                'expected_mode': 'Logic Only',
                'expected_answer': 'false',
                'category': 'formal_logic',
                'difficulty': 'medium'
            },
            {
                'id': 6,
                'problem': "If A implies B, and B implies C, does A imply C?",
                'expected_mode': 'Dual Mode',
                'expected_answer': 'yes',
                'category': 'conditional',
                'difficulty': 'medium'
            },
            {
                'id': 7,
                'problem': "All humans are mortal. Socrates is human. Is Socrates mortal?",
                'expected_mode': 'Natural Language Only',
                'expected_answer': 'yes',
                'category': 'categorical',
                'difficulty': 'easy'
            },
            {
                'id': 8,
                'problem': "What is the truth value of (P ∨ Q) ∧ (¬P ∨ R) when P=True, Q=False, R=True?",
                'expected_mode': 'Logic Only',
                'expected_answer': 'true',
                'category': 'formal_logic',
                'difficulty': 'medium'
            },
            {
                'id': 9,
                'problem': "If the weather is nice, we go hiking. We didn't go hiking. What can we conclude?",
                'expected_mode': 'Dual Mode',
                'expected_answer': 'weather not nice',
                'category': 'conditional',
                'difficulty': 'medium'
            },
            {
                'id': 10,
                'problem': "Some students are athletes. All athletes are healthy. Are some students healthy?",
                'expected_mode': 'Natural Language Only',
                'expected_answer': 'yes',
                'category': 'categorical',
                'difficulty': 'hard'
            }
        ]
    
    def run_full_evaluation(self) -> Dict[str, Any]:
        """
        Run the complete evaluation suite.
        
        Returns:
            Dict[str, Any]: Complete evaluation results
        """
        logger.info("Starting full evaluation suite...")
        
        results = []
        total_start_time = time.time()
        
        # Test each problem
        for test_case in self.test_problems:
            logger.info(f"Testing problem {test_case['id']}: {test_case['problem'][:50]}...")
            
            # Test dual modality
            dual_result = self._test_dual_modality(test_case)
            
            # Test natural language only
            nl_result = self._test_natural_language_only(test_case)
            
            # Test logic only
            logic_result = self._test_logic_only(test_case)
            
            # Combine results
            result = {
                'problem_id': test_case['id'],
                'problem': test_case['problem'],
                'category': test_case['category'],
                'difficulty': test_case['difficulty'],
                'expected_mode': test_case['expected_mode'],
                'expected_answer': test_case['expected_answer'],
                'dual_modality': dual_result,
                'natural_language_only': nl_result,
                'logic_only': logic_result
            }
            
            results.append(result)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        total_time = time.time() - total_start_time
        
        # Generate summary statistics
        summary = self._generate_summary(results, total_time)
        
        return {
            'summary': summary,
            'detailed_results': results,
            'total_time': total_time
        }
    
    def _test_dual_modality(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Test dual modality reasoning on a problem."""
        start_time = time.time()
        
        try:
            result = self.controller.process_problem(test_case['problem'])
            
            processing_time = time.time() - start_time
            
            # Evaluate results
            mode_correct = result.get('mode_selection', {}).get('mode') == test_case['expected_mode']
            success = result.get('success', False)
            confidence = result.get('confidence', 0.0)
            
            # Simple answer correctness check
            answer_correct = self._check_answer_correctness(
                result.get('conclusion', ''),
                test_case['expected_answer']
            )
            
            return {
                'success': success,
                'processing_time': processing_time,
                'confidence': confidence,
                'mode_correct': mode_correct,
                'answer_correct': answer_correct,
                'conclusion': result.get('conclusion', ''),
                'mode_selected': result.get('mode_selection', {}).get('mode', 'Unknown')
            }
            
        except Exception as e:
            logger.error(f"Error testing dual modality: {e}")
            return {
                'success': False,
                'processing_time': time.time() - start_time,
                'confidence': 0.0,
                'mode_correct': False,
                'answer_correct': False,
                'conclusion': f"Error: {str(e)}",
                'mode_selected': 'Error'
            }
    
    def _test_natural_language_only(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Test natural language reasoning only on a problem."""
        start_time = time.time()
        
        try:
            result = self.nl_reasoner.reason(test_case['problem'], 'general')
            
            processing_time = time.time() - start_time
            
            answer_correct = self._check_answer_correctness(
                result.get('conclusion', ''),
                test_case['expected_answer']
            )
            
            return {
                'success': result.get('success', False),
                'processing_time': processing_time,
                'confidence': result.get('confidence', 0.0),
                'answer_correct': answer_correct,
                'conclusion': result.get('conclusion', '')
            }
            
        except Exception as e:
            logger.error(f"Error testing natural language: {e}")
            return {
                'success': False,
                'processing_time': time.time() - start_time,
                'confidence': 0.0,
                'answer_correct': False,
                'conclusion': f"Error: {str(e)}"
            }
    
    def _test_logic_only(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Test logic reasoning only on a problem."""
        start_time = time.time()
        
        try:
            result = self.logic_reasoner.reason(test_case['problem'])
            
            processing_time = time.time() - start_time
            
            answer_correct = self._check_answer_correctness(
                result.get('conclusion', ''),
                test_case['expected_answer']
            )
            
            return {
                'success': result.get('success', False),
                'processing_time': processing_time,
                'confidence': result.get('confidence', 0.0),
                'answer_correct': answer_correct,
                'conclusion': result.get('conclusion', '')
            }
            
        except Exception as e:
            logger.error(f"Error testing logic reasoning: {e}")
            return {
                'success': False,
                'processing_time': time.time() - start_time,
                'confidence': 0.0,
                'answer_correct': False,
                'conclusion': f"Error: {str(e)}"
            }
    
    def _check_answer_correctness(self, actual: str, expected: str) -> bool:
        """
        Check if the actual answer matches the expected answer.
        
        Args:
            actual (str): Actual answer from the system
            expected (str): Expected answer
            
        Returns:
            bool: True if answers match, False otherwise
        """
        if not actual or not expected:
            return False
        
        actual_lower = actual.lower()
        expected_lower = expected.lower()
        
        # Direct match
        if expected_lower in actual_lower:
            return True
        
        # Check for semantic equivalents
        equivalents = {
            'yes': ['true', 'correct', 'affirmative', 'positive'],
            'no': ['false', 'incorrect', 'negative'],
            'true': ['yes', 'correct', 'affirmative'],
            'false': ['no', 'incorrect', 'negative'],
            'passed': ['pass', 'success', 'successful'],
            'weather not nice': ['not nice', 'bad weather', 'poor weather']
        }
        
        for key, values in equivalents.items():
            if expected_lower == key:
                return any(val in actual_lower for val in values)
            elif expected_lower in values:
                return key in actual_lower or any(val in actual_lower for val in values)
        
        return False
    
    def _generate_summary(self, results: List[Dict[str, Any]], total_time: float) -> Dict[str, Any]:
        """
        Generate summary statistics from evaluation results.
        
        Args:
            results (List[Dict[str, Any]]): Detailed results
            total_time (float): Total evaluation time
            
        Returns:
            Dict[str, Any]: Summary statistics
        """
        total_problems = len(results)
        
        # Dual modality statistics
        dual_success = sum(1 for r in results if r['dual_modality']['success'])
        dual_answers_correct = sum(1 for r in results if r['dual_modality']['answer_correct'])
        dual_modes_correct = sum(1 for r in results if r['dual_modality']['mode_correct'])
        dual_avg_confidence = sum(r['dual_modality']['confidence'] for r in results) / total_problems
        dual_avg_time = sum(r['dual_modality']['processing_time'] for r in results) / total_problems
        
        # Natural language statistics
        nl_success = sum(1 for r in results if r['natural_language_only']['success'])
        nl_answers_correct = sum(1 for r in results if r['natural_language_only']['answer_correct'])
        nl_avg_confidence = sum(r['natural_language_only']['confidence'] for r in results) / total_problems
        nl_avg_time = sum(r['natural_language_only']['processing_time'] for r in results) / total_problems
        
        # Logic statistics
        logic_success = sum(1 for r in results if r['logic_only']['success'])
        logic_answers_correct = sum(1 for r in results if r['logic_only']['answer_correct'])
        logic_avg_confidence = sum(r['logic_only']['confidence'] for r in results) / total_problems
        logic_avg_time = sum(r['logic_only']['processing_time'] for r in results) / total_problems
        
        # Category-wise performance
        categories = {}
        for result in results:
            category = result['category']
            if category not in categories:
                categories[category] = {'total': 0, 'dual_correct': 0, 'nl_correct': 0, 'logic_correct': 0}
            
            categories[category]['total'] += 1
            if result['dual_modality']['answer_correct']:
                categories[category]['dual_correct'] += 1
            if result['natural_language_only']['answer_correct']:
                categories[category]['nl_correct'] += 1
            if result['logic_only']['answer_correct']:
                categories[category]['logic_correct'] += 1
        
        # Difficulty-wise performance
        difficulties = {}
        for result in results:
            difficulty = result['difficulty']
            if difficulty not in difficulties:
                difficulties[difficulty] = {'total': 0, 'dual_correct': 0, 'nl_correct': 0, 'logic_correct': 0}
            
            difficulties[difficulty]['total'] += 1
            if result['dual_modality']['answer_correct']:
                difficulties[difficulty]['dual_correct'] += 1
            if result['natural_language_only']['answer_correct']:
                difficulties[difficulty]['nl_correct'] += 1
            if result['logic_only']['answer_correct']:
                difficulties[difficulty]['logic_correct'] += 1
        
        return {
            'total_problems': total_problems,
            'total_time': total_time,
            'dual_modality': {
                'success_rate': dual_success / total_problems,
                'accuracy': dual_answers_correct / total_problems,
                'mode_selection_accuracy': dual_modes_correct / total_problems,
                'avg_confidence': dual_avg_confidence,
                'avg_processing_time': dual_avg_time
            },
            'natural_language': {
                'success_rate': nl_success / total_problems,
                'accuracy': nl_answers_correct / total_problems,
                'avg_confidence': nl_avg_confidence,
                'avg_processing_time': nl_avg_time
            },
            'logic_reasoning': {
                'success_rate': logic_success / total_problems,
                'accuracy': logic_answers_correct / total_problems,
                'avg_confidence': logic_avg_confidence,
                'avg_processing_time': logic_avg_time
            },
            'category_performance': categories,
            'difficulty_performance': difficulties
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Save evaluation results to CSV files.
        
        Args:
            results (Dict[str, Any]): Evaluation results
            filename (str, optional): Base filename for output files
            
        Returns:
            str: Path to saved files
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}"
        
        # Save detailed results
        detailed_data = []
        for result in results['detailed_results']:
            row = {
                'problem_id': result['problem_id'],
                'problem': result['problem'],
                'category': result['category'],
                'difficulty': result['difficulty'],
                'expected_mode': result['expected_mode'],
                'expected_answer': result['expected_answer'],
                'dual_success': result['dual_modality']['success'],
                'dual_answer_correct': result['dual_modality']['answer_correct'],
                'dual_mode_correct': result['dual_modality']['mode_correct'],
                'dual_confidence': result['dual_modality']['confidence'],
                'dual_time': result['dual_modality']['processing_time'],
                'dual_conclusion': result['dual_modality']['conclusion'],
                'dual_mode_selected': result['dual_modality']['mode_selected'],
                'nl_success': result['natural_language_only']['success'],
                'nl_answer_correct': result['natural_language_only']['answer_correct'],
                'nl_confidence': result['natural_language_only']['confidence'],
                'nl_time': result['natural_language_only']['processing_time'],
                'nl_conclusion': result['natural_language_only']['conclusion'],
                'logic_success': result['logic_only']['success'],
                'logic_answer_correct': result['logic_only']['answer_correct'],
                'logic_confidence': result['logic_only']['confidence'],
                'logic_time': result['logic_only']['processing_time'],
                'logic_conclusion': result['logic_only']['conclusion']
            }
            detailed_data.append(row)
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_filename = f"{filename}_detailed.csv"
        detailed_df.to_csv(detailed_filename, index=False)
        
        # Save summary statistics
        summary_data = []
        summary = results['summary']
        
        # Overall statistics
        summary_data.append({
            'metric': 'dual_modality_accuracy',
            'value': summary['dual_modality']['accuracy'],
            'category': 'overall'
        })
        summary_data.append({
            'metric': 'dual_modality_mode_accuracy',
            'value': summary['dual_modality']['mode_selection_accuracy'],
            'category': 'overall'
        })
        summary_data.append({
            'metric': 'natural_language_accuracy',
            'value': summary['natural_language']['accuracy'],
            'category': 'overall'
        })
        summary_data.append({
            'metric': 'logic_reasoning_accuracy',
            'value': summary['logic_reasoning']['accuracy'],
            'category': 'overall'
        })
        
        # Category-wise statistics
        for category, perf in summary['category_performance'].items():
            if perf['total'] > 0:
                summary_data.append({
                    'metric': 'dual_modality_accuracy',
                    'value': perf['dual_correct'] / perf['total'],
                    'category': category
                })
                summary_data.append({
                    'metric': 'natural_language_accuracy',
                    'value': perf['nl_correct'] / perf['total'],
                    'category': category
                })
                summary_data.append({
                    'metric': 'logic_reasoning_accuracy',
                    'value': perf['logic_correct'] / perf['total'],
                    'category': category
                })
        
        summary_df = pd.DataFrame(summary_data)
        summary_filename = f"{filename}_summary.csv"
        summary_df.to_csv(summary_filename, index=False)
        
        logger.info(f"Results saved to {detailed_filename} and {summary_filename}")
        return f"{filename}_*.csv"

def run_evaluation(api_key: str = None) -> Dict[str, Any]:
    """
    Run the complete evaluation suite.
    
    Args:
        api_key (str, optional): Google AI API key
        
    Returns:
        Dict[str, Any]: Evaluation results
    """
    evaluator = EvaluationSuite(api_key)
    results = evaluator.run_full_evaluation()
    
    # Save results
    filename = evaluator.save_results(results)
    results['saved_files'] = filename
    
    return results

if __name__ == "__main__":
    # Run evaluation if executed directly
    import os
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if api_key:
        print("Running evaluation suite...")
        results = run_evaluation(api_key)
        
        print(f"\nEvaluation Summary:")
        print(f"Total problems: {results['summary']['total_problems']}")
        print(f"Total time: {results['summary']['total_time']:.2f} seconds")
        print(f"Dual modality accuracy: {results['summary']['dual_modality']['accuracy']:.2f}")
        print(f"Natural language accuracy: {results['summary']['natural_language']['accuracy']:.2f}")
        print(f"Logic reasoning accuracy: {results['summary']['logic_reasoning']['accuracy']:.2f}")
        print(f"Results saved to: {results['saved_files']}")
    else:
        print("Please set GOOGLE_AI_API_KEY environment variable to run evaluation")

