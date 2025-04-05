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

# In[99]:


# 📦 Install the Google Generative AI SDK to access the Gemini API
#get_ipython().system('pip install google-generativeai')


# In[103]:


# 📦 Install streamlit package for the Google Generative AI SDK to access the Gemini API
#get_ipython().system('pip install streamlit google-generativeai')


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

# ========================================================================================
# 🔐 SETUP GEMINI API (uses Streamlit secrets for secure key handling)
# ========================================================================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ========================================================================================
# 🧠 PERSONALITY PROMPT: Defines assistant behavior and safe conduct rules
# ========================================================================================
PERSONALITY_PROMPT = """
You are Code Whisperer, an expert AI code assistant with deep experience in software engineering, 
performance optimization, and best practices.

Your top priority is to provide helpful and accurate responses, even if that means saying 'I don't know'.

Rules:
1. If you're unsure, say so — do NOT hallucinate.
2. Be clear, helpful, and respectful.
3. Ask for clarification when the question lacks context.
"""

# ========================================================================================
# 🧠 CREATE ASSISTANT WITH MEMORY + CUSTOM SETTINGS
# ========================================================================================
def create_code_assistant(temperature=0.3, top_p=1.0, top_k=40, max_output_tokens=1024):
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
# 💬 CHAT INTERFACE (Code or Question Input)
# ========================================================================================
st.subheader("💬 Paste code or ask a question:")
user_input = st.text_area("Input", height=200, placeholder="Paste code or ask something like 'Can you find bugs?'")

# Optional expected keywords for evaluation
expected_keywords = st.text_input("🔍 Expected keywords (comma-separated, optional)", placeholder="e.g. loop, return, bug")

# Create Gemini assistant with memory and custom generation settings
assistant = create_code_assistant(temperature, top_p, top_k, max_tokens)

# ========================================================================================
# ▶️ SUBMIT TO LLM & HANDLE RESPONSE
# ========================================================================================
if st.button("Send"):
    if user_input.strip():
        with st.spinner("💬 Thinking..."):
            try:
                keywords_list = [kw.strip() for kw in expected_keywords.split(",")] if expected_keywords else []
                response, score = send_with_guardrails(assistant, user_input, keywords_list)

                st.markdown("### 🤖 Code Whisperer says:")
                st.write(response)

                # Show confidence score
                st.markdown(f"### 🔎 Confidence Score: **{round(score * 100)}%**")

                # Hallucination alert
                if score < 0.6:
                    st.error("🚨 Possible Hallucination – Review response carefully.")
                elif score < 0.8:
                    st.warning("⚠️ Moderate confidence – Use with caution.")
                else:
                    st.success("✅ High confidence – Looks good!")

            except Exception as e:
                st.error(f"❌ Gemini API Error: {e}")
    else:
        st.warning("Please enter some input before sending.")

# ========================================================================================
# 📜 DISPLAY CHAT MEMORY HISTORY
# Includes defensive checks in case of malformed data or API quirks
# ========================================================================================
if st.checkbox("📜 Show full conversation history"):
    if hasattr(assistant, "history"):
        for msg in assistant.history:
            try:
                # Use attribute access (Gemini returns object, not dict)
                role = msg.role
                text = "\n".join(msg.parts)

                # Display message clearly formatted
                st.markdown(f"**{role.capitalize()}:** {text}")

            except Exception as e:
                # Show any error gracefully instead of crashing the app
                st.error(f"⚠️ Error displaying message: {e}")
    else:
        st.warning("🤷‍♂️ No chat history found yet.")

