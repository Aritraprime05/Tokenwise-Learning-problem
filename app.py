from pathlib import Path

import streamlit as st
from config import COURSE, MODULES
from utils.session import initialize_state, mark_module_complete
from modules import hook, core_concepts, tokenizer_sandbox, practical_challenge, real_world
from modules.common import render_header, render_footer

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="TokenWise | Generative AI Learning Lab", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
initialize_state()

with open(BASE_DIR / "assets" / "custom.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

PAGES = {
    "Overview": None,
    "01 · The Hook": hook.render,
    "02 · Core Concepts": core_concepts.render,
    "03 · Tokenization Sandbox": tokenizer_sandbox.render,
    "04 · Practical Challenge": practical_challenge.render,
    "05 · Real-world Applications": real_world.render,
}

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span><span>TokenWise</span></div>', unsafe_allow_html=True)
    st.caption("GENERATIVE AI LEARNING LAB")
    st.progress(st.session_state.course_progress / 5, text=f"Course progress · {st.session_state.course_progress}/5 modules")
    selected = st.radio("COURSE NAVIGATION", list(PAGES), key="course_nav", label_visibility="visible")
    st.divider()
    st.markdown("**Your learning journey**")
    for i, module in enumerate(MODULES):
        done = i in st.session_state.completed_modules
        st.markdown(f'<div class="side-module"><span class="status-dot {"done" if done else ""}"></span><span>{module["title"]}</span><small>{module["duration"]}</small></div>', unsafe_allow_html=True)
    st.divider()
    if st.button("↺ Reset course progress", use_container_width=True):
        for key in ["completed_modules", "quiz_answers", "challenge_scores", "final_answers", "final_submitted"]:
            st.session_state[key] = [] if key in ["completed_modules", "quiz_answers", "challenge_scores", "final_answers"] else False
        st.session_state.course_progress = 0
        st.rerun()
    st.caption("Built for curious minds · 45 min")

if selected == "Overview":
    render_header("Learn how AI reads, remembers and processes language.", "A hands-on course on tokenization and context window management.")
    st.markdown('<div class="hero-panel"><div class="eyebrow">THE GENERATIVE AI FOUNDATIONS SERIES</div><h1>Text goes in.<br><span>Tokens make it work.</span></h1><p>Explore the invisible layer between human language and large language models. Experiment with real tokenization, then learn to manage an AI model’s limited working context.</p></div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("Learning time", "45 min")
    b.metric("Difficulty", "Beginner")
    c.metric("Learning modules", "05")
    st.markdown("### What you'll be able to do")
    cols = st.columns(3)
    objectives = [("Understand tokens","Explain words, subwords, token IDs and encoding."),("Inspect real tokenization","Use a real tokenizer to inspect token pieces and IDs."),("Design context budgets","Fit useful instructions and history into a finite context.")]
    for col,(title,desc) in zip(cols,objectives):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">◈</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown("### Your 45-minute learning path")
    for i,m in enumerate(MODULES):
        st.markdown(f'<div class="module-row"><div class="module-number">{i+1:02}</div><div><b>{m["title"]}</b><p>{m["summary"]}</p></div><div class="module-time">{m["duration"]}</div></div>',unsafe_allow_html=True)
    st.info("Suggested pace: read, try the activity, answer the knowledge check, and note the key takeaway in each module.")
    st.button("Start learning →", type="primary", use_container_width=True,
              on_click=lambda: st.session_state.update({"course_nav": "01 · The Hook"}))
    st.markdown("### Course progress")
    st.progress(st.session_state.course_progress/5, text=f'{st.session_state.course_progress*20}% complete')
else:
    page = PAGES[selected]
    render_header(selected, MODULES[list(PAGES).index(selected)-1]["summary"])
    page()
    idx = list(PAGES).index(selected)-1
    if st.button("Mark module complete ✓", type="primary", key=f"complete_{idx}"):
        mark_module_complete(idx)
        st.success("Progress saved.")
        st.rerun()
    render_footer()
