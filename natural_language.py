"""
Natural Language Reasoning Module for Dual Modality Reasoning Agent
Uses OpenRouter API for chain-of-thought reasoning (with fallback)
"""

import os
import logging
from typing import Dict, Any, Optional
import time
import requests

logger = logging.getLogger(__name__)

class NaturalLanguageReasoner:
    """Natural language reasoning powered by OpenRouter-hosted LLMs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the natural language reasoner.
        
        Args:
            api_key (str, optional): OpenRouter API key. If None, tries to get from environment.
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.model_name = os.getenv('OPENROUTER_MODEL', 'openrouter/auto')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1/chat/completions')
        self.referer = os.getenv('OPENROUTER_REFERER', 'https://openrouter.ai')
        self.app_title = os.getenv('OPENROUTER_APP_NAME', 'Dual-Modality-Reasoning-Agent')
        self.api_available = True if self.api_key else False

        if not self.api_available:
            logger.warning("No OpenRouter API key found. Set OPENROUTER_API_KEY to enable NL reasoning.")
        
        # Reasoning prompts
        self.reasoning_prompts = {
            'logical': """You are a logical reasoning expert. Analyze the following problem step by step:

Problem: {problem}

Please provide:
1. A clear step-by-step logical analysis
2. Identify the logical structure (premises, conclusions, reasoning)
3. State your final answer clearly
4. Explain your reasoning process

Be concise but thorough in your analysis.""",

            'general': """You are a reasoning expert. Analyze the following problem step by step:

Problem: {problem}

Please provide:
1. A clear step-by-step analysis
2. Break down the problem into manageable parts
3. Apply logical reasoning where appropriate
4. State your final answer clearly
5. Explain your reasoning process

Be concise but thorough in your analysis.""",

            'fallback': """Analyze this problem and provide a clear answer with reasoning:

{problem}

