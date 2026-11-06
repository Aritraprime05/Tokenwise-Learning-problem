import streamlit as st
import plotly.express as px
from utils.tokenizer import tokenize, text_stats
from utils.analytics import comparison_frame, token_piece_insight
from modules.common import learning_objectives, recap

SAMPLES = {
 "Short sentence":"Hello, world! Tokenization is interesting.",
 "Numbers & punctuation":"In 2026, version 3.14 costs $19.99 — really?",
 "Unicode & emoji":"नमस्ते! Café ☕️ — こんにちは 🌍",
 "Longer paragraph":"Large language models do not read text exactly as people do. A tokenizer converts text into a sequence of token IDs. The model processes those IDs within a limited context window, which may include instructions, conversation history and the current request.",
 "Code-like text":"def greet(name):\\n    return f'Hello, {name}!'"
}

def render():
    learning_objectives(["Tokenize arbitrary text with a real encoding.","Inspect token pieces and their exact IDs.","Compare token counts with whitespace-separated words.","Notice how punctuation, numbers and Unicode affect tokenization."])
    st.markdown("### Tokenization playground")
    choice = st.selectbox("Load an experiment",["Write your own"]+list(SAMPLES))
    default = "" if choice=="Write your own" else SAMPLES[choice]
    text = st.text_area("Text input",value=default,height=150,placeholder="Type or paste any text…")
    try:
        stats = text_stats(text)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Tokens",stats["tokens"])
        m2.metric("Words",stats["words"])
        m3.metric("Characters",stats["characters"])
        m4.metric("Tokens / word",stats["token_to_word_ratio"])
        st.caption("Encoding: cl100k_base · Counts are computed locally with tiktoken.")
        st.markdown("### Token stream")
        if stats["token_details"]:
            palette = ["#b8d8ff","#d7c7ff","#bdebdc","#ffe2ae","#ffc9d4"]
            blocks = []
            for i,t in enumerate(stats["token_details"]):
                piece = t["piece"]
                safe = piece.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace(" ","·").replace("\\n","↵")
                blocks.append(f'<span class="token-chip" style="background:{palette[i%len(palette)]};color:#172033" title="Token ID: {t["id"]}">{safe or "∅"}<small>#{i+1}</small></span>')
            st.markdown('<div class="token-stream">'+"".join(blocks)+'</div>',unsafe_allow_html=True)
            with st.expander("Inspect token IDs and exact decoded pieces"):
                st.dataframe([{"Position":i+1,"Token piece":repr(t["piece"]),"Token ID":t["id"],"UTF-8 bytes":len(t["piece"].encode("utf-8"))} for i,t in enumerate(stats["token_details"])],use_container_width=True,hide_index=True)
            selected = st.selectbox("Explore why a token looks this way",range(len(stats["token_details"])),format_func=lambda i:f"#{i+1}: {stats['token_details'][i]['piece']!r}")
            st.info(token_piece_insight(stats["token_details"][selected]["piece"]))
        else:
            st.info("Enter text above to see token pieces.")
        st.markdown("### Word count vs token count")
        frame = comparison_frame(stats["words"],stats["tokens"])
        fig = px.bar(frame,x="Unit",y="Count",text="Count",color="Unit",color_discrete_sequence=["#8bb8ff","#b69cff"])
        fig.update_layout(height=300,showlegend=False,margin=dict(l=10,r=10,t=20,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig,use_container_width=True)
        st.caption("Word count here means whitespace-separated chunks. It is a simple comparison, not a linguistic word parser.")
        st.markdown("### Experiment prompts")
        st.write("Try a long number, repeated punctuation, a URL, an emoji sequence, a non-English sentence, or a word you invented. Compare how the token pieces change.")
    except Exception as exc:
        st.error(f"Could not tokenize this input: {exc}")
    recap("The token count is determined by the chosen encoding, not by counting visible words. Always measure with the tokenizer used by the target model.")
