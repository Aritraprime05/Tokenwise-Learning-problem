import streamlit as st
from modules.common import learning_objectives, quiz, recap

QUESTIONS = [
 {"question":"What is the basic unit an LLM tokenizer maps text into?","options":["A sentence","A token","A paragraph"],"answer":1,"explanation":"A tokenizer maps text into token IDs that the model can process."},
 {"question":"Is one token always one complete word?","options":["Yes","No","Only in English"],"answer":1,"explanation":"Tokens may be whole words, word fragments, whitespace or punctuation."},
 {"question":"Why tokenize text?","options":["To convert language into model-readable IDs","To make every word shorter","To translate every sentence"],"answer":0,"explanation":"Models operate on numerical token IDs, not raw human-readable strings."}
]

def render():
    learning_objectives(["Contrast human reading with machine text representation.","Define a token in plain language.","Explain why tokenization is a necessary preprocessing step."])
    st.markdown("### Start with a familiar sentence")
    st.markdown('<div class="quote-card">“I love learning about artificial intelligence.”</div>',unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        st.markdown("**How people read**")
        st.write("We recognize words, grammar, meaning and context almost instantly.")
    with right:
        st.markdown("**How a language model receives text**")
        st.write("A tokenizer converts text into a sequence of token IDs. The model processes those numerical representations.")
    st.markdown("### A useful analogy")
    st.write("Imagine a postal sorting centre. People write addresses in familiar language, but the sorting system uses standardized codes to route each item. Tokens are not meanings; they are the coded pieces used to represent text for computation.")
    st.markdown("### Try the transformation")
    text = st.text_input("Enter a short sentence", "AI reads text through tokens.")
    st.code("Human text → tokenizer → token IDs → model", language="text")
    st.caption("Open the Tokenization Sandbox in Module 3 to inspect the actual token boundaries and IDs.")
    st.markdown("### Why not feed raw words?")
    st.write("A model needs a finite vocabulary and numeric input. Subword tokenization balances vocabulary size with the ability to represent uncommon words, names and new combinations.")
    quiz(QUESTIONS,"hook_quiz")
    recap("A token is a unit chosen by a tokenizer. Tokenization turns text into numerical IDs so a language model can process it.")
