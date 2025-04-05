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


# In[103]:


# 📦 Install streamlit package for the Google Generative AI SDK to access the Gemini API



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

# In[105]:


# 🧠 Import the Google Generative AI SDK to use Gemini models
import google.generativeai as genai

# 🧠 Import streamlit SDK
import streamlit as st

# 🧠 Configure the Gemini API with your secure secret key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# In[107]:


# 🧠 Define the system prompt that sets Code Whisperer's personality and behavior
# This prompt helps guide the model toward accurate, cautious, and mentor-like responses
# 🧠 Guardrails prompt

PERSONALITY_PROMPT = """
You are Code Whisperer, an expert AI code assistant with deep experience in software engineering, 
performance optimization, and best practices.

Your top priority is to provide helpful and accurate responses, **even if that means saying 'I don't know' or asking the user for clarification.**

Rules:
1. If you are unsure or lack enough context, say so — do NOT guess or make up an answer.
2. Prioritize clarity, truthfulness, and transparency over sounding smart.
3. If a question is vague or open-ended, ask a follow-up before answering.
4. Use clear reasoning to support your answers and cite assumptions when needed.

Always act as a respectful, supportive mentor.
"""


# In[74]:


# 🤖 Function to create an interactive code review assistant (Code Whisperer)
# This initializes a chat session with memory using the Gemini 2.0 Flash model

def create_code_assistant(code_snippet, agent_name="Code Whisperer", temperature=0.3, top_p=1.0, top_k=40, max_output_tokens=512):
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens
        )
    )
    
    # 🧠 Personalize the intro prompt and include the user's code
    full_intro_prompt = PERSONALITY_PROMPT + f"\n\nCode to analyze:\n{code_snippet}"

    # 💬 Start the interactive chat with memory
    convo = model.start_chat(history=[
        {"role": "user", "parts": [full_intro_prompt]},
        {"role": "model", "parts": ["Hi! I'm Code Whisperer. Ask me anything about the code above."]}
    ])

    # 🚀 Return the interactive chat session (agent ready for questions)
    return convo


# In[76]:


# 🎛️ Generation configuration — users can adjust these to experiment
temperature = 0.2        # Controls randomness (0.0 = deterministic, 1.0 = creative)
top_p = 0.95             # Controls nucleus sampling (range: 0–1)
top_k = 40               # Limits to top-k most likely tokens
max_output_tokens = 256 # Limits response length

# 👤 Agent name (just for flavor)
agent_name = "Code Whisperer"

# 🌐 Streamlit Interface
st.set_page_config(page_title="Code Whisperer", page_icon="🤖")
st.title("🤖 Code Whisperer – Your AI Code Review Buddy")
# In[78]:
# 🛡️ Keyword-based scoring + retry if confidence is low
def safe_send_message(agent, question, expected_keywords, threshold=0.6):
    response = agent.send_message(question).text
    response_lower = response.lower()
    hits = sum(1 for kw in expected_keywords if kw in response_lower)
    score = hits / len(expected_keywords)

    if score < threshold:
        follow_up = "Can you double-check your answer and be more specific or cautious?"
        response = agent.send_message(follow_up).text

    return response, score

# 📊 Score formatting
def format_score(score):
    flag = "🟩 Accurate" if score > 0.7 else "🟨 Possible Hallucination"
    return f"{round(score * 100)}% – {flag}"
    

# 🧾 Paste code
code_input = st.text_area("Paste your Python code here:", height=200, value=
"""def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True""")

# 💬 Ask a question
question = st.text_input("Ask a question about your code:", placeholder="e.g. Are there any bugs?")

# 🎛️ Generation Controls
with st.expander("🔧 Advanced Generation Settings"):
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)
    top_p = st.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.95)
    top_k = st.slider("Top-k (top tokens to sample from)", 1, 100, 40)
    max_output_tokens = st.slider("Max output tokens", 256, 2048, 1024)

# ✅ Expected keywords (for scoring)
expected_keywords = st.text_input("Expected keywords (comma-separated):", value="prime,check,number")

# ▶️ Run on submit
if st.button("Run Analysis"):
    if not code_input.strip() or not question.strip():
        st.warning("Please provide both code and a question.")
    else:
        st.info("Evaluating with Code Whisperer...")

        # Create the assistant with user-defined generation settings
        assistant = create_code_assistant(
            code_snippet=code_input,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens
        )

        # Ask the custom question
        response, score = safe_send_message(
            assistant,
            question,
            [kw.strip().lower() for kw in expected_keywords.split(",")] if expected_keywords else []
        )

        # Display result
        st.markdown("### 💡 Response:")
        st.write(response)

        st.markdown("### 📊 Evaluation:")
        st.success(format_score(score))



# ✅ Define a small evaluation set to test how well the agent answers code-related questions
# Each item includes:
# - A code snippet
# - A question to ask about that code
# - A list of expected keywords that should appear in a good response