Please give a step-by-step explanation and your final conclusion."""
        }
    
    def reason(self, problem: str, reasoning_type: str = 'general') -> Dict[str, Any]:
        """
        Perform natural language reasoning on the given problem.
        
        Args:
            problem (str): The problem to analyze
            reasoning_type (str): Type of reasoning ('logical', 'general', 'fallback')
            
        Returns:
            Dict[str, Any]: Reasoning result with confidence and explanation
        """
        if not self.api_available:
            return self._fallback_reasoning(problem)
        
        try:
            prompt = self.reasoning_prompts.get(reasoning_type, self.reasoning_prompts['fallback'])
            formatted_prompt = prompt.format(problem=problem)
            
            # Generate response with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response_text = self._call_openrouter(formatted_prompt)
                    if response_text:
                        return self._process_response(response_text, reasoning_type)
                    logger.warning(f"Empty response from OpenRouter (attempt {attempt + 1})")
                except Exception as e:
                    logger.error(f"Error calling OpenRouter API (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                    continue
                
                time.sleep(1)
            
            # If all retries failed, use fallback
            return self._fallback_reasoning(problem)
            
        except Exception as e:
            logger.error(f"Error in natural language reasoning: {e}")
            return self._fallback_reasoning(problem)
    
    def _process_response(self, response_text: str, reasoning_type: str) -> Dict[str, Any]:
        """
        Process the response from the LLM.
        
        Args:
            response_text (str): Raw response text
            reasoning_type (str): Type of reasoning used
            
        Returns:
            Dict[str, Any]: Processed result
        """
        # Clean up the response
        cleaned_response = response_text.strip()
        
        # Extract conclusion if possible
        conclusion = self._extract_conclusion(cleaned_response)
        
        # Calculate confidence based on response quality
        confidence = self._calculate_confidence(cleaned_response, reasoning_type)
        
        return {
            'result': cleaned_response,
            'conclusion': conclusion,
            'confidence': confidence,
            'reasoning_type': reasoning_type,
            'success': True
        }
    
    def _extract_conclusion(self, response: str) -> str:
        """
        Extract the main conclusion from the response.
        
        Args:
            response (str): Full response text
            
        Returns:
            str: Extracted conclusion
        """
        # Look for conclusion indicators
        conclusion_indicators = [
            'conclusion:', 'final answer:', 'answer:', 'result:',
            'therefore:', 'thus:', 'hence:', 'in conclusion:'
        ]
        
        response_lower = response.lower()
        for indicator in conclusion_indicators:
            if indicator in response_lower:
                # Find the sentence after the indicator
                start_idx = response_lower.find(indicator) + len(indicator)
                remaining = response[start_idx:].strip()
                # Get the first sentence
                sentences = remaining.split('.')
                if sentences:
                    return sentences[0].strip()
        
        # If no clear conclusion indicator, try to get the last sentence
        sentences = response.split('.')
        if len(sentences) > 1:
            return sentences[-2].strip() + '.'
        
        return response[:200] + "..." if len(response) > 200 else response
    
    def _calculate_confidence(self, response: str, reasoning_type: str) -> float:
        """
        Calculate confidence score based on response quality.
        
        Args:
            response (str): Response text
            reasoning_type (str): Type of reasoning used
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        base_confidence = 0.7
        
        # Length factor
        if len(response) > 100:
            base_confidence += 0.1
        elif len(response) < 50:
            base_confidence -= 0.2
        
        # Structure factor (look for numbered steps, conclusions, etc.)
        if any(indicator in response.lower() for indicator in ['step', 'conclusion', 'therefore', 'thus']):
            base_confidence += 0.1
        
        # Reasoning type factor
        if reasoning_type == 'logical':
            base_confidence += 0.1
        
        return min(1.0, max(0.0, base_confidence))
    
    def _call_openrouter(self, prompt: str) -> Optional[str]:
        """
        Call the OpenRouter chat completion endpoint.
        
        Args:
            prompt (str): Prompt to send
        
        Returns:
            Optional[str]: Response text or None
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.referer,
            "X-Title": self.app_title,
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a precise reasoning assistant for a research project. "
                        "Always explain your logical steps clearly, enumerate premises, and conclude explicitly."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.3,
            "max_tokens": int(os.getenv("OPENROUTER_MAX_TOKENS", "512")),
            "top_p": 0.9,
        }

        response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            logger.error(
                "OpenRouter API returned %s: %s",
                response.status_code,
                response.text[:200],
            )
            return None

        data = response.json()
        choices = data.get("choices")
        if not choices:
            return None

        return choices[0].get("message", {}).get("content")
    
    def _fallback_reasoning(self, problem: str) -> Dict[str, Any]:
        """
        Fallback reasoning when API is not available.
        
        Args:
            problem (str): Problem to analyze
            
        Returns:
            Dict[str, Any]: Fallback result
        """
        logger.info("Using fallback reasoning (no API available)")
        
        # Simple pattern-based reasoning
        problem_lower = problem.lower()
        
        # Check for conditional statements
        if 'if' in problem_lower and 'then' in problem_lower:
            return {
                'result': f"Based on the conditional statement in the problem: '{problem}', I can analyze the logical structure. However, without access to the reasoning model, I can only provide a basic analysis.",
                'conclusion': "Conditional logic detected - requires formal analysis",
                'confidence': 0.3,
                'reasoning_type': 'fallback',
                'success': False
            }
        
        # Check for questions
        if any(q_word in problem_lower for q_word in ['is', 'are', 'can', 'will', 'does', 'do']):
            return {
                'result': f"The problem appears to be a question: '{problem}'. This requires detailed analysis which I cannot provide without the reasoning model.",
                'conclusion': "Question format detected - requires reasoning analysis",
                'confidence': 0.2,
                'reasoning_type': 'fallback',
                'success': False
            }
        
        # Generic fallback
        return {
            'result': f"I cannot provide detailed reasoning for: '{problem}' without access to the reasoning model. Please check your API configuration.",
            'conclusion': "Unable to analyze - API not available",
            'confidence': 0.1,
            'reasoning_type': 'fallback',
            'success': False
        }

def get_natural_language_reasoner(api_key: Optional[str] = None) -> NaturalLanguageReasoner:
    """
    Factory function to create a natural language reasoner.
    
    Args:
        api_key (str, optional): OpenRouter API key
        
    Returns:
        NaturalLanguageReasoner: Configured reasoner instance
    """
    return NaturalLanguageReasoner(api_key)
