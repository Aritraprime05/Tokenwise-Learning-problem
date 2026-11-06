import streamlit as st

def initialize_state():
    defaults = {"completed_modules": [], "course_progress": 0, "quiz_answers": [],
                "challenge_scores": [], "final_answers": [], "final_submitted": False}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def mark_module_complete(index: int):
    completed = set(st.session_state.completed_modules)
    completed.add(index)
    st.session_state.completed_modules = sorted(completed)
    st.session_state.course_progress = len(completed)
