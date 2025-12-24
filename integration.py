"""
Integration Controller for Dual Modality Reasoning Agent
Coordinates between natural language and logic reasoning modules
"""

import logging
from typing import Dict, Any, Optional, Tuple
from natural_language import NaturalLanguageReasoner
from logic_reasoning import LogicReasoner
from utils import (
    detect_logical_keywords, 
    calculate_confidence_score, 
    format_reasoning_output,
    validate_input
)

logger = logging.getLogger(__name__)

class DualModalityController:
    """Main controller that integrates natural language and logic reasoning."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the dual modality controller.
        
        Args:
            api_key (str, optional): Google AI API key for natural language reasoning
        """
        self.nl_reasoner = NaturalLanguageReasoner(api_key)
        self.logic_reasoner = LogicReasoner()
        
        # Mode selection thresholds
        self.thresholds = {
            'logic_strong': 0.8,    # High confidence for logic-only mode
            'dual_mode': 0.6,       # Medium confidence for dual mode
            'nl_only': 0.3          # Low confidence for NL-only mode
        }
    
    def process_problem(self, problem: str) -> Dict[str, Any]:
        """
        Process a problem using the dual modality reasoning system.
        
        Args:
            problem (str): The problem to analyze
            
        Returns:
            Dict[str, Any]: Complete reasoning result
        """
        # Validate input
        validation = validate_input(problem)
        if not validation['valid']:
            return {
                'error': validation['error'],
                'success': False
            }
        
        try:
            # Analyze problem to determine reasoning approach
            mode_selection = self._select_reasoning_mode(problem)
            
            # Execute reasoning based on selected mode
            if mode_selection['mode'] == 'Natural Language Only':
                result = self._process_nl_only(problem)
            elif mode_selection['mode'] == 'Logic Only':
                result = self._process_logic_only(problem)
            else:  # Dual Mode
                result = self._process_dual_mode(problem)
            
            # Add mode selection information
            result['mode_selection'] = mode_selection
            result['success'] = True
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing problem: {e}")
            return {
                'error': f"Error processing problem: {str(e)}",
                'success': False
            }
    
    def _select_reasoning_mode(self, problem: str) -> Dict[str, Any]:
        """
        Select the appropriate reasoning mode based on problem analysis.
        
        Args:
            problem (str): Problem to analyze
            
        Returns:
            Dict[str, Any]: Mode selection with explanation
        """
        # Detect logical keywords and patterns
        logical_features = detect_logical_keywords(problem)
        
        # Calculate mode confidence scores
        logic_confidence = self._calculate_logic_confidence(logical_features, problem)
        nl_confidence = self._calculate_nl_confidence(logical_features, problem)
        
        # Determine mode based on confidence scores and thresholds
        if logic_confidence >= self.thresholds['logic_strong']:
            mode = 'Logic Only'
            explanation = "High confidence in logical structure detected. Using formal logic reasoning."
        elif (logic_confidence >= self.thresholds['dual_mode'] and 
              nl_confidence >= self.thresholds['dual_mode']):
            mode = 'Dual Mode'
            explanation = "Both logical structure and natural language patterns detected. Using both reasoning approaches."
        elif logic_confidence >= self.thresholds['nl_only']:
            mode = 'Dual Mode'
            explanation = "Some logical elements detected. Using dual mode for comprehensive analysis."
        else:
            mode = 'Natural Language Only'
            explanation = "No clear logical structure detected. Using natural language reasoning."
        
        return {
            'mode': mode,
            'explanation': explanation,
            'logic_confidence': logic_confidence,
            'nl_confidence': nl_confidence,
            'features': logical_features
        }
    
    def _calculate_logic_confidence(self, features: Dict[str, bool], problem: str) -> float:
        """
        Calculate confidence score for using logic reasoning.
        
        Args:
            features (Dict[str, bool]): Detected logical features
            problem (str): Problem text
            
        Returns:
            float: Logic confidence score
        """
        confidence = 0.0
        
        # Formal logic symbols
        if features['formal_logic']:
            confidence += 0.4
        
        # Logical connectives
        if features['logical_connectives']:
            confidence += 0.3
        
        # Conditional statements
        if features['conditionals']:
            confidence += 0.2
        
        # Quantifiers (lower weight for propositional logic)
        if features['quantifiers']:
            confidence += 0.1
        
        # Check for specific logical patterns
        if 'prove' in problem.lower() or 'show' in problem.lower():
            confidence += 0.2
        
        if any(symbol in problem for symbol in ['→', '∧', '∨', '¬', '≡']):
            confidence += 0.3
        
        return min(1.0, confidence)
    
    def _calculate_nl_confidence(self, features: Dict[str, bool], problem: str) -> float:
        """
        Calculate confidence score for using natural language reasoning.
        
        Args:
            features (Dict[str, bool]): Detected logical features
            problem (str): Problem text
            
        Returns:
            float: Natural language confidence score
        """
        confidence = 0.5  # Base confidence for NL reasoning
        
        # Questions indicate NL reasoning is appropriate
        if features['questions']:
            confidence += 0.3
        
        # Complex language patterns
        if len(problem.split()) > 10:
            confidence += 0.1
        
        # Narrative elements
        if any(word in problem.lower() for word in ['john', 'mary', 'student', 'teacher', 'person']):
            confidence += 0.2
        
        # Decrease confidence if too much formal logic
        if features['formal_logic']:
            confidence -= 0.2
        
        return max(0.0, min(1.0, confidence))
    
    def _process_nl_only(self, problem: str) -> Dict[str, Any]:
        """
        Process problem using only natural language reasoning.
        
        Args:
            problem (str): Problem to analyze
            
        Returns:
            Dict[str, Any]: Natural language reasoning result
        """
        nl_result = self.nl_reasoner.reason(problem, 'general')
        
        return {
            'mode': 'Natural Language Only',
            'natural_language': nl_result,
            'logic_reasoning': None,
            'combined_result': nl_result['result'],
            'confidence': nl_result['confidence'],
            'conclusion': nl_result['conclusion']
        }
    
    def _process_logic_only(self, problem: str) -> Dict[str, Any]:
        """
        Process problem using only logic reasoning.
        
        Args:
            problem (str): Problem to analyze
            
        Returns:
            Dict[str, Any]: Logic reasoning result
        """
        logic_result = self.logic_reasoner.reason(problem)
        
        return {
            'mode': 'Logic Only',
            'natural_language': None,
            'logic_reasoning': logic_result,
            'combined_result': logic_result['result'],
            'confidence': logic_result['confidence'],
            'conclusion': logic_result['conclusion']
        }
    
    def _process_dual_mode(self, problem: str) -> Dict[str, Any]:
        """
        Process problem using both natural language and logic reasoning.
        
        Args:
            problem (str): Problem to analyze
            
        Returns:
            Dict[str, Any]: Combined reasoning result
        """
        # Run both reasoning modes
        nl_result = self.nl_reasoner.reason(problem, 'logical')
        logic_result = self.logic_reasoner.reason(problem)
        
        # Check for agreement between modes
        mode_agreement = self._check_mode_agreement(nl_result, logic_result)
        
        # Calculate combined confidence
        combined_confidence = calculate_confidence_score(
            nl_result['result'] if nl_result['success'] else '',
            logic_result['result'] if logic_result['success'] else '',
            mode_agreement,
            nl_result['success'] and logic_result['success']
        )
        
        # Generate combined result
        combined_result = self._combine_results(nl_result, logic_result, mode_agreement)
        
        return {
            'mode': 'Dual Mode',
            'natural_language': nl_result,
            'logic_reasoning': logic_result,
            'combined_result': combined_result,
            'confidence': combined_confidence,
            'conclusion': self._generate_dual_conclusion(nl_result, logic_result, mode_agreement),
            'mode_agreement': mode_agreement
        }
    
    def _check_mode_agreement(self, nl_result: Dict[str, Any], logic_result: Dict[str, Any]) -> bool:
        """
        Check if the two reasoning modes agree on the conclusion.
        
        Args:
            nl_result (Dict[str, Any]): Natural language result
            logic_result (Dict[str, Any]): Logic reasoning result
            
        Returns:
            bool: True if modes agree, False otherwise
        """
        if not nl_result['success'] or not logic_result['success']:
            return False
        
        nl_conclusion = nl_result['conclusion'].lower()
        logic_conclusion = logic_result['conclusion'].lower()
        
        # Simple agreement check based on keywords
        agreement_indicators = ['true', 'false', 'yes', 'no', 'correct', 'incorrect']
        
        nl_has_indicator = any(indicator in nl_conclusion for indicator in agreement_indicators)
        logic_has_indicator = any(indicator in logic_conclusion for indicator in agreement_indicators)
        
        if nl_has_indicator and logic_has_indicator:
            # Check if they have the same polarity
            positive_indicators = ['true', 'yes', 'correct']
            nl_positive = any(indicator in nl_conclusion for indicator in positive_indicators)
            logic_positive = any(indicator in logic_conclusion for indicator in positive_indicators)
            return nl_positive == logic_positive
        
        # If no clear indicators, assume agreement if both succeeded
        return True
    
    def _combine_results(self, nl_result: Dict[str, Any], logic_result: Dict[str, Any], agreement: bool) -> str:
        """
        Combine results from both reasoning modes.
        
        Args:
            nl_result (Dict[str, Any]): Natural language result
            logic_result (Dict[str, Any]): Logic reasoning result
            agreement (bool): Whether modes agree
            
        Returns:
            str: Combined result text
        """
        combined = "Dual Modality Analysis:\n\n"
        
        # Natural language reasoning section
        if nl_result['success']:
            combined += "Natural Language Reasoning:\n"
            combined += nl_result['result'] + "\n\n"
        
        # Logic reasoning section
        if logic_result['success']:
            combined += "Logic Reasoning:\n"
            combined += logic_result['result'] + "\n\n"
        
        # Agreement analysis
        if agreement:
            combined += "The two reasoning approaches agree on the conclusion.\n"
        else:
            combined += "The two reasoning approaches show different perspectives.\n"
        
        # Final conclusion
        if nl_result['success'] and logic_result['success']:
            if agreement:
                combined += f"\nFinal Conclusion: {nl_result['conclusion']}"
            else:
                combined += f"\nNatural Language Conclusion: {nl_result['conclusion']}\n"
                combined += f"Logic Conclusion: {logic_result['conclusion']}"
        elif nl_result['success']:
            combined += f"\nFinal Conclusion: {nl_result['conclusion']}"
        elif logic_result['success']:
            combined += f"\nFinal Conclusion: {logic_result['conclusion']}"
        else:
            combined += "\nUnable to reach a definitive conclusion through either reasoning approach."
        
        return combined
    
    def _generate_dual_conclusion(self, nl_result: Dict[str, Any], logic_result: Dict[str, Any], agreement: bool) -> str:
        """
        Generate a conclusion for dual mode reasoning.
        
        Args:
            nl_result (Dict[str, Any]): Natural language result
            logic_result (Dict[str, Any]): Logic reasoning result
            agreement (bool): Whether modes agree
            
        Returns:
            str: Generated conclusion
        """
        if agreement:
            if nl_result['success']:
                return nl_result['conclusion']
            elif logic_result['success']:
                return logic_result['conclusion']
        else:
            return f"Mixed results: NL suggests {nl_result['conclusion'] if nl_result['success'] else 'N/A'}, Logic suggests {logic_result['conclusion'] if logic_result['success'] else 'N/A'}"
        
        return "Unable to determine conclusion"

def get_dual_modality_controller(api_key: Optional[str] = None) -> DualModalityController:
    """
    Factory function to create a dual modality controller.
    
    Args:
        api_key (str, optional): Google AI API key
        
    Returns:
        DualModalityController: Configured controller instance
    """
    return DualModalityController(api_key)

