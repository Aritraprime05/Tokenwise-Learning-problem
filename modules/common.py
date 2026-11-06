import streamlit as st

def render_header(title, subtitle):
    st.markdown(f'<div class="page-kicker">TOKENWISE LEARNING PATH</div><h1 class="page-title">{title}</h1><p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-note">TOKENWISE · Learn by understanding, then learn by doing.</div>', unsafe_allow_html=True)

def learning_objectives(items):
    with st.expander("Learning objectives", expanded=True):
        for item in items:
            st.markdown(f"- {item}")

def recap(text):
    st.markdown(f'<div class="takeaway"><b>KEY TAKEAWAY</b><p>{text}</p></div>', unsafe_allow_html=True)

def quiz(questions, key_prefix):
    st.markdown("### Knowledge check")
    answers = {}
    for i,q in enumerate(questions):
        choice = st.radio(q["question"], q["options"], index=None, key=f"{key_prefix}_{i}")
        if choice is not None:
            answers[str(i)] = q["options"].index(choice)
    if st.button("Check answers", key=f"{key_prefix}_check"):
        for i,q in enumerate(questions):
            selected = answers.get(str(i))
            if selected == q["answer"]:
                st.success(f"Q{i+1}: Correct. {q['explanation']}")
            elif selected is None:
                st.warning(f"Q{i+1}: Please answer this question.")
            else:
                st.error(f"Q{i+1}: {q['explanation']}")
