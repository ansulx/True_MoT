"""
Simplified Dual Modality Reasoning Agent - Streamlit Interface
Works without external API dependencies
"""

import streamlit as st
import pandas as pd
import time
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

def initialize_session_state():
    """Initialize session state variables."""
    if 'logic_reasoner' not in st.session_state:
        st.session_state.logic_reasoner = get_logic_reasoner()
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []

def analyze_problem(problem: str) -> Dict[str, Any]:
    """
    Analyze a problem using logic reasoning.
    
    Args:
        problem (str): The problem to analyze
        
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
        
        # Determine reasoning mode based on features
        if logical_features['formal_logic']:
            mode = 'Logic Only'
            explanation = "Formal logic symbols detected. Using logic reasoning."
        elif logical_features['logical_connectives'] or logical_features['conditionals']:
            mode = 'Dual Mode (Logic Focus)'
            explanation = "Logical structure detected. Using logic reasoning with natural language context."
        else:
            mode = 'Natural Language Only (Fallback)'
            explanation = "No clear logical structure. Using fallback reasoning."
        
        # Analyze with logic reasoner
        logic_result = st.session_state.logic_reasoner.reason(problem)
        
        # Calculate overall confidence
        confidence = logic_result['confidence']
        
        # Generate combined result
        combined_result = f"""
Analysis Mode: {mode}
Explanation: {explanation}

Logic Reasoning Result:
{logic_result['result']}

Conclusion: {logic_result['conclusion']}
"""
        
        return {
            'success': True,
            'mode': mode,
            'explanation': explanation,
            'logic_result': logic_result,
            'combined_result': combined_result,
            'confidence': confidence,
            'conclusion': logic_result['conclusion'],
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
    if 'Logic' in mode:
        mode_color = "🟦"
    elif 'Natural Language' in mode:
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
        st.markdown("**Analysis:**")
        st.text_area("", value=result['combined_result'], height=200, disabled=True)
        
        # Logic reasoning details
        if result['logic_result']['success']:
            st.markdown("**Logic Analysis:**")
            st.text_area("", value=result['logic_result']['result'], height=150, disabled=True)
            
            # Display truth table if available
            if result['logic_result']['truth_table']:
                st.markdown("**Truth Table:**")
                df = pd.DataFrame(result['logic_result']['truth_table'])
                st.dataframe(df, use_container_width=True)
        else:
            st.text("Logic analysis was not successful for this problem type.")

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
        <p>Logic Reasoning with Truth Table Generation</p>
        <p><em>Simplified version - Logic reasoning module active</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ System Status")
        st.success("✅ Logic Reasoning: Active")
        st.info("ℹ️ Natural Language: Fallback Mode")
        st.warning("⚠️ Google API: Not available (dependency conflict)")
        
        # Example problems
        display_example_problems()
        
        # Processing history
        if st.session_state.processing_history:
            st.markdown("### 📊 Recent Problems")
            for i, history_item in enumerate(st.session_state.processing_history[-5:], 1):
                if st.button(f"{i}. {history_item['problem'][:40]}...", key=f"history_{i}"):
                    st.session_state.problem_input = history_item['problem']
                    st.rerun()
    
    # Main interface
    st.markdown("### 💭 Enter Your Problem")
    
    # Problem input
    problem = st.text_area(
        "Describe the problem or question you'd like to analyze:",
        placeholder="e.g., 'If it rains, the ground is wet. It's raining. Is the ground wet?' or 'A → B'",
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
                    result = analyze_problem(problem)
                    
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
        <p>Dual Modality Reasoning Agent - Logic Reasoning Module</p>
        <p>Demonstrating formal logic processing with truth table generation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
