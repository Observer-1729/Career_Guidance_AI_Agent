# 🎓 AI Career Guidance Bot

This is an AI-powered career guidance assistant built using **Gemini Flash**, **LangGraph**, and **Streamlit**. It helps students and professionals find the right career path by asking them about their interests, strengths, work style, learning goals, and education level — and then generates **detailed, personalized advice**.

---

## 📌 Features

- 🤖 Powered by Gemini 1.5 Flash (free-tier LLM from Google)
- 💡 Uses LangGraph (state machine for multi-step logic)
- 💬 Beautiful Streamlit web interface
- 📋 Detailed career suggestions: careers, skills, certs, companies, resources
- 🔐 Gemini API key handled securely via environment variable
- 🚫 Graceful error handling if quota is exceeded

---

## 📥 Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
▶️ How to Run
Install dependencies (if not already installed):

```bash
pip install -r requirements.txt
```

Set your Gemini API key

Open the code file and replace this line:

```python

os.environ["GOOGLE_API_KEY"] = "your-api-key-here"
```

Run the app

```bash

streamlit run App.py
```
