"""
Research-Grade Dual Modality Reasoning Agent Interface
Clean, minimal, professional design for academic demonstrations
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
    initial_sidebar_state="collapsed"
)

# Clean, minimal CSS
st.markdown("""
<style>
    /* Reset/defaults */
    body, .css-1v0mbdj, .block-container {
        background-color: #f5f7fb !important;
        color: #1f2937;
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
    }

    #MainMenu, footer {visibility: hidden;}

    .main-title {
        font-size: 2.4rem;
        font-weight: 600;
        color: #0f172a;
        text-align: left;
        margin-bottom: 0.4rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }

    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 2px 10px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.2rem;
    }

    .card h4 {
        margin-top: 0;
        color: #0f172a;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 0.2rem;
    }

    .value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
    }

    .confidence-high { color: #16a34a; }
    .confidence-medium { color: #eab308; }
    .confidence-low { color: #dc2626; }

    .feature-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem 0.8rem;
        padding: 0;
        list-style: none;
        margin: 0;
    }

    .feature-pill {
        background-color: #e0f2fe;
        color: #0c4a6e;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .example-grid button {
        width: 100%;
        border-radius: 8px !important;
        border: 1px solid #cbd5f5;
        background: #eef2ff !important;
        color: #1e3a8a !important;
        font-weight: 500 !important;
    }

    .example-grid button:hover {
        background: #e0e7ff !important;
        border-color: #a5b4fc !important;
    }

    .stTextArea textarea {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.95rem;
        line-height: 1.5;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #2563eb, #0ea5e9) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.8rem !important;
        border-radius: 999px !important;
    }

    .stButton button:hover {
        filter: brightness(1.05);
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
            mode = 'Formal Logic Analysis'
            explanation = "Detected formal logic symbols. Using symbolic reasoning."
        elif logical_features['logical_connectives'] or logical_features['conditionals']:
            mode = 'Logical Structure Analysis'
            explanation = "Detected logical structure. Using propositional logic analysis."
        else:
            mode = 'General Analysis'
            explanation = "Using general logical analysis approach."
        
        # Analyze with logic reasoner
        logic_result = st.session_state.logic_reasoner.reason(problem)
        
        # Calculate overall confidence
        confidence = logic_result['confidence']
        
        return {
            'success': True,
            'mode': mode,
            'explanation': explanation,
            'logic_result': logic_result,
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

def display_analysis_result(result: Dict[str, Any]):
    """Display the analysis result in a clean, research-grade format."""
    if not result['success']:
        st.error(f"**Error:** {result.get('error', 'Unknown error')}")
        return
    
    # Analysis Summary
    st.markdown("#### Analysis Summary")
    with st.container():
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.markdown('<div class="label">Reasoning Mode</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value">{result["mode"]}</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown('<div class="label">Confidence</div>', unsafe_allow_html=True)
            confidence_class = 'confidence-high' if result['confidence'] > 0.7 else 'confidence-medium' if result['confidence'] > 0.4 else 'confidence-low'
            st.markdown(f'<div class="value {confidence_class}">{result["confidence"]:.2f}</div>', unsafe_allow_html=True)
        with cols[2]:
            st.markdown('<div class="label">Status</div>', unsafe_allow_html=True)
            status_html = '<div class="value confidence-high">Success</div>' if result['success'] else '<div class="value confidence-low">Failed</div>'
            st.markdown(status_html, unsafe_allow_html=True)
    
    # Features Detected
    st.markdown("#### Features Detected")
    features = result['features']
    feature_text = []
    if features['formal_logic']:
        feature_text.append("Formal Logic Symbols")
    if features['logical_connectives']:
        feature_text.append("Logical Connectives")
    if features['conditionals']:
        feature_text.append("Conditional Statements")
    if features['quantifiers']:
        feature_text.append("Quantifiers")
    if features['questions']:
        feature_text.append("Question Format")
    
    if feature_text:
        pills = "".join([f'<span class="feature-pill">{txt}</span>' for txt in feature_text])
        st.markdown(f'<div class="card"><div class="feature-list">{pills}</div></div>', unsafe_allow_html=True)
    else:
        st.info("No specific logical features detected.")
    
    # Reasoning Process
    st.markdown("#### Reasoning Process")
    st.markdown(f"**Approach** · {result['explanation']}")
    
    # Logic Analysis
    if result['logic_result']['success']:
        with st.container():
            st.markdown("**Logic Analysis**")
            st.code(result['logic_result']['result'], language="text")
        
        # Truth Table
        if result['logic_result']['truth_table']:
            st.markdown("#### Truth Table")
            df = pd.DataFrame(result['logic_result']['truth_table'])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No truth table was generated for this expression.")
    
    # Final Conclusion
    st.markdown("#### Final Conclusion")
    st.success(result['conclusion'])

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Clean header
    st.markdown('<h1 class="main-title">Dual Modality Reasoning Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Research Demonstration · Integrating Formal Logic with Natural Language Reasoning</p>', unsafe_allow_html=True)
    
    # System status
    with st.container():
        cols = st.columns([1, 1, 1])
        cols[0].markdown('<div class="card"><div class="label">Logic Engine</div><div class="value confidence-high">Active</div></div>', unsafe_allow_html=True)
        cols[1].markdown('<div class="card"><div class="label">SymPy Integration</div><div class="value confidence-high">Ready</div></div>', unsafe_allow_html=True)
        cols[2].markdown('<div class="card"><div class="label">Truth Tables</div><div class="value confidence-high">Available</div></div>', unsafe_allow_html=True)
    
    # Example problems section
    st.markdown("#### Example Problems")
    st.markdown("Select a template problem to pre-fill the analyzer.")
    examples = [
        "A → B",
        "A ∧ B",
        "A ∨ B", 
        "If it rains, the ground is wet. It's raining. Is the ground wet?",
        "Prove that (A → B) ∧ (B → C) implies (A → C)",
        "What is the truth value of P ∨ ¬P?"
    ]
    
    st.markdown('<div class="example-grid">', unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    for idx, example in enumerate(examples):
        with cols[idx % 3]:
            if st.button(example, key=f"example_{idx}"):
                st.session_state.problem_input = example
                st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main input section
    st.markdown("#### Problem Input")
    problem = st.text_area(
        "Problem Statement",
        placeholder="Example: If it rains, the ground is wet. It's raining. Is the ground wet?",
        height=120,
        key="problem_input"
    )
    
    # Analyze button
    if st.button("Analyze Problem", use_container_width=True):
        if not problem.strip():
            st.warning("Please enter a problem to analyze.")
        else:
            # Process the problem
            with st.spinner("Analyzing problem..."):
                try:
                    result = analyze_problem(problem)
                    
                    # Store in history
                    st.session_state.processing_history.append({
                        'problem': problem,
                        'result': result,
                        'timestamp': time.time()
                    })
                    
                    # Display results
                    display_analysis_result(result)
                    
                except Exception as e:
                    st.error(f"Error processing problem: {str(e)}")
                    logger.error(f"Error in main processing: {e}")
    
    # Processing history
    if st.session_state.processing_history:
        st.markdown("### Recent Analyses")
        for i, history_item in enumerate(st.session_state.processing_history[-3:], 1):
            with st.expander(f"Analysis {i}: {history_item['problem'][:50]}{'...' if len(history_item['problem']) > 50 else ''}"):
                if history_item['result']['success']:
                    st.write(f"**Mode:** {history_item['result']['mode']}")
                    st.write(f"**Confidence:** {history_item['result']['confidence']:.2f}")
                    st.write(f"**Conclusion:** {history_item['result']['conclusion']}")
                else:
                    st.write(f"**Error:** {history_item['result'].get('error', 'Unknown error')}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem; margin-top: 2rem;">
        <p><strong>Dual Modality Reasoning Agent</strong> | Research Project</p>
        <p>Demonstrating integration of formal logic with intelligent reasoning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

