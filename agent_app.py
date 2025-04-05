#!/usr/bin/env python
# coding: utf-8

# # 🏆 Capstone Project: Code Whisperer – Your AI Code Review Buddy
# 
# 
# ### 👋 Introduction
# 
# **Code Whisperer** is an AI-powered code review assistant that acts like your personal senior developer.
# 
# It reviews your code, explains it, suggests improvements, spots bugs, and answers questions all within a chat-style notebook interface powered by GenAI.
# 
# Whether you’re a beginner or building a startup solo, Code Whisperer brings professional feedback right to your fingertips.

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# 
# 

# ### ❓ Problem Statement
# 
# **Code reviews** are essential for improving software quality, but many developers, especially students and solo devs that don’t have access to experienced mentors.
# 
# AI models like Gemini can help fill this gap, but they often hallucinate or give vague feedback.
# 
# 
# **Code Whisperer** solves this by combining:
# 
# A conversational code review agent
# 
# Self-evaluation of its responses
# 
# Guardrails to ensure accuracy

# -------------------------------------------------------------------------------------------------------------------------------------------------------

# ### 🤖 Solution: Code Whisperer
# 
# **Code Whisperer** is an interactive, GenAI-powered assistant built on Gemini (gemini-2.0-flash). It works by:
# 
# Accepting user-submitted code
# 
# Letting users chat with an AI code mentor
# 
# Scoring the agent’s answers
# 
# Asking the model to retry if its answer is weak
# 
# It’s like having a friendly, tireless senior dev on your team — available 24/7.

# -----------------------------------------------------------------------------------------------------------------------------------------------------

# ### 🧠 GenAI Capabilities Used
# 
# This project demonstrates at least 3 GenAI capabilities:
# 
# ✅ Agents – Conversational interaction via persistent memory
# 
# ✅ GenAI Evaluation – Keyword-based response scoring with retry logic
# 
# ✅ Structured Output – Markdown formatting, JSON-like analysis
# 
# ✅ (Optional bonus): Few-shot prompting, long context window handling

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# 
#  **Let´s code!**
# 
# -----------------------------------------------------------------------------------------------------------------------------------------------------

# ### ⚙️ How It Works
# 
# User inputs Python code
# 
# Agent starts a chat session with memory of that code
# 
# The user asks questions like:
# 
# “What does this function do?”
# 
# “Are there any bugs?”
# 
# “Can you improve the readability?”
# 
# The agent responds, and we score the quality of the response
# 
# If the answer is weak, the agent auto-corrects itself

# ========================================================================================
# 🤖 Code Whisperer – Capstone Project (Contest Submission)
# An AI-powered code review assistant with memory, tuning, evaluation & hallucination guardrails.
# Built with Gemini API + Streamlit
# ========================================================================================

import streamlit as st
import google.generativeai as genai
import json
import fitz

# ========================================================================================
# 🔐 SETUP GEMINI API (uses Streamlit secrets for secure key handling)
# ========================================================================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ========================================================================================
# 🧠 PERSONALITY PROMPT: Defines assistant behavior and safe conduct rules
# ========================================================================================
PERSONALITY_PROMPT = """
You are Code Whisperer — an elite AI-powered code mentor trained in software engineering, debugging, architecture, 
performance tuning, and best practices across multiple languages.

Your mission is to analyze, explain, and improve code with honesty, clarity, and precision.

🔐 Rules of Engagement:
1. If the code is ambiguous or incomplete, respond with what you *can* infer — and ask the user for clarification.
2. Never guess. If you're unsure or lack context, say: “I need more information to answer accurately.”
3. If a question is subjective (e.g., best language), offer a balanced perspective with pros/cons.
4. Use markdown for formatting. Use bullet points, headings, and code blocks for clarity.
5. Keep answers structured and direct — avoid rambling or filler.
6. Always explain **why** you're making a suggestion (especially when improving code).

💬 Response Format (when possible):
1. **What the code does**
2. **How it works**
3. **Any bugs, edge cases, or inefficiencies**
4. **Suggestions or improvements**
5. **Optional enhancements (if useful)**

🔥 Tone & Voice:
- Be professional but warm — like a mentor helping a student.
- Avoid jargon unless requested.
- Use examples to clarify concepts when helpful.

🛡️ Hallucination Safety:
- If asked a question outside your knowledge or training (e.g., future tech), say so respectfully.
- Never make up code features or behaviors.

You're allowed to say:
- "I don’t know."
- "Here’s what I can infer..."
- "I’d need more context to be sure."

Remember: Clarity > Creativity. Truth > Confidence.
"""

# ========================================================================================
# 🧠 CREATE ASSISTANT WITH MEMORY + CUSTOM SETTINGS
# ========================================================================================
def create_code_assistant(temperature=0.3, top_p=1.0, top_k=40, max_output_tokens=512):
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens
        )
    )

    if "chat" not in st.session_state:
        intro = PERSONALITY_PROMPT + "\n\nLet's start reviewing your code."
        st.session_state.chat = model.start_chat(history=[
            {"role": "user", "parts": [intro]},
            {"role": "model", "parts": ["Hi! I'm Code Whisperer. Paste your code or ask me anything."]}
        ])
    
    return st.session_state.chat

