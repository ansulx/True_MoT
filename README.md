<div align="center">

# 🧠 True_MoT: Dual Modality Reasoning Agent

**Bridging Symbolic Logic & Neural Reasoning** | *Where Formal Logic Meets Natural Language Understanding*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-FF4B4B.svg)](https://streamlit.io/)
[![SymPy](https://img.shields.io/badge/SymPy-1.12-green.svg)](https://www.sympy.org/)
[![License](https://img.shields.io/badge/License-Research-purple.svg)](LICENSE)

*A research-grade AI system that intelligently combines natural language reasoning with formal truth table logic for comprehensive problem-solving and analysis.*

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## 🎯 What is True_MoT?

**True_MoT** (True Modality of Thought) is an advanced reasoning system that seamlessly integrates two powerful AI paradigms:

- 🗣️ **Natural Language Reasoning** - Leverages Google's Gemini API for intuitive, chain-of-thought problem-solving
- 🔢 **Formal Logic Reasoning** - Uses SymPy for rigorous symbolic logic, truth table generation, and propositional analysis
- 🎯 **Intelligent Integration** - Automatically selects and combines the optimal reasoning approach(es) for each problem

Think of it as having both a philosopher and a mathematician working together in perfect harmony. 🎭

---

## ✨ Key Features

### 🚀 Core Capabilities

| Feature | Description |
|---------|-------------|
| **🧠 Intelligent Mode Selection** | Automatically analyzes problem structure to determine optimal reasoning approach |
| **🔄 Dual-Mode Processing** | Runs both reasoning modes simultaneously for complex problems requiring multiple perspectives |
| **📊 Result Integration** | Combines outputs with sophisticated confidence scoring and conflict resolution |
| **📋 Truth Table Generation** | Creates comprehensive truth tables for formal propositional logic statements |
| **💭 Chain-of-Thought Reasoning** | Provides step-by-step natural language explanations with full transparency |

### 🎨 Reasoning Modes

- **Natural Language Only** → Perfect for narrative problems, philosophical questions, and complex reasoning
- **Logic Only** → Ideal for formal logical statements, mathematical proofs, and symbolic analysis
- **Dual Mode** → The best of both worlds for problems that benefit from multiple reasoning approaches

### 🖥️ Interface Features

- ✨ Clean, modern Streamlit web interface
- ⚡ Real-time problem analysis and mode selection
- 📖 Expandable detailed reasoning displays
- 📚 Example problems library and processing history
- 📊 Interactive truth table visualization

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────┐
                    │      Problem Input              │
                    └────────────┬────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Keyword Detection &    │
                    │  Problem Analysis       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Mode Selection        │
                    │  (Logic/NL/Dual)        │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐      ┌────────▼────────┐      ┌───────▼────────┐
│ Logic Reasoning│      │ Natural Language│      │   Dual Mode    │
│    (SymPy)     │      │  (Gemini API)   │      │  (Both)        │
│                │      │                 │      │                │
│ Truth Tables   │      │ Chain-of-Thought│      │ Combined       │
│ Symbolic Logic │      │ Explanations    │      │ Results        │
└───────┬────────┘      └────────┬────────┘      └───────┬────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Result Integration     │
                    │  Confidence Scoring     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Streamlit Interface    │
                    │  Formatted Output       │
                    └─────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI API key ([Get one for free!](https://makersuite.google.com/app/apikey))
- Internet connection for API calls

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ansulx/True_MoT.git
   cd True_MoT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (choose one method)
   
   **Option A: Environment Variable** (Recommended)
   ```bash
   export GOOGLE_AI_API_KEY="your_api_key_here"
   ```
   
   **Option B: Through the Streamlit interface**
   - Run the app and enter your API key in the sidebar

4. **Launch the application**
   ```bash
   streamlit run main.py
   ```
   
   The app will open at `http://localhost:8501` 🎉

---

## 🎮 Usage Examples

### Example 1: Formal Logic
```
Input: "A → B"
Output: 
- Mode: Logic Only
- Truth Table Generated (4 rows)
- Confidence: 0.95
```

### Example 2: Conditional Reasoning
```
Input: "If it rains, the ground is wet. It's raining. Is the ground wet?"
Output:
- Mode: Dual Mode
- Natural Language: Step-by-step explanation
- Logic: Formal proof with truth table
- Final Answer: Yes, with 0.92 confidence
```

### Example 3: Complex Logic
```
Input: "(A ∧ B) ∨ (¬A ∧ C)"
Output:
- Mode: Logic Only
- Complete truth table (8 rows)
- Simplified expression
- Confidence: 0.88
```

---

## 🧪 Evaluation & Testing

### Run the Evaluation Suite

```bash
python evaluation.py
```

This comprehensive test suite will:
- ✅ Test the system on 10 predefined problems across multiple categories
- 📊 Compare dual-mode vs single-mode performance
- ⏱️ Generate accuracy metrics and response times
- 💾 Save results to CSV files for detailed analysis

### Explore Sample Problems

```bash
python sample_problems.py
```

View the complete collection of 21+ test problems organized by:
- Category (Conditional, Formal Logic, Categorical)
- Difficulty level
- Expected reasoning mode

### Quick Demo (No API Required)

```bash
python run_demo.py
```

Test the core logic reasoning functionality without needing an API key!

---

## 📊 Performance Metrics

The evaluation system tracks:

| Metric | Description |
|--------|-------------|
| **Accuracy** | Correctness of final answers across problem types |
| **Mode Selection Accuracy** | How well the system chooses the right reasoning approach |
| **Confidence Scoring** | Reliability of confidence assessments |
| **Response Time** | Processing speed for each mode |
| **Category Performance** | Performance breakdown by problem type |

---

## 📁 Project Structure

```
True_MoT/
├── 🎯 main.py                 # Streamlit web interface
├── 🧩 integration.py          # Main controller & mode selection
├── 💬 natural_language.py     # Natural language reasoning module
├── 🔢 logic_reasoning.py       # Logic reasoning & truth tables
├── 🛠️ utils.py                # Utility functions & helpers
├── 🧪 evaluation.py           # Evaluation suite & testing
├── 📚 sample_problems.py      # Test problems collection
├── 🎬 run_demo.py             # Command-line demo
├── 📦 requirements.txt        # Python dependencies
└── 📖 README.md               # This file
```

---

## 🔬 Research Applications

This system demonstrates cutting-edge concepts in:

- **🤖 Multi-modal AI Integration** - Combining symbolic and neural reasoning paradigms
- **🔗 Neural-Symbolic AI** - Bridging the gap between formal logic and natural language
- **📈 Confidence Estimation** - Quantifying reasoning reliability in hybrid systems
- **🎯 Intelligent Mode Selection** - Adaptive approach selection algorithms
- **🧮 Automated Theorem Proving** - Formal logic processing and verification
- **💡 Human-AI Interaction** - Clear explanations and visualizations

---

## 🛠️ Configuration & Customization

### API Configuration
- Uses Google's Gemini API (free tier available)
- No paid services required
- Graceful fallback reasoning when API is unavailable

### Customization Options
- Modify `utils.py` for different keyword detection patterns
- Adjust confidence thresholds in `integration.py`
- Add new problem types in `sample_problems.py`
- Extend logic operators in `logic_reasoning.py`

---

## 🐛 Troubleshooting

### Common Issues

**🔑 API Key Issues**
- Ensure your Google AI API key is valid and active
- Check that the key has necessary permissions
- Verify the key is correctly set (environment variable or interface)

**📦 Import Errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)
- Try: `pip install --upgrade -r requirements.txt`

**🔢 Logic Parsing Errors**
- The system handles basic propositional logic
- Complex formal logic may require simpler notation
- Use standard logical operators: `→`, `∧`, `∨`, `¬`, `↔`

### Error Handling
- ✅ Comprehensive error handling throughout
- 🔄 Fallback reasoning when APIs are unavailable
- 🛡️ Graceful degradation for unsupported problem types

---

## 📈 Roadmap & Future Enhancements

Potential improvements for research expansion:

- [ ] **Predicate Logic Support** - Extend beyond propositional logic
- [ ] **Multi-LLM Integration** - Support for additional free models (Claude, GPT, etc.)
- [ ] **ML-Based Mode Selection** - Machine learning approach selection
- [ ] **Interactive Proofs** - Step-by-step proof construction interface
- [ ] **Multi-language Support** - Reasoning in different languages
- [ ] **Graph Visualization** - Visual representation of logical relationships
- [ ] **API Endpoints** - RESTful API for programmatic access

---

## 📚 Academic References

This project implements concepts from:

- Multi-modal AI reasoning and hybrid systems
- Symbolic AI and neural-symbolic integration
- Formal logic and automated theorem proving
- Natural language processing and reasoning
- Human-AI interaction design
- Confidence estimation in AI systems

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Implement changes with tests
4. 📝 Commit your changes (`git commit -m 'Add amazing feature'`)
5. 📤 Push to the branch (`git push origin feature/amazing-feature`)
6. 🔄 Open a Pull Request with detailed description

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Be respectful and constructive in discussions

---

## 📄 License

This project is created for **academic research purposes**. Please ensure compliance with:
- Google AI API terms of service
- Academic integrity guidelines
- Any applicable institutional policies

---

## 👤 Author

**ansulx** - *AI Researcher & Developer*

- GitHub: [@ansulx](https://github.com/ansulx)
- Email: ansulpundir2468@gmail.com

---

## 🙏 Acknowledgments

- Google for the Gemini API
- SymPy team for the excellent symbolic math library
- Streamlit for the amazing web framework
- The open-source community for inspiration and tools

---

<div align="center">

### ⭐ If you find this project interesting, give it a star! ⭐

**Made with ❤️ and lots of ☕ by an AI researcher passionate about multi-modal reasoning**

---

*"The best way to predict the future is to combine multiple ways of thinking about it."* 🚀

</div>
