# TokenWise — 5–7 minute explanation video script

## 0:00–0:30 — Introduction
**Screen:** Open the TokenWise home page.
"Hello, my name is Aritra, and this is TokenWise, an interactive learning platform about tokenization and context window management in Generative AI. The experience is designed as a 45-minute self-learning course for beginners."

## 0:30–1:05 — Why this topic?
**Screen:** Home page learning objectives.
"I selected this topic because tokens are one of the foundations of how large language models process text, but beginners often confuse tokens with words. Context windows are equally important because a model cannot use unlimited information in a single request. Understanding both helps developers build more reliable and cost-aware AI applications."

## 1:05–1:40 — Problem statement and objectives
**Screen:** Module overview.
"The problem is that explanations of tokenization can feel abstract. TokenWise turns the topic into a sequence of short lessons, real tokenizer experiments, context-budget calculations and practical challenges. Students should be able to inspect token IDs, estimate context usage and make informed decisions about conversation history."

## 1:40–2:20 — Course structure
**Screen:** Sidebar and each module title.
"The course is divided into five modules: a five-minute introduction, ten minutes of core concepts, ten minutes in the tokenization sandbox, ten minutes of context-window challenges and ten minutes on real-world applications. The structure moves from intuition to concepts, experimentation, application and assessment."

## 2:20–3:00 — Technical architecture and tiktoken
**Screen:** Briefly show project folder in VS Code, then sandbox.
"The application is built with Python and Streamlit. The tokenizer utility uses tiktoken with the cl100k_base encoding. When a learner enters text, the application calls the real encoding to obtain token IDs. It then decodes each token's bytes for inspection. This is not a random count or a simulated tokenizer. cl100k_base is used by certain OpenAI model families, but it is not universal."

## 3:00–4:00 — Sandbox demonstration
**Screen:** Module 3. Enter a sentence, then a number, emoji or non-English phrase.
"In the sandbox, I can enter any text or load a sample. The application displays the token count, whitespace-separated word count, character count and token-to-word ratio. Each colored block represents an actual token piece, and the expandable table shows its token ID. I can experiment with punctuation, numbers and Unicode to see how the encoding segments different strings. The chart compares word count with token count."

## 4:00–5:00 — Context challenge
**Screen:** Module 4, select Level 1, edit prompt, show counter and feedback.
"The practical challenge simulates a chatbot with a limited token budget. I must shorten the request while preserving its important requirements. The feedback is transparent: the prompt must fit and include at least 60 percent of the essential phrases listed for the challenge. This is a simple rule-based teaching rubric, not a semantic AI evaluator. The goal is to learn that token efficiency should not destroy the user's intent."

## 5:00–5:45 — Real-world applications
**Screen:** Module 5 workflow and budget calculator.
"In a real chatbot, context can include system instructions, conversation history, the current user message and retrieved documents. Developers count tokens, reserve output capacity, and select or summarize relevant history. Retrieval-Augmented Generation can bring relevant external information into the current prompt. When limits are exceeded, behavior depends on the API and application; it is not always automatic truncation."

## 5:45–6:20 — Interactivity and learner outcomes
**Screen:** Quiz, glossary and progress.
"Students learn by changing inputs, observing real tokenization, solving challenges and checking their understanding. The final assessment provides explanations, and module progress is retained during the Streamlit session."

## 6:20–6:40 — Conclusion
**Screen:** Return to home page.
"TokenWise aims to make an invisible part of Generative AI visible and testable. It connects tokenizer mechanics with practical context management decisions that developers make when building AI applications. Thank you."

---

**Recording tips:** Use 1080p if available, keep browser zoom around 90–100%, hide unrelated tabs and notifications, speak at a steady pace, and show actual interactions rather than reading every paragraph. Target duration: approximately 6 minutes.