evaluation_set = [
    {
        "code": "def add(x, y): return x + y",  # ➕ Simple addition function
        "question": "What does this function do?",
        "expected_keywords": ["adds", "two", "numbers"]
    },
    {
        "code": "def foo(): pass",  # 💤 Placeholder / no-op function
        "question": "What does this function do?",
        "expected_keywords": ["does nothing", "placeholder", "no-op"]
    }
]


def evaluate_agent_response(agent, question, expected_keywords):
    response = agent.send_message(question).text.lower()
    hits = sum(1 for word in expected_keywords if word in response)
    return hits / len(expected_keywords), response


# 🧪 Example code snippet to be reviewed by the agent
# This function checks whether a number is prime

code_snippet = """
def is_prime(n):
    if n <= 1:
        return False  # Not prime if less than or equal to 1
    for i in range(2, int(n**0.5)+1):  # Loop from 2 to sqrt(n)
        if n % i == 0:
            return False  # Not prime if divisible by any number in range
    return True  # Return True if no divisors found
"""

# 📊 Evaluate the agent's responses to a set of questions
# This function checks how well the agent's answers align with expected keywords

def evaluate_agent(assistant, questions_set):
    results = []  # Store evaluation results here

    for q in questions_set:
        question = q["question"]
        expected_keywords = q["expected_keywords"]

        # 💬 Send the question to the agent and convert response to lowercase for matching
        response = assistant.send_message(question).text.lower()

        # ✅ Count how many expected keywords appear in the response
        hits = sum(1 for word in expected_keywords if word in response)
        score = hits / len(expected_keywords)  # Calculate a simple accuracy score

        # 🧾 Store the results in a dictionary
        results.append({
            "question": question,
            "response": response,
            "score": round(score * 100, 2)  # Convert to percentage
        })

    return results  # 📤 Return the list of scored results


# 📋 Define a set of test questions for evaluating the agent on a single code snippet
# Each question includes a list of expected keywords that should appear in a good response

questions_to_test = [
    {
        "question": "What does this function do?",  # 🔍 Understanding the overall purpose
        "expected_keywords": ["check", "prime", "number"]
    },
    {
        "question": "How can it be improved?",  # 🛠 Suggestions for optimization or clarity
        "expected_keywords": ["optimize", "early return", "edge cases"]
    },
    {
        "question": "What's the time complexity?",  # ⏱ Assessing algorithm efficiency
        "expected_keywords": ["o(sqrt(n))", "efficiency", "complexity"]
    },
    {
        "question": "Can you make it more readable?",  # 📚 Code clarity and readability
        "expected_keywords": ["variable", "comment", "readability"]
    },
    {
        "question": "Are there any bugs?",  # 🐞 Bug detection and edge case handling
        "expected_keywords": ["bug", "none", "error", "issue"]
    }
]



# 🛡️ Safe response handler: sends a question to the agent and triggers a retry if confidence is low
# This adds an extra layer of protection against hallucinations

def safe_send_message(agent, question, expected_keywords, threshold=0.6):
    # 💬 Send the question to the agent and get the response
    response = agent.send_message(question).text
    response_lower = response.lower()  # Normalize text for keyword matching

    # ✅ Count how many expected keywords are present in the response
    hits = sum(1 for kw in expected_keywords if kw in response_lower)
    score = hits / len(expected_keywords)

    # ⚠️ If confidence score is below threshold, ask Gemini to clarify its answer
    if score < threshold:
        print(f"⚠️ Low confidence ({round(score*100)}%). Asking Gemini to clarify...")
        follow_up = "Can you double-check your answer and be more specific or cautious?"
        response = agent.send_message(follow_up).text

    return response  # 📤 Return the final (possibly revised) response



# 📊 Nicely format and display the result of an agent response evaluation
# This makes my notebook output clean and readable

def format_result(question, response, score):
    # ✅ Set a label based on the score: accurate or possible hallucination
    flag = "🟩 Accurate" if score > 0.7 else "🟨 Possible Hallucination"

    # 🖨️ Display the evaluation result in a readable, structured format
    print(f"💬 Question: {question}")
    print(f"🤖 Response: {response}")
    print(f"🔎 Score: {round(score*100)}% – {flag}")
    print("-" * 80)


# 🧠 Create the assistant with the target code snippet
assistant = create_code_assistant(code_snippet)

# 🚀 Loop through all test questions and evaluate the agent's performance
for item in questions_to_test:
    question = item["question"]
    expected = item["expected_keywords"]

    # 🛡️ Get the response with hallucination protection
    response = safe_send_message(assistant, question, expected)

    # 📊 Score the response again (for display)
    hits = sum(1 for kw in expected if kw in response.lower())
    score = hits / len(expected)

    # 🖥️ Format and display the result
    format_result(question, response, score)
