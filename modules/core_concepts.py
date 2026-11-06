import streamlit as st
from utils.tokenizer import tokenize, count_tokens
from modules.common import learning_objectives, quiz, recap

QUESTIONS = [
 {"question":"Which statement about token IDs is correct?","options":["They are universal across all models","They are integers assigned by a particular tokenizer vocabulary","They represent sentiment"],"answer":1,"explanation":"Token IDs are vocabulary-specific; different encodings can assign different IDs."},
 {"question":"What does a context window describe?","options":["The maximum amount of text/context a model can handle in one request","The number of users online","Only the generated answer length"],"answer":0,"explanation":"The context window is the model's finite working context, commonly measured in tokens."},
 {"question":"Which statement is accurate?","options":["Input and output limits are always identical","Output tokens do not use context","The output cap and context window are distinct constraints"],"answer":2,"explanation":"A model can have a total context capacity and a separate maximum output-token limit."}
]

def render():
    learning_objectives(["Compare character, word and subword tokenization.","Inspect token pieces and IDs.","Distinguish context windows from output limits.","Calculate a simple context budget."])
    st.markdown("### 1. Three ways to split text")
    a,b,c = st.columns(3)
    a.markdown('<div class="concept-card"><b>Character-level</b><p>Split into individual characters. Flexible, but sequences become long.</p></div>',unsafe_allow_html=True)
    b.markdown('<div class="concept-card"><b>Word-level</b><p>Split on word boundaries. Intuitive, but rare words create vocabulary problems.</p></div>',unsafe_allow_html=True)
    c.markdown('<div class="concept-card"><b>Subword-level</b><p>Reuse frequent fragments. Balances vocabulary size and flexibility.</p></div>',unsafe_allow_html=True)
    st.markdown("### 2. Tokenization pipeline")
    st.code("Input string → encoding rules / pre-tokenization → token pieces → vocabulary lookup → integer token IDs",language="text")
    st.write("The exact process depends on the tokenizer. This course uses `cl100k_base`, an encoding used by certain OpenAI model families. It is not a universal tokenizer.")
    sample = st.text_input("Inspect a sample", "Tokenization makes language computable.")
    try:
        details = tokenize(sample)
        st.write(f"**{len(details)} tokens**")
        st.dataframe([{"Position":i+1,"Visible piece":repr(t["piece"]),"Token ID":t["id"]} for i,t in enumerate(details)],use_container_width=True,hide_index=True)
    except Exception as exc:
        st.error(f"Tokenizer error: {exc}")
    st.markdown("### 3. Why counts differ")
    st.write("A word may be one token or several subword tokens. Whitespace and punctuation may be included in token pieces. Numbers, Unicode characters and emoji can have surprising splits. Different model families use different vocabularies and pre-tokenization rules, so counts are not interchangeable.")
    st.info("The often-quoted estimate that one token is about ¾ of an English word is only a rough planning heuristic. It is not a conversion rule.")
    st.markdown("### 4. Context window vs output limit")
    st.write("The context window is the total working space for the request and generated continuation. The output token limit is a separate cap on how many tokens the model may generate. Exact accounting and API behavior vary by model and platform.")
    st.markdown("### Context budget example")
    context = st.slider("Illustrative context window (tokens)",100,2000,1000,100)
    system = st.number_input("System instructions",0,1000,100)
    history = st.number_input("Conversation history",0,1000,350)
    prompt = st.number_input("Current user prompt",0,1000,150)
    output = st.number_input("Reserved output",0,1000,200)
    used = int(system+history+prompt+output)
    st.progress(min(used/context,1.0),text=f"{used:,} / {context:,} total budget")
    if used <= context: st.success(f"{context-used} tokens remain in this illustrative budget.")
    else: st.error(f"Over budget by {used-context} tokens. The application must decide how to respond.")
    st.caption("This is a simplified accounting model. Some systems also account for tool schemas, message framing, multimodal payloads and model-specific overhead.")
    quiz(QUESTIONS,"core_quiz")
    recap("Token IDs are tokenizer-specific. Context windows bound the combined working context; output limits are separate constraints.")
