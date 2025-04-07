# 🤖 Code Whisperer – AI Code Review Assistant

> Your personal senior dev – now powered by GenAI.

**Code Whisperer** is a conversational AI assistant designed to analyze, explain, and improve your code. Built as a Capstone project using **Google Gemini**, **Streamlit**, and advanced **prompt engineering**, this tool showcases real-world LLM application for developers.

---

## ✨ Features

✅ Natural Language Chat Interface (via `st.chat_message`)  
✅ Supports `.py`, `.txt`, `.json`, `.pdf` file uploads  
✅ Memory-enabled Gemini model with conversational context  
✅ Customizable generation settings (temperature, top-k, top-p, max tokens)  
✅ Hallucination guardrails with scoring + clarification retries  
✅ Prompt engineered for accuracy, structure, and clarity  
✅ Markdown-enhanced output for readable, dev-friendly results

---

## 💡 Use Cases

- Ask questions about code behavior, bugs, or best practices  
- Upload files and get breakdowns, summaries, or performance tips  
- Chat freely and receive context-aware mentorship  
- Evaluate LLM reliability with grounded response scoring

---

## 🧠 Technologies Used

- 🧠 [Google Gemini (Generative AI)](https://ai.google.dev/)
- 🖼️ [Streamlit](https://streamlit.io/)
- 📄 [PyMuPDF](https://github.com/pymupdf/PyMuPDF) for PDF parsing
- 🛡️ Custom scoring + hallucination filtering logic
- 💬 Prompt engineering using human-aligned mentor archetype

---

## 🚀 Live Demo

👉 Try the app on [Streamlit Cloud](https://your-streamlit-app-link.streamlit.app)

---

## 📂 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/code-whisperer.git
cd code-whisperer

# 2. Create virtual environment & activate it (optional but recommended)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
# Inside .streamlit/secrets.toml:
# [GEMINI_API_KEY]
# GEMINI_API_KEY = "your-google-api-key"

# 5. Run the app
streamlit run agent_app.py
