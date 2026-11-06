# TokenWise — Tokenization & Context Window Learning Lab

A 45-minute, self-paced interactive learning experience for beginners exploring how large language models process text and manage limited context.

## Problem statement

People often think language models read whole words and remember an entire conversation. In practice, model inputs are represented as tokenizer-specific token IDs, and models operate within finite context constraints. Learners need a safe environment to inspect real tokenization and experiment with context budgets.

## Objectives

- Explain tokens, subword segmentation, token IDs and tokenizer-specific behavior.
- Demonstrate real `cl100k_base` tokenization locally with `tiktoken`.
- Distinguish total context capacity from output-token limits.
- Practice editing prompts under a token budget while preserving required intent.
- Explain history selection, summarization, retrieval-augmented generation and token-aware budgeting.

## Features

- Five paced modules (5 + 10 + 10 + 10 + 10 minutes).
- Real local tokenizer: `tiktoken.get_encoding("cl100k_base")`.
- Token-piece display, token IDs, word/character statistics and Plotly comparison chart.
- Context-budget calculators and three prompt challenges.
- Rule-based transparent challenge scoring.
- Final assessment, glossary and progress tracking.
- No OpenAI API key or network inference required.

## Technology stack

Python 3.10+, Streamlit, tiktoken, Plotly, Pandas and pytest.

## Folder structure

```text
tokenization-learning-platform/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── VIDEO_SCRIPT.md
├── EVALUATOR_QA.md
├── SUBMISSION_CHECKLIST.md
├── assets/custom.css
├── modules/
│   ├── common.py
│   ├── hook.py
│   ├── core_concepts.py
│   ├── tokenizer_sandbox.py
│   ├── practical_challenge.py
│   └── real_world.py
├── utils/
│   ├── tokenizer.py
│   ├── analytics.py
│   ├── context_manager.py
│   ├── quiz_engine.py
│   └── session.py
└── tests/
    ├── test_tokenizer.py
    ├── test_context_manager.py
    └── test_quiz_engine.py
```

## Installation (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Extract the ZIP and open the project folder in VS Code.
3. Create a virtual environment:

   ```powershell
   py -3.10 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

   `tiktoken` may download its encoding data on first use. Run once while connected to the internet if it is not already cached.

5. Start the application:

   ```powershell
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## How tokenization works

The sandbox calls the actual `cl100k_base` encoding from tiktoken. `encode()` returns integer vocabulary IDs. The app decodes each ID's token bytes individually for a human-readable inspection view. Individual pieces are shown with UTF-8 replacement handling where a token boundary splits a multibyte sequence; the token ID and count remain those returned by the encoding.

`cl100k_base` is used by certain OpenAI model families; it is not universal. Different models and providers can use different encodings and token counts. The app permits special-token-looking strings as ordinary text by calling `encode(..., disallowed_special=())`.

Word count is whitespace-separated chunks, included only as a simple comparison. The 0.75-word-per-token estimate is not used for calculation.

## How context window management works

The budget simulator adds system instruction tokens, history tokens, current prompt tokens, and reserved output tokens. Remaining capacity is:

`context window − system − history − current prompt − reserved output`

This is an educational simplified accounting model. Real APIs may include message framing, tool definitions, multimodal payloads and provider-specific rules. The output cap is distinct from total context capacity. When a request exceeds constraints, actual behavior depends on the API and application; it may reject, select, summarize or truncate content.

The challenge scorer checks whether the prompt fits and whether at least 60% of listed essential phrases are present. It is intentionally transparent and lexical—not semantic evaluation. A high score does not prove the prompt preserves meaning perfectly.

## Testing

Install requirements, then run:

```powershell
pytest -q
```

Tests cover empty text, English, long paragraphs, punctuation, numbers, Unicode, emoji, token IDs, decoding, context budget arithmetic, challenge evaluation and quiz scoring.

## Screenshots

Add screenshots after running the app:

- `screenshots/01-home.png` — course overview
- `screenshots/02-token-sandbox.png` — actual token pieces and IDs
- `screenshots/03-context-challenge.png` — budget challenge
- `screenshots/04-final-assessment.png` — final assessment

## Learning plan

| Module | Duration | Focus |
|---|---:|---|
| 1. The Hook | 5 min | Why AI uses tokens |
| 2. Core Concepts | 10 min | Token types, IDs and context |
| 3. Tokenization Sandbox | 10 min | Real tokenizer experimentation |
| 4. Practical Challenge | 10 min | Fit prompts into a budget |
| 5. Real-world Applications | 10 min | Memory, summarization and RAG |

## Limitations and future enhancements

- The app uses `cl100k_base` for demonstration, not every model's tokenizer.
- The challenge evaluator is a transparent phrase-coverage heuristic, not an LLM judge.
- Context accounting is simplified and does not model provider-specific message overhead.
- Progress is stored in Streamlit session state and is not a permanent user account.
- Future work: add model-specific tokenizer selection, persistent learner profiles, instructor analytics, accessibility testing, and a richer semantic rubric with human review.

## Responsible use

This is an educational simulator, not a live model API client. Token counts are exact for the selected encoding and input text; context behavior and pricing vary by deployed model and provider.
