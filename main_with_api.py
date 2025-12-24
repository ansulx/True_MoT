"""
Dual Modality Reasoning Agent with Google API - Streamlit Interface
Uses requests to call Google API directly to avoid dependency conflicts
"""

import streamlit as st
import pandas as pd
import time
import requests
import json
import os
from typing import Dict, Any
import logging

from logic_reasoning import get_logic_reasoner
from utils import detect_logical_keywords, validate_input
from sample_problems import get_all_problems, get_problems_by_category

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Dual Modality Reasoning Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .mode-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
    .result-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .truth-table {
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def call_gemini_api(problem: str, api_key: str) -> Dict[str, Any]:
    """
    Call Google Gemini API using requests to avoid dependency conflicts.
    
    Args:
        problem (str): Problem to analyze
        api_key (str): Google AI API key
        
    Returns:
        Dict[str, Any]: API response
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        prompt = f"""You are a logical reasoning expert. Analyze the following problem step by step:

Problem: {problem}

Please provide:
1. A clear step-by-step logical analysis
2. Identify the logical structure (premises, conclusions, reasoning)
3. State your final answer clearly
4. Explain your reasoning process

Be concise but thorough in your analysis."""

        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return {
                    'success': True,
                    'result': content,
                    'conclusion': extract_conclusion(content),
                    'confidence': 0.8
                }
        
        return {
            'success': False,
            'result': f"API Error: {response.status_code}",
            'conclusion': "API call failed",
            'confidence': 0.1
        }
        
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return {
            'success': False,
            'result': f"API Error: {str(e)}",
            'conclusion': "API call failed",
            'confidence': 0.1
        }

def extract_conclusion(text: str) -> str:
    """Extract conclusion from Gemini response."""
    # Look for conclusion indicators
    conclusion_indicators = [
        'conclusion:', 'final answer:', 'answer:', 'result:',
        'therefore:', 'thus:', 'hence:', 'in conclusion:'
    ]
    
    text_lower = text.lower()
    for indicator in conclusion_indicators:
        if indicator in text_lower:
            start_idx = text_lower.find(indicator) + len(indicator)
            remaining = text[start_idx:].strip()
            sentences = remaining.split('.')
            if sentences:
                return sentences[0].strip()
    
    # If no clear conclusion indicator, get the last sentence
    sentences = text.split('.')
    if len(sentences) > 1:
        return sentences[-2].strip() + '.'
    
    return text[:200] + "..." if len(text) > 200 else text

def initialize_session_state():
    """Initialize session state variables."""
    if 'logic_reasoner' not in st.session_state:
        st.session_state.logic_reasoner = get_logic_reasoner()
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = False

def analyze_problem(problem: str, api_key: str = None) -> Dict[str, Any]:
    """
    Analyze a problem using both logic and natural language reasoning.
    
    Args:
        problem (str): The problem to analyze
        api_key (str): Google AI API key
        
    Returns:
        Dict[str, Any]: Analysis result
    """
    # Validate input
    validation = validate_input(problem)
    if not validation['valid']:
        return {
            'error': validation['error'],
            'success': False
        }
    
    try:
        # Detect logical features
        logical_features = detect_logical_keywords(problem)
        
        # Run logic reasoning
        logic_result = st.session_state.logic_reasoner.reason(problem)
        
        # Run natural language reasoning if API key available
        nl_result = None
        if api_key:
            nl_result = call_gemini_api(problem, api_key)
        
        # Determine mode and combine results
        if logical_features['formal_logic']:
            mode = 'Logic Only'
            explanation = "Formal logic symbols detected. Using logic reasoning."
            combined_result = logic_result['result']
            confidence = logic_result['confidence']
            conclusion = logic_result['conclusion']
        elif api_key and nl_result['success']:
            if logic_result['success']:
                mode = 'Dual Mode'
                explanation = "Using both natural language and logic reasoning."
                combined_result = f"""Natural Language Analysis:
{nl_result['result']}

Logic Analysis:
{logic_result['result']}"""
                confidence = (nl_result['confidence'] + logic_result['confidence']) / 2
                conclusion = f"NL: {nl_result['conclusion']} | Logic: {logic_result['conclusion']}"
            else:
                mode = 'Natural Language Only'
                explanation = "Using natural language reasoning."
                combined_result = nl_result['result']
                confidence = nl_result['confidence']
                conclusion = nl_result['conclusion']
        else:
            mode = 'Logic Only (Fallback)'
            explanation = "Using logic reasoning (natural language API not available)."
            combined_result = logic_result['result']
            confidence = logic_result['confidence']
            conclusion = logic_result['conclusion']
        
        return {
            'success': True,
            'mode': mode,
            'explanation': explanation,
            'logic_result': logic_result,
            'nl_result': nl_result,
            'combined_result': combined_result,
            'confidence': confidence,
            'conclusion': conclusion,
            'features': logical_features
        }
        
    except Exception as e:
        logger.error(f"Error analyzing problem: {e}")
        return {
            'error': f"Error analyzing problem: {str(e)}",
            'success': False
        }

def display_mode_selection(mode: str, explanation: str, features: Dict[str, bool]):
    """Display the reasoning mode selection information."""
    st.markdown("### 🎯 Reasoning Mode Selection")
    
    # Mode indicator with color coding
    if 'Logic' in mode and 'Dual' not in mode:
        mode_color = "🟦"
    elif 'Natural Language' in mode and 'Dual' not in mode:
        mode_color = "🟩"
    else:
        mode_color = "🟪"
    
    st.markdown(f"""
    <div class="mode-info">
        <h4>{mode_color} Selected Mode: {mode}</h4>
        <p><strong>Explanation:</strong> {explanation}</p>
        <p><strong>Features Detected:</strong></p>
        <ul>
            <li>Logical Connectives: {'✅' if features['logical_connectives'] else '❌'}</li>
            <li>Conditionals: {'✅' if features['conditionals'] else '❌'}</li>
            <li>Formal Logic: {'✅' if features['formal_logic'] else '❌'}</li>
            <li>Quantifiers: {'✅' if features['quantifiers'] else '❌'}</li>
            <li>Questions: {'✅' if features['questions'] else '❌'}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def display_result(result: Dict[str, Any]):
    """Display the reasoning result."""
    if not result['success']:
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    # Display final answer prominently
    st.markdown("### 🎯 Final Answer")
    st.markdown(f"""
    <div class="result-box">
        <h3>{result['conclusion']}</h3>
        <p><strong>Confidence:</strong> <span class="confidence-{'high' if result['confidence'] > 0.7 else 'medium' if result['confidence'] > 0.4 else 'low'}">{result['confidence']:.2f}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display detailed reasoning
    st.markdown("### 📝 Detailed Reasoning")
    
    with st.expander("Show detailed analysis", expanded=True):
        # Combined result
        st.markdown("**Combined Analysis:**")
        st.text_area("", value=result['combined_result'], height=200, disabled=True)
        
        # Mode-specific results
        if result['mode'] == 'Dual Mode':
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Natural Language Reasoning:**")
                if result['nl_result'] and result['nl_result']['success']:
                    st.text_area("", value=result['nl_result']['result'], height=150, disabled=True)
                else:
                    st.text("Natural language analysis not available")
            
            with col2:
                st.markdown("**Logic Reasoning:**")
                if result['logic_result']['success']:
                    st.text_area("", value=result['logic_result']['result'], height=150, disabled=True)
                    
                    # Display truth table if available
                    if result['logic_result']['truth_table']:
                        st.markdown("**Truth Table:**")
                        df = pd.DataFrame(result['logic_result']['truth_table'])
                        st.dataframe(df, use_container_width=True)
                else:
                    st.text("Logic analysis failed")
        
        elif 'Natural Language' in result['mode']:
            st.markdown("**Natural Language Analysis:**")
            if result['nl_result'] and result['nl_result']['success']:
                st.text_area("", value=result['nl_result']['result'], height=200, disabled=True)
            else:
                st.text("Natural language analysis failed")
        
        elif 'Logic' in result['mode']:
            st.markdown("**Logic Analysis:**")
            if result['logic_result']['success']:
                st.text_area("", value=result['logic_result']['result'], height=200, disabled=True)
                
                # Display truth table if available
                if result['logic_result']['truth_table']:
                    st.markdown("**Truth Table:**")
                    df = pd.DataFrame(result['logic_result']['truth_table'])
                    st.dataframe(df, use_container_width=True)
            else:
                st.text("Logic analysis failed")

def display_example_problems():
    """Display example problems in the sidebar."""
    st.sidebar.markdown("### 📚 Example Problems")
    
    # Get problems by category
    categories = ['conditional', 'formal_logic', 'categorical']
    
    for category in categories:
        st.sidebar.markdown(f"**{category.title()}:**")
        problems = get_problems_by_category(category)
        
        for i, problem in enumerate(problems[:2], 1):  # Show first 2
            if st.sidebar.button(f"{i}. {problem['problem'][:40]}...", key=f"{category}_{i}"):
                st.session_state.problem_input = problem['problem']
                st.rerun()

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Dual Modality Reasoning Agent</h1>
        <p>Integrating Natural Language and Formal Logic Reasoning</p>
        <p><em>Full version with Google Gemini API</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        # Check if API key is set in environment variable
        default_key = os.getenv('GOOGLE_AI_API_KEY', '')
        api_key = st.text_input(
            "Google AI API Key",
            value=default_key,
            type="password",
            help="Enter your Google AI API key for natural language reasoning",
            key="api_key_input"
        )
        
        if st.button("Set API Key"):
            if api_key:
                st.session_state.api_key_set = True
                st.success("✅ API key configured successfully!")
            else:
                st.error("❌ Please enter an API key")
        
        # Display setup status
        if st.session_state.api_key_set and api_key:
            st.success("✅ Controller ready with API")
        else:
            st.warning("⚠️ Please set API key to enable natural language reasoning")
        
        # Example problems
        display_example_problems()
        
        # Processing history
        if st.session_state.processing_history:
            st.markdown("### 📊 Recent Problems")
            for i, history_item in enumerate(st.session_state.processing_history[-5:], 1):
                if st.button(f"{i}. {history_item['problem'][:50]}...", key=f"history_{i}"):
                    st.session_state.problem_input = history_item['problem']
                    st.rerun()
    
    # Main interface
    st.markdown("### 💭 Enter Your Problem")
    
    # Problem input
    problem = st.text_area(
        "Describe the problem or question you'd like to analyze:",
        placeholder="e.g., 'If it rains, the ground is wet. It's raining. Is the ground wet?'",
        height=100,
        key="problem_input"
    )
    
    # Submit button
    if st.button("🔍 Analyze Problem", type="primary"):
        if not problem.strip():
            st.error("Please enter a problem to analyze.")
        else:
            # Process the problem
            with st.spinner("🧠 Analyzing problem..."):
                try:
                    result = analyze_problem(problem, api_key if st.session_state.api_key_set else None)
                    
                    # Store in history
                    st.session_state.processing_history.append({
                        'problem': problem,
                        'result': result,
                        'timestamp': time.time()
                    })
                    
                    # Display results
                    if 'mode' in result:
                        display_mode_selection(result['mode'], result['explanation'], result['features'])
                        display_result(result)
                    else:
                        st.error("Error in result processing")
                    
                except Exception as e:
                    st.error(f"❌ Error processing problem: {str(e)}")
                    logger.error(f"Error in main processing: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>Dual Modality Reasoning Agent - Research Project</p>
        <p>Combining Natural Language and Formal Logic Reasoning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

