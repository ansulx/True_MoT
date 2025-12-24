"""
Logic Reasoning Module for Dual Modality Reasoning Agent
Uses SymPy for symbolic logic and truth table generation
"""

import re
import logging
from typing import Dict, Any, List, Tuple, Optional
from sympy import symbols, Implies, And, Or, Not, Equivalent, satisfiable
from sympy.logic import simplify_logic
from sympy.logic.boolalg import BooleanFunction

logger = logging.getLogger(__name__)

class LogicReasoner:
    """Logic reasoning using SymPy for propositional logic."""
    
    def __init__(self):
        """Initialize the logic reasoner."""
        self.symbol_map = {}
        self.operator_map = {
            'and': And,
            'or': Or,
            'not': Not,
            'implies': Implies,
            'iff': Equivalent,
            'if and only if': Equivalent,
            '→': Implies,
            '∧': And,
            '∨': Or,
            '¬': Not,
            '≡': Equivalent
        }
    
    def reason(self, problem: str) -> Dict[str, Any]:
        """
        Perform logical reasoning on the given problem.
        
        Args:
            problem (str): The problem to analyze
            
        Returns:
            Dict[str, Any]: Logic reasoning result
        """
        try:
            # Try to extract logical statements from the problem
            logical_statement = self._extract_logical_statement(problem)
            
            if logical_statement:
                return self._analyze_logical_statement(logical_statement, problem)
            else:
                # Try to convert natural language to logic
                return self._convert_and_analyze(problem)
                
        except Exception as e:
            logger.error(f"Error in logic reasoning: {e}")
            return {
                'result': f"Error in logic analysis: {str(e)}",
                'truth_table': None,
                'conclusion': "Unable to perform logic analysis",
                'confidence': 0.1,
                'success': False
            }
    
    def _extract_logical_statement(self, problem: str) -> Optional[str]:
        """
        Extract logical statement from the problem text.
        
        Args:
            problem (str): Problem text
            
        Returns:
            Optional[str]: Extracted logical statement or None
        """
        # Look for formal logic symbols
        formal_patterns = [
            r'[A-Z]\s*[→∧∨¬≡]\s*[A-Z]',
            r'\([A-Z]\s*[→∧∨¬≡]\s*[A-Z]\)',
            r'[A-Z]\s*(implies|iff)\s*[A-Z]',
            r'\([A-Z]\s*(implies|iff)\s*[A-Z]\)'
        ]
        
        for pattern in formal_patterns:
            match = re.search(pattern, problem, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _analyze_logical_statement(self, statement: str, original_problem: str) -> Dict[str, Any]:
        """
        Analyze a logical statement using SymPy.
        
        Args:
            statement (str): Logical statement
            original_problem (str): Original problem for context
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            # Parse the statement
            parsed_expr = self._parse_statement(statement)
            
            if parsed_expr is None:
                return {
                    'result': f"Could not parse logical statement: {statement}",
                    'truth_table': None,
                    'conclusion': "Parsing failed",
                    'confidence': 0.2,
                    'success': False
                }
            
            # Generate truth table
            truth_table = self._generate_truth_table(parsed_expr)
            
            # Analyze the statement
            analysis = self._analyze_expression(parsed_expr, original_problem)
            
            return {
                'result': analysis['explanation'],
                'truth_table': truth_table,
                'conclusion': analysis['conclusion'],
                'confidence': analysis['confidence'],
                'success': True,
                'expression': str(parsed_expr)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing logical statement: {e}")
            return {
                'result': f"Error analyzing statement: {str(e)}",
                'truth_table': None,
                'conclusion': "Analysis failed",
                'confidence': 0.1,
                'success': False
            }
    
    def _parse_statement(self, statement: str) -> Optional[BooleanFunction]:
        """
        Parse a logical statement into a SymPy expression.
        
        Args:
            statement (str): Logical statement
            
        Returns:
            Optional[BooleanFunction]: Parsed SymPy expression
        """
        try:
            # Clean the statement
            clean_statement = statement.strip()
            
            # Replace operators with SymPy equivalents
            for op, sympy_op in self.operator_map.items():
                if op in clean_statement.lower():
                    clean_statement = clean_statement.replace(op, sympy_op.__name__)
            
            # Extract variables
            variables = re.findall(r'\b[A-Z]\b', clean_statement)
            unique_vars = list(set(variables))
            
            # Create symbol mapping
            sym_vars = {}
            for var in unique_vars:
                if var not in self.symbol_map:
                    self.symbol_map[var] = symbols(var)
                sym_vars[var] = self.symbol_map[var]
            
            # Simple parsing for basic statements
            if '→' in clean_statement or 'Implies' in clean_statement:
                parts = re.split(r'[→]|Implies', clean_statement)
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    return Implies(self._parse_atom(left), self._parse_atom(right))
            
            elif '∧' in clean_statement or 'And' in clean_statement:
                parts = re.split(r'[∧]|And', clean_statement)
                if len(parts) >= 2:
                    atoms = [self._parse_atom(part.strip()) for part in parts]
                    return And(*atoms)
            
            elif '∨' in clean_statement or 'Or' in clean_statement:
                parts = re.split(r'[∨]|Or', clean_statement)
                if len(parts) >= 2:
                    atoms = [self._parse_atom(part.strip()) for part in parts]
                    return Or(*atoms)
            
            elif '¬' in clean_statement or 'Not' in clean_statement:
                atom_part = clean_statement.replace('¬', '').replace('Not', '').strip()
                return Not(self._parse_atom(atom_part))
            
            # If no operators found, treat as single atom
            return self._parse_atom(clean_statement)
            
        except Exception as e:
            logger.error(f"Error parsing statement: {e}")
            return None
    
    def _parse_atom(self, atom: str) -> Any:
        """
        Parse an atomic proposition.
        
        Args:
            atom (str): Atomic proposition
            
        Returns:
            Any: SymPy symbol or expression
        """
        atom = atom.strip('() ')
        if atom in self.symbol_map:
            return self.symbol_map[atom]
        else:
            # Create new symbol
            symbol = symbols(atom)
            self.symbol_map[atom] = symbol
            return symbol
    
    def _generate_truth_table(self, expression: BooleanFunction) -> List[Dict[str, Any]]:
        """
        Generate truth table for the given expression.
        
        Args:
            expression (BooleanFunction): SymPy boolean expression
            
        Returns:
            List[Dict[str, Any]]: Truth table as list of dictionaries
        """
        try:
            # Get all symbols in the expression
            symbols_list = list(expression.atoms())
            symbols_list.sort(key=str)  # Sort for consistent ordering
            
            if not symbols_list:
                return []
            
            # Generate all possible truth value combinations
            truth_table = []
            num_vars = len(symbols_list)
            
            for i in range(2 ** num_vars):
                # Convert i to binary and create assignment
                binary = format(i, f'0{num_vars}b')
                assignment = {}
                
                for j, symbol in enumerate(symbols_list):
                    assignment[symbol] = binary[j] == '1'
                
                # Evaluate expression with this assignment
                try:
                    result = expression.subs(assignment)
                    if hasattr(result, 'simplify'):
                        result = result.simplify()
                    
                    # Convert result to boolean
                    if result == True:
                        result_value = True
                    elif result == False:
                        result_value = False
                    else:
                        result_value = str(result)
                    
                    # Create row
                    row = {}
                    for symbol in symbols_list:
                        row[str(symbol)] = assignment[symbol]
                    row['Result'] = result_value
                    
                    truth_table.append(row)
                    
                except Exception as e:
                    logger.error(f"Error evaluating expression: {e}")
                    continue
            
            return truth_table
            
        except Exception as e:
            logger.error(f"Error generating truth table: {e}")
            return []
    
    def _analyze_expression(self, expression: BooleanFunction, original_problem: str) -> Dict[str, Any]:
        """
        Analyze a logical expression and provide interpretation.
        
        Args:
            expression (BooleanFunction): SymPy expression
            original_problem (str): Original problem for context
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            explanation = f"Analyzing the logical expression: {expression}\n\n"
            
            # Check if expression is tautology, contradiction, or contingency
            symbols_list = list(expression.atoms())
            
            if symbols_list:
                # Check satisfiability
                if satisfiable(expression):
                    explanation += "The expression is satisfiable (not a contradiction).\n"
                    
                    # Check if it's a tautology by checking if its negation is unsatisfiable
                    if not satisfiable(Not(expression)):
                        explanation += "The expression is a tautology (always true).\n"
                        conclusion = "The statement is always true (tautology)."
                        confidence = 0.9
                    else:
                        explanation += "The expression is a contingency (sometimes true, sometimes false).\n"
                        conclusion = "The statement depends on the truth values of its components."
                        confidence = 0.7
                else:
                    explanation += "The expression is a contradiction (never true).\n"
                    conclusion = "The statement is always false (contradiction)."
                    confidence = 0.9
            else:
                # No variables, constant expression
                if expression == True:
                    explanation += "The expression is always true.\n"
                    conclusion = "The statement is always true."
                    confidence = 1.0
                elif expression == False:
                    explanation += "The expression is always false.\n"
                    conclusion = "The statement is always false."
                    confidence = 1.0
                else:
                    explanation += "The expression has a constant value.\n"
                    conclusion = f"The statement evaluates to: {expression}"
                    confidence = 0.8
            
            # Add context from original problem
            if 'if' in original_problem.lower() and 'then' in original_problem.lower():
                explanation += "\nThis appears to be a conditional statement (if-then).\n"
            
            return {
                'explanation': explanation,
                'conclusion': conclusion,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error analyzing expression: {e}")
            return {
                'explanation': f"Error in analysis: {str(e)}",
                'conclusion': "Analysis failed",
                'confidence': 0.1
            }
    
    def _convert_and_analyze(self, problem: str) -> Dict[str, Any]:
        """
        Convert natural language problem to logical form and analyze.
        
        Args:
            problem (str): Natural language problem
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            # Look for conditional statements
            if 'if' in problem.lower() and 'then' in problem.lower():
                return self._analyze_conditional(problem)
            
            # Look for categorical statements
            if any(word in problem.lower() for word in ['all', 'some', 'every', 'any']):
                return self._analyze_categorical(problem)
            
            # Default analysis
            return {
                'result': f"The problem '{problem}' does not contain clear logical structure that can be analyzed with propositional logic.",
                'truth_table': None,
                'conclusion': "No clear logical structure detected",
                'confidence': 0.3,
                'success': False
            }
            
        except Exception as e:
            logger.error(f"Error in convert and analyze: {e}")
            return {
                'result': f"Error converting problem to logic: {str(e)}",
                'truth_table': None,
                'conclusion': "Conversion failed",
                'confidence': 0.1,
                'success': False
            }
    
    def _analyze_conditional(self, problem: str) -> Dict[str, Any]:
        """
        Analyze conditional statements.
        
        Args:
            problem (str): Problem containing conditional
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            # Extract conditional parts
            if_match = re.search(r'if\s+(.+?)\s+then\s+(.+)', problem.lower())
            if if_match:
                antecedent = if_match.group(1).strip()
                consequent = if_match.group(2).strip()
                
                # Create logical expression
                A = symbols('A')  # Antecedent
                B = symbols('B')  # Consequent
                expression = Implies(A, B)
                
                # Generate truth table
                truth_table = self._generate_truth_table(expression)
                
                explanation = f"Conditional Analysis:\n"
                explanation += f"Antecedent (A): {antecedent}\n"
                explanation += f"Consequent (B): {consequent}\n"
                explanation += f"Logical form: A → B\n\n"
                explanation += "Truth table shows when the conditional is true:\n"
                explanation += "- When A is false, the conditional is always true (vacuous truth)\n"
                explanation += "- When A is true and B is true, the conditional is true\n"
                explanation += "- When A is true and B is false, the conditional is false\n"
                
                return {
                    'result': explanation,
                    'truth_table': truth_table,
                    'conclusion': "This is a conditional statement (if-then). The truth table shows all possible truth value combinations.",
                    'confidence': 0.8,
                    'success': True,
                    'expression': str(expression)
                }
            
            return {
                'result': "Could not extract conditional structure from the problem.",
                'truth_table': None,
                'conclusion': "Conditional structure not found",
                'confidence': 0.3,
                'success': False
            }
            
        except Exception as e:
            logger.error(f"Error analyzing conditional: {e}")
            return {
                'result': f"Error analyzing conditional: {str(e)}",
                'truth_table': None,
                'conclusion': "Conditional analysis failed",
                'confidence': 0.1,
                'success': False
            }
    
    def _analyze_categorical(self, problem: str) -> Dict[str, Any]:
        """
        Analyze categorical statements (basic handling).
        
        Args:
            problem (str): Problem containing categorical statements
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        return {
            'result': f"The problem '{problem}' contains categorical statements (all/some/every). These are typically handled by predicate logic rather than propositional logic.",
            'truth_table': None,
            'conclusion': "Categorical statements require predicate logic analysis",
            'confidence': 0.4,
            'success': False
        }

def get_logic_reasoner() -> LogicReasoner:
    """
    Factory function to create a logic reasoner.
    
    Returns:
        LogicReasoner: Configured reasoner instance
    """
    return LogicReasoner()

