import streamlit as st
from utils.tokenizer import count_tokens
from utils.context_manager import assess_prompt
from modules.common import learning_objectives, recap

CHALLENGES = [
 {"title":"Level 1 · The essentials","budget":50,"initial":"Please act as an experienced history teacher and provide a comprehensive explanation of the French Revolution, including its background, major causes, important events, influential personalities, consequences, and its impact on modern democratic societies. Make the explanation easy for middle school students to understand.","terms":["French Revolution","causes","events","consequences","middle school"]},
 {"title":"Level 2 · Keep the audience","budget":42,"initial":"Explain photosynthesis in a detailed and engaging way for a student who is new to biology. Include the role of sunlight, water, carbon dioxide, chlorophyll, glucose, and oxygen, and finish with a short everyday analogy.","terms":["photosynthesis","sunlight","water","carbon dioxide","glucose","oxygen","analogy"]},
 {"title":"Level 3 · Constrained output","budget":38,"initial":"You are a patient programming tutor. Explain binary search to a beginner, state its sorted-array requirement, walk through a small example, mention its O(log n) time complexity, and end with one common mistake to avoid.","terms":["binary search","sorted","example","O(log n)","mistake"]}
]
SAMPLES = ["Explain the French Revolution for middle school students. Cover causes, key events and consequences.",
           "Explain photosynthesis for beginners: sunlight, water, CO2, glucose and oxygen; end with an analogy.",
           "Teach binary search to a beginner with a sorted-array example, O(log n) complexity and one common mistake."]

def render():
    learning_objectives(["Calculate prompt token usage against a fixed budget.","Prioritize essential requirements when editing prompts.","Interpret transparent rule-based challenge feedback."])
    st.markdown("### Your mission")
    st.write("A chatbot has a limited context budget. Your job is to compress a request without losing the user's main goal or the essential requirements.")
    level = st.selectbox("Choose a challenge",range(3),format_func=lambda i:CHALLENGES[i]["title"])
    challenge = CHALLENGES[level]
    budget = st.slider("Context budget for this challenge",20,100,challenge["budget"],1)
    st.markdown("**Original prompt**")
    st.markdown(f'<div class="quote-card">{challenge["initial"]}</div>',unsafe_allow_html=True)
    prompt = st.text_area("Rewrite the prompt",value=st.session_state.get(f"challenge_prompt_{level}",challenge["initial"]),height=130,key=f"challenge_prompt_input_{level}")
    st.session_state[f"challenge_prompt_{level}"] = prompt
    count = count_tokens(prompt)
    remaining = budget-count
    a,b,c = st.columns(3)
    a.metric("Prompt tokens",count)
    b.metric("Budget",budget)
    c.metric("Remaining",remaining)
    st.progress(min(count/budget,1.0),text=f"{count} / {budget} tokens")
    result = assess_prompt(prompt,count,budget,challenge["terms"])
    st.caption("Scoring method: prompt must fit and include at least 60% of the explicitly listed essential phrases. This is a transparent lexical heuristic, not a semantic model or proof of quality.")
    st.write("**Essential requirements to preserve:** "+", ".join(challenge["terms"]))
    if result["passed"]:
        st.success(result["feedback"])
    else:
        st.warning(result["feedback"])
    st.write(f"Requirement coverage: {len(result['matched'])}/{len(challenge['terms'])} ({result['coverage']:.0%})")
    with st.expander("Hint"):
        st.write("Remove ceremonial wording, repeated adjectives and unnecessary role-play. Keep the task, audience, key coverage points and requested output.")
    with st.expander("Sample optimized prompt"):
        st.code(SAMPLES[level])
        st.caption(f"Sample uses {count_tokens(SAMPLES[level])} tokens with cl100k_base.")
    if st.button("Submit challenge",type="primary",key=f"submit_challenge_{level}"):
        score = (10 if result["passed"] else 0) + round(result["coverage"]*5)
        scores = st.session_state.challenge_scores
        if len(scores)<=level:
            scores.extend([0]*(level+1-len(scores)))
        scores[level] = score
        st.session_state.challenge_scores = scores
        st.success(f"Challenge score: {score}/15")
    if st.button("Reset this challenge",key=f"reset_challenge_{level}"):
        st.session_state[f"challenge_prompt_{level}"] = challenge["initial"]
        st.rerun()
    if st.session_state.challenge_scores:
        st.markdown("### Challenge scorecard")
        for i,score in enumerate(st.session_state.challenge_scores):
            st.write(f"{CHALLENGES[i]['title']}: **{score}/15**")
        st.metric("Total challenge points",sum(st.session_state.challenge_scores), "out of 45")
    st.markdown("### What happens when a context limit is exceeded?")
    st.write("There is no single universal behavior. Depending on the API and application, a request may be rejected, the application may remove or summarize older messages, or an implementation may truncate content. Do not assume every model automatically truncates.")
    recap("Good context management preserves the information needed for the task—not merely the fewest possible tokens.")