# ========================================================================================
# 🧪 EVALUATION LOGIC – SCORE THE RESPONSE BASED ON EXPECTED KEYWORDS
# ========================================================================================
def evaluate_response(response, expected_keywords_list):
    response_lower = response.lower()
    hits = sum(1 for kw in expected_keywords_list if kw.lower() in response_lower)
    score = hits / len(expected_keywords_list) if expected_keywords_list else 1.0
    return score

# ========================================================================================
# 🛡️ HALLUCINATION GUARDRAIL – Retry with caution prompt if confidence is low
# ========================================================================================
def send_with_guardrails(agent, question, expected_keywords_list, threshold=0.6):
    response = agent.send_message(question).text
    score = evaluate_response(response, expected_keywords_list)

    if score < threshold:
        st.warning(f"⚠️ Low confidence ({round(score * 100)}%). Asking the model to double-check...")
        follow_up = "Please double-check your answer and be more specific or cautious."
        response = agent.send_message(follow_up).text
        score = evaluate_response(response, expected_keywords_list)

    return response, score

# ========================================================================================
# 🌐 STREAMLIT APP CONFIGURATION
# ========================================================================================
st.set_page_config(page_title="Code Whisperer", page_icon="🤖")
st.title("🤖 Code Whisperer – AI Code Review Assistant")

# ========================================================================================
# ⚙️ ADVANCED GENERATION SETTINGS (Tuning Interface)
# ========================================================================================
with st.expander("⚙️ Advanced Generation Settings"):
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.3,
        help="🔁 Creativity: Lower = more focused, Higher = more diverse."
    )
    top_p = st.slider(
        "Top-p (nucleus sampling)", 0.1, 1.0, 0.95,
        help="📊 Diversity: Restricts generation to top % likely tokens."
    )
    top_k = st.slider(
        "Top-k (top tokens to sample from)", 1, 100, 40,
        help="📦 Limits next token sampling to top-k. Lower = safer output."
    )
    max_tokens = st.slider(
        "Max output tokens", 256, 2048, 1024,
        help="🧾 Max length of model output. Larger = more detailed."
    )

# ========================================================================================
# 🧠 USER TIPS FOR CONTROLLING LLM OUTPUT
# ========================================================================================
with st.expander("🧠 Tips to Improve LLM Responses"):
    st.markdown("""
- **Need precise answers?** Set **temperature = 0.0**, **top_k = 20**
- **Want creativity?** Increase **temperature to 0.7+**
- **Seeing hallucinations?** Lower **top_p** to ~0.85
- **Too short responses?** Raise **max_output_tokens** to **1024+**
""")

# ========================================================================================
# 🧠 Interaction Mode
# ========================================================================================
st.subheader("💬 How would you like to interact?")
mode = st.radio("Choose input mode:", ["Chat", "Upload file"], horizontal=True)

file_code = ""
user_question = ""

# CHAT MODE 🧑‍💻
if mode == "Chat":
    user_question = st.text_input("💬 Ask anything:")
    file_code = ""

# FILE UPLOAD MODE 📂
else:
    uploaded_file = st.file_uploader("Upload file (.py, .txt, .json, .pdf)", type=["py", "txt", "md", "json", "pdf"])
    if uploaded_file:
        file_code = handle_uploaded_file(uploaded_file)
        st.text_area("📄 File content loaded:", value=file_code, height=250)
    user_question = st.text_input("💬 Ask about the uploaded file:")

# ========================================================================================
# 🎯 Optional Evaluation
# ========================================================================================
expected_keywords = st.text_input("🔍 Expected keywords (optional, comma-separated):", placeholder="e.g. bug, readability")

# ========================================================================================
# 🚀 Ask the Assistant
# ========================================================================================
assistant = create_code_assistant(temperature, top_p, top_k, max_tokens)

if st.button("🚀 Ask Code Whisperer"):
    # Handle CHAT mode
    if mode == "Chat" and user_question.strip():
        full_input = user_question

    # Handle FILE mode
    elif mode == "Upload file" and file_code.strip() and user_question.strip():
        full_input = f"{file_code}\n\n{user_question}"

    else:
        st.warning("Please provide a question." if mode == "Chat" else "Please upload a file and enter a question.")
        st.stop()

    keywords_list = [kw.strip() for kw in expected_keywords.split(",")] if expected_keywords else []

    with st.spinner("Asking Code Whisperer..."):
        try:
            response, score = send_with_guardrails(assistant, full_input, keywords_list)
            with st.expander("📥 Code Whisperer’s Answer", expanded=True):
                st.markdown(f"```\n{response.strip()}\n```")

            if score < 0.6:
                st.error("🔴 Confidence: LOW – Review carefully")
            elif score < 0.8:
                st.warning("🟠 Confidence: MEDIUM – Double-check advised")
            else:
                st.success("🟢 Confidence: HIGH – Looks great!")

        except Exception as e:
            st.error(f"❌ API Error: {e}")

# ========================================================================================
# 📜 DISPLAYS CHAT MEMORY HISTORY
# ========================================================================================
if st.checkbox("📜 Show full conversation history"):
    if hasattr(assistant, "history"):
        for msg in assistant.history:
            try:
                # Access role and convert each part to string
                role = msg.role
                text_parts = [str(part) for part in msg.parts]  # Convert parts safely
                text = "\n".join(text_parts)

                # Display formatted chat message
                st.markdown(f"**{role.capitalize()}:** {text}")

            except Exception as e:
                st.error(f"⚠️ Error displaying message: {e}")
    else:
        st.warning("🤷‍♂️ No chat history found yet.")
