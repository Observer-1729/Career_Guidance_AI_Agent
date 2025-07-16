import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# -- Streamlit UI --
st.set_page_config(page_title="Career Guidance Bot", page_icon="🎓")
st.title("🎓 AI Career Guidance Bot")

# -- API Key (already included directly)
api_key = "AIzaSyAk9qhvZJqyV8uGCAmhDFcU9kovX7j8WLo" # Add your own API Key

# -- Input Form --
with st.form("career_form_streamlit"):
    interests = st.text_input("👋 What subjects or fields excite you most?")
    strengths = st.text_input("💪 What are your strengths?")
    preferences = st.text_input("🧠 What type of work do you prefer?")
    goals = st.text_input("🎯 What are your learning goals?")
    education = st.selectbox("🎓 What is your current education level?", 
                             ["High school", "Diploma", "Bachelor's", "Dropout", "Other"])
    submitted = st.form_submit_button("Submit & Get Advice")

# -- Run only after form is submitted and inputs are valid --
if submitted:
    if not all([interests, strengths, preferences, goals, education]):
        st.warning("⚠️ Please fill out all the fields.")
    else:
        # st.spinner(
        #     "🤖 Making a career path suitable for you..."
        # )
        os.environ["GOOGLE_API_KEY"] = api_key
        llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.3)

        def ask_interests(state: dict) -> dict:
            state["interests"] = interests
            return state

        def ask_strengths(state: dict) -> dict:
            state["strengths"] = strengths
            return state

        def ask_preferences(state: dict) -> dict:
            state["preferences"] = preferences
            return state

        def ask_learning_goals(state: dict) -> dict:
            state["goals"] = goals
            return state

        def ask_education_level(state: dict) -> dict:
            state["education"] = education
            return state

        def generate_career_advice(state: dict) -> dict:
            prompt = (
                "You are a smart, friendly career counselor helping students find their ideal career.\n"
                "Based on the following user's inputs, suggest 1-2 best-fit career options. For each option, provide:\n"
                "1. Career name and a short description\n"
                "2. Why it fits this person\n"
                "3. Recommended degrees or certifications\n"
                "4. Key skills to master\n"
                "5. Top companies or job roles they can aim for\n"
                "6. Free or popular learning resources (platforms or courses)\n\n"
                f"User Interests: {state.get('interests')}\n"
                f"User Strengths: {state.get('strengths')}\n"
                f"Work Preferences: {state.get('preferences')}\n"
                f"Learning Goals: {state.get('goals')}\n"
                f"Education Level: {state.get('education')}\n\n"
                "Respond in a helpful and structured way. Don't repeat the inputs."
            )
            with st.spinner("🤖 Making a career path suitable for you..."):
                try:
                    response = llm.invoke([HumanMessage(content=prompt)])
                    advice = response.content.strip()
                    state["career_advice"] = advice
                    st.success("✅ Career Suggestions Ready!")
                    st.markdown("### 📋 Your Personalized Career Plan")
                    st.markdown(advice)
                except Exception as e:
                    st.error("🚫 Error while generating response. Maybe token limit exceeded or API key is invalid.")
                    st.code(str(e), language="text")
                return state

        # LangGraph setup AFTER submit
        builder = StateGraph(dict)
        builder.set_entry_point("ask_interests")
        builder.add_node("ask_interests", ask_interests)
        builder.add_node("ask_strengths", ask_strengths)
        builder.add_node("ask_preferences", ask_preferences)
        builder.add_node("ask_learning_goals", ask_learning_goals)
        builder.add_node("ask_education_level", ask_education_level)
        builder.add_node("generate_career_advice", generate_career_advice)

        builder.add_edge("ask_interests", "ask_strengths")
        builder.add_edge("ask_strengths", "ask_preferences")
        builder.add_edge("ask_preferences", "ask_learning_goals")
        builder.add_edge("ask_learning_goals", "ask_education_level")
        builder.add_edge("ask_education_level", "generate_career_advice")
        builder.add_edge("generate_career_advice", END)

        graph = builder.compile()
        graph.invoke({})  # Invoke after everything is ready
