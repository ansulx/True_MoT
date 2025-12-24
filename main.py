"""
Main Streamlit Interface for Dual Modality Reasoning Agent
"""

import streamlit as st
import pandas as pd
import time
from typing import Dict, Any
import logging

from integration import get_dual_modality_controller
from utils import validate_input

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

def initialize_session_state():
    """Initialize session state variables."""
    if 'controller' not in st.session_state:
        st.session_state.controller = None
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = False

def setup_controller():
    """Setup the dual modality controller with API key."""
    api_key = st.session_state.get('api_key_input', '')
    
    if api_key and not st.session_state.api_key_set:
        try:
            st.session_state.controller = get_dual_modality_controller(api_key)
            st.session_state.api_key_set = True
            st.success("✅ API key configured successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Error setting up controller: {str(e)}")
            return False
    elif st.session_state.controller is None:
        # Try to use environment variable
        import os
        if os.getenv('GOOGLE_AI_API_KEY'):
            try:
                st.session_state.controller = get_dual_modality_controller()
                st.session_state.api_key_set = True
                return True
            except Exception as e:
                logger.error(f"Error setting up controller with env var: {e}")
    
    return st.session_state.api_key_set

def display_mode_selection(mode_selection: Dict[str, Any]):
    """Display the reasoning mode selection information."""
    st.markdown("### 🎯 Reasoning Mode Selection")
    
    mode = mode_selection['mode']
    explanation = mode_selection['explanation']
    
    # Mode indicator with color coding
    if mode == 'Logic Only':
        mode_color = "🟦"
    elif mode == 'Natural Language Only':
        mode_color = "🟩"
    else:
        mode_color = "🟪"
    
    st.markdown(f"""
    <div class="mode-info">
        <h4>{mode_color} Selected Mode: {mode}</h4>
        <p><strong>Explanation:</strong> {explanation}</p>
        <p><strong>Logic Confidence:</strong> {mode_selection['logic_confidence']:.2f}</p>
        <p><strong>Natural Language Confidence:</strong> {mode_selection['nl_confidence']:.2f}</p>
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
                if result['natural_language'] and result['natural_language']['success']:
                    st.text_area("", value=result['natural_language']['result'], height=150, disabled=True)
                else:
                    st.text("No natural language analysis available")
            
            with col2:
                st.markdown("**Logic Reasoning:**")
                if result['logic_reasoning'] and result['logic_reasoning']['success']:
                    st.text_area("", value=result['logic_reasoning']['result'], height=150, disabled=True)
                    
                    # Display truth table if available
                    if result['logic_reasoning']['truth_table']:
                        st.markdown("**Truth Table:**")
                        df = pd.DataFrame(result['logic_reasoning']['truth_table'])
                        st.dataframe(df, use_container_width=True)
                else:
                    st.text("No logic analysis available")
        
        elif result['mode'] == 'Natural Language Only':
            st.markdown("**Natural Language Analysis:**")
            if result['natural_language'] and result['natural_language']['success']:
                st.text_area("", value=result['natural_language']['result'], height=200, disabled=True)
            else:
                st.text("Natural language analysis failed")
        
        elif result['mode'] == 'Logic Only':
            st.markdown("**Logic Analysis:**")
            if result['logic_reasoning'] and result['logic_reasoning']['success']:
                st.text_area("", value=result['logic_reasoning']['result'], height=200, disabled=True)
                
                # Display truth table if available
                if result['logic_reasoning']['truth_table']:
                    st.markdown("**Truth Table:**")
                    df = pd.DataFrame(result['logic_reasoning']['truth_table'])
                    st.dataframe(df, use_container_width=True)
            else:
                st.text("Logic analysis failed")

def display_example_problems():
    """Display example problems in the sidebar."""
    st.sidebar.markdown("### 📚 Example Problems")
    
    examples = [
        "If it rains, the ground is wet. It's raining. Is the ground wet?",
        "All birds can fly. Penguins are birds. Can penguins fly?",
        "Prove that (A → B) ∧ (B → C) implies (A → C)",
        "If John studies, he passes. John studied. What happened?",
        "Is the statement 'P ∧ ¬P' always true or always false?",
        "If A implies B, and B implies C, does A imply C?"
    ]
    
    for i, example in enumerate(examples, 1):
        if st.sidebar.button(f"Example {i}", key=f"example_{i}"):
            st.session_state.problem_input = example
            st.rerun()

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Dual Modality Reasoning Agent</h1>
        <p>Integrating Natural Language and Formal Logic Reasoning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            help="Enter your Google AI API key for natural language reasoning",
            key="api_key_input"
        )
        
        if st.button("Set API Key"):
            setup_controller()
        
        # Display setup status
        if st.session_state.api_key_set:
            st.success("✅ Controller ready")
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
        elif not st.session_state.api_key_set:
            st.error("Please set your API key in the sidebar first.")
        else:
            # Validate input
            validation = validate_input(problem)
            if not validation['valid']:
                st.error(f"❌ {validation['error']}")
            else:
                # Process the problem
                with st.spinner("🧠 Analyzing problem..."):
                    try:
                        result = st.session_state.controller.process_problem(problem)
                        
                        # Store in history
                        st.session_state.processing_history.append({
                            'problem': problem,
                            'result': result,
                            'timestamp': time.time()
                        })
                        
                        # Display results
                        if 'mode_selection' in result:
                            display_mode_selection(result['mode_selection'])
                        
                        display_result(result)
                        
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

