import streamlit as st
from utils.tokenizer import count_tokens
from utils.quiz_engine import grade_quiz
from modules.common import learning_objectives, recap

QUESTIONS = [
 {"question":"Why might a chatbot summarize older turns?","options":["To preserve useful information while reducing context usage","To increase token count","To change the user's identity"],"answer":0,"explanation":"A summary can retain key facts and decisions in fewer tokens, though details may be lost."},
 {"question":"What is RAG commonly used for?","options":["To retrieve relevant external information and provide it as model context","To make a context window infinite","To replace tokenization"],"answer":0,"explanation":"Retrieval-Augmented Generation retrieves relevant chunks and includes them in the prompt."},
 {"question":"Which is a sound context-management strategy?","options":["Keep every message forever","Select relevant history and reserve output capacity","Ignore system instructions"],"answer":1,"explanation":"Relevance filtering and output reservation help keep requests within limits."},
 {"question":"How does tokenization affect API pricing?","options":["Pricing may depend on input and output token usage","Only character count matters","All tokenizers cost the same"],"answer":0,"explanation":"Many APIs price input and output tokens separately; exact prices depend on provider and model."},
 {"question":"What is a context window?","options":["A limit on the model's working context measured in tokens","A browser window","Only the system prompt"],"answer":0,"explanation":"The context includes instructions, supplied history and current input, plus generated output within the model's constraints."}
]

def render():
    learning_objectives(["Explain why context management matters in deployed chatbots.","Compare history selection, summarization and RAG.","Trace a practical message-selection workflow.","Evaluate understanding with a final assessment."])
    st.markdown("### A chatbot's working memory")
    st.write("A chatbot application often stores a longer conversation than it sends to the model on every turn. Before a request, the application chooses what context to include.")
    st.code("User message → Conversation history → Token counting → Context budget check → Select / summarize → LLM input",language="text")
    st.markdown("### Try a conversation budget")
    window = st.slider("Model context window (illustrative)",500,8000,4000,500)
    system = st.number_input("System instruction tokens",0,3000,250,key="rw_system")
    history = st.number_input("History tokens",0,8000,2200,key="rw_history")
    current = st.number_input("Current message tokens",0,3000,350,key="rw_current")
    retrieved = st.number_input("Retrieved RAG context tokens",0,4000,500,key="rw_rag")
    reserve = st.number_input("Reserved output tokens",0,4000,700,key="rw_reserve")
    total = int(system+history+current+retrieved+reserve)
    st.progress(min(total/window,1.0),text=f"{total} / {window} tokens")
    if total<=window: st.success(f"{window-total} tokens remain.")
    else: st.error(f"Over budget by {total-window}. Reduce or select context before sending.")
    st.markdown("### Common strategies")
    strategies = [
      ("History selection","Keep recent turns and older turns that are relevant to the current request."),
      ("Summarization","Compress older discussion into a compact memory. Summaries can omit nuance, so retain critical facts carefully."),
      ("Retrieval-Augmented Generation","Store documents or conversation knowledge externally, retrieve relevant chunks, then include those chunks in the current prompt."),
      ("Token-aware budgeting","Count with the target model's tokenizer and reserve capacity for the expected answer."),
      ("Truncation policy","If needed, remove content deliberately and transparently; do not silently discard critical instructions.")
    ]
    for title,desc in strategies:
        with st.expander(title):
            st.write(desc)
    st.markdown("### Real-world scenario: a study assistant")
    st.write("A student has a 30-turn tutoring conversation. The latest question concerns recursion. The application can keep the system instruction, the latest relevant recursion discussion, a short summary of the student's level and one retrieved course-note excerpt. It can omit unrelated earlier small talk and reserve tokens for the explanation.")
    st.markdown("### Final knowledge assessment")
    answers = {}
    for i,q in enumerate(QUESTIONS):
        selected = st.radio(q["question"],q["options"],index=None,key=f"final_q_{i}")
        if selected is not None: answers[str(i)] = q["options"].index(selected)
    if st.button("Submit final assessment",type="primary"):
        result = grade_quiz(QUESTIONS,answers)
        st.session_state.final_submitted = True
        st.session_state.final_result = result
    if st.session_state.get("final_submitted") and st.session_state.get("final_result"):
        result = st.session_state.final_result
        st.metric("Final score",f'{result["score"]}/{result["total"]}',f'{result["percentage"]}%')
        st.success("Course assessment passed." if result["percentage"]>=70 else "Review the explanations and try again.")
        st.write(f'Correct: {result["score"]} · Incorrect: {result["total"]-result["score"]}')
        for item in result["correct"]:
            st.success(f'Correct: {item["question"]} — {item["explanation"]}')
        for item in result["incorrect"]:
            st.error(f'Incorrect: {item["question"]} Correct answer: {item["correct_answer"]}. {item["explanation"]}')
    st.markdown("### Glossary")
    terms = {"Token":"A unit produced by a tokenizer and represented by a token ID.","Encoding":"A tokenizer vocabulary and set of rules mapping text to IDs.","Context window":"The model's finite working context, commonly measured in tokens.","Output token limit":"A separate cap on generated output tokens.","RAG":"Retrieval-Augmented Generation: retrieving relevant information and supplying it as model context.","Summarization":"Compressing longer content into a shorter representation that preserves selected information."}
    for term,definition in terms.items():
        st.markdown(f"**{term}:** {definition}")
    recap("A production chatbot manages context intentionally: select relevant history, summarize when appropriate, retrieve useful knowledge and reserve output capacity.")
