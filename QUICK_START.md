# Quick Start Guide - Dual Modality Reasoning Agent

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Core Functionality (Optional)
```bash
python run_demo.py
```
This tests the logic reasoning module without needing any API keys.

### 3. Run the Application

**Option A: With Google Gemini API (Full Features)**
1. Get a free API key from: https://makersuite.google.com/app/apikey
2. Set the API key: `export GOOGLE_AI_API_KEY='your_key'`
3. Run: `streamlit run main.py`

**Option B: Without API (Logic Reasoning Only)**
```bash
streamlit run main.py
```
The system will work with fallback reasoning for natural language problems.

## 🧪 Test the System

Try these example problems:

1. **Formal Logic**: `A → B` (generates truth table)
2. **Conditional**: `If it rains, the ground is wet. It's raining. Is the ground wet?`
3. **Complex Logic**: `(A ∧ B) ∨ (¬A ∧ C)`

## 📊 Run Evaluation
```bash
python evaluation.py
```
Tests the system on 10 predefined problems and generates performance metrics.

## 🔧 Troubleshooting

- **Import Errors**: Make sure all dependencies are installed
- **API Issues**: The system works without the Google API using fallback reasoning
- **Logic Parsing**: Use simple logical notation for best results

## 📁 Key Files

- `main.py` - Streamlit web interface
- `run_demo.py` - Command-line demo (no API needed)
- `logic_reasoning.py` - Core logic reasoning engine
- `natural_language.py` - Natural language processing (requires API)
- `evaluation.py` - Performance testing suite

## 🎯 What It Does

The system analyzes problems and:
1. **Detects logical structure** in the input
2. **Selects appropriate reasoning mode** (Logic, Natural Language, or Both)
3. **Generates truth tables** for formal logic
4. **Provides step-by-step explanations**
5. **Combines results** with confidence scoring

Perfect for research on multi-modal AI reasoning and symbolic-neural integration!

