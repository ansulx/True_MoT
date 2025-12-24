"""
Utility functions for the Dual Modality Reasoning Agent
"""

import re
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_logical_keywords(text: str) -> Dict[str, bool]:
    """
    Detect logical keywords in the input text to determine reasoning approach.
    
    Args:
        text (str): Input problem text
        
    Returns:
        Dict[str, bool]: Dictionary indicating presence of logical constructs
    """
    text_lower = text.lower()
    
    # Logical connectives
    logical_connectives = any(keyword in text_lower for keyword in [
        'if', 'then', 'implies', 'therefore', 'thus', 'hence', 'consequently',
        'all', 'some', 'every', 'any', 'none', 'not all', 'some not',
        'and', 'or', 'not', 'but', 'however', 'although', 'unless',
        'only if', 'if and only if', 'necessary', 'sufficient'
    ])
    
    # Quantifiers
    quantifiers = any(keyword in text_lower for keyword in [
        'all', 'some', 'every', 'any', 'none', 'most', 'few', 'many'
    ])
    
    # Conditional statements
    conditionals = any(pattern in text_lower for pattern in [
        'if ', 'when ', 'unless ', 'provided that', 'given that'
    ])
    
    # Formal logic symbols
    formal_logic = any(symbol in text for symbol in [
        '→', '∧', '∨', '¬', '⊃', '≡', '∀', '∃', '⊢', '⊨'
    ])
    
    # Question patterns
    questions = any(pattern in text_lower for pattern in [
        'is ', 'are ', 'can ', 'will ', 'does ', 'do ', 'what ', 'how ',
        'why ', 'which ', 'who ', 'where ', 'when '
    ])
    
    return {
        'logical_connectives': logical_connectives,
        'quantifiers': quantifiers,
        'conditionals': conditionals,
        'formal_logic': formal_logic,
        'questions': questions
    }

def calculate_confidence_score(
    nl_result: str,
    logic_result: str,
    mode_agreement: bool,
    internal_consistency: bool
) -> float:
    """
    Calculate confidence score based on multiple factors.
    
    Args:
        nl_result (str): Natural language reasoning result
        logic_result (str): Logic reasoning result
        mode_agreement (bool): Whether both modes agree
        internal_consistency (bool): Whether internal logic is consistent
        
    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    base_confidence = 0.5
    
    # Mode agreement bonus
    if mode_agreement:
        base_confidence += 0.3
    
    # Internal consistency bonus
    if internal_consistency:
        base_confidence += 0.2
    
    # Penalty for empty or very short results
    if len(nl_result.strip()) < 10:
        base_confidence -= 0.2
    if len(logic_result.strip()) < 5:
        base_confidence -= 0.1
    
    return max(0.0, min(1.0, base_confidence))

def parse_propositional_logic(statement: str) -> Dict[str, Any]:
    """
    Parse propositional logic statement to extract components.
    
    Args:
        statement (str): Logical statement to parse
        
    Returns:
        Dict[str, Any]: Parsed components
    """
    # Extract variables (single letters, typically A-Z)
    variables = re.findall(r'\b[A-Z]\b', statement)
    
    # Check for logical operators
    operators = {
        'implication': '→' in statement or 'implies' in statement.lower(),
        'conjunction': '∧' in statement or 'and' in statement.lower(),
        'disjunction': '∨' in statement or 'or' in statement.lower(),
        'negation': '¬' in statement or 'not' in statement.lower(),
        'biconditional': '≡' in statement or 'iff' in statement.lower()
    }
    
    return {
        'variables': list(set(variables)),
        'operators': operators,
        'complexity': len(variables) + sum(operators.values())
    }

def format_reasoning_output(
    mode_selection: str,
    nl_result: str,
    logic_result: str,
    confidence: float
) -> Dict[str, Any]:
    """
    Format the reasoning output for display.
    
    Args:
        mode_selection (str): Selected reasoning mode
        nl_result (str): Natural language result
        logic_result (str): Logic reasoning result
        confidence (float): Confidence score
        
    Returns:
        Dict[str, Any]: Formatted output
    """
    return {
        'mode': mode_selection,
        'natural_language': nl_result,
        'logic_reasoning': logic_result,
        'confidence': confidence,
        'combined_result': combine_results(nl_result, logic_result, mode_selection)
    }

def combine_results(nl_result: str, logic_result: str, mode: str) -> str:
    """
    Combine results from different reasoning modes.
    
    Args:
        nl_result (str): Natural language result
        logic_result (str): Logic reasoning result
        mode (str): Reasoning mode used
        
    Returns:
        str: Combined result
    """
    if mode == "Natural Language Only":
        return nl_result
    elif mode == "Logic Only":
        return logic_result
    elif mode == "Dual Mode":
        if nl_result and logic_result:
            return f"Both reasoning approaches lead to the same conclusion: {nl_result}"
        elif nl_result:
            return nl_result
        elif logic_result:
            return logic_result
        else:
            return "Unable to determine result through either reasoning approach."
    
    return "No valid reasoning mode selected."

def validate_input(text: str) -> Dict[str, Any]:
    """
    Validate input text for processing.
    
    Args:
        text (str): Input text to validate
        
    Returns:
        Dict[str, Any]: Validation result
    """
    if not text or len(text.strip()) < 5:
        return {
            'valid': False,
            'error': 'Input too short. Please provide a more detailed problem.'
        }
    
    if len(text) > 2000:
        return {
            'valid': False,
            'error': 'Input too long. Please limit to 2000 characters.'
        }
    
    return {'valid': True, 'error': None}

