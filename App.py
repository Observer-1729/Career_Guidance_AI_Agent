import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# -- Streamlit App Title --
st.set_page_config(page_title="Career Guidance Bot", page_icon="🎓")
st.title("🎓 AI Career Guidance Bot")

# -- SET API Key Directly (⚠️ Replace YOUR_API_KEY_HERE) --
os.environ["GOOGLE_API_KEY"] = "AIzaSyAk9qhvZJqyV8uGCAmhDFcU9kovX7j8WLo"
  # Replace this with your real Gemini API key
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.3)

# -- Form for User Input --
with st.form("career_form"):
    interests = st.text_input("👋 What subjects or fields excite you? (e.g., AI, art, biology)")
    strengths = st.text_input("💪 What are your strengths? (e.g., logical thinking, creativity)")
    preferences = st.text_input("🧠 What work style do you prefer? (e.g., solo, team, remote)")
    goals = st.text_input("🎯 What are your learning goals? (e.g., job readiness, research)")
    education = st.selectbox("🎓 Your current education level", ["High School", "Diploma", "Bachelor's", "Dropout", "Other"])
    submitted = st.form_submit_button("Get Career Advice")

# -- Run LLM & Show Output --
if submitted:
    with st.spinner("🤖 Thinking... generating the best career for you..."):
        try:
            prompt = (
                "You are a smart, friendly career counselor helping students find their ideal career.\n"
                "Based on the following user's inputs, suggest 1-2 best-fit career options. For each option, provide:\n"
                "1. Career name and a short description\n"
                "2. Why it fits this person\n"
                "3. Recommended degrees or certifications\n"
                "4. Key skills to master\n"
                "5. Top companies or job roles they can aim for\n"
                "6. Free or popular learning resources (platforms or courses)\n\n"
                f"User Interests: {interests}\n"
                f"User Strengths: {strengths}\n"
                f"Work Preferences: {preferences}\n"
                f"Learning Goals: {goals}\n"
                f"Education Level: {education}\n\n"
                "Respond in a helpful and structured way. Don't repeat the inputs."
            )

            response = llm.invoke([HumanMessage(content=prompt)])
            advice = response.content.strip()

            st.success("✅ Career Suggestions Ready!")
            st.markdown("### 📋 Your Personalized Career Plan")
            st.markdown(advice)

        except Exception as e:
            st.error("🚫 Oops! Looks like your Gemini API quota has been exceeded or the key is invalid.")
            st.info("You can get a new API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and try again.")
            st.code(str(e), language="text")
