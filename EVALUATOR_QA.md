# Evaluator Q&A — TokenWise

**1. Why did you choose this topic?**  
Tokenization and context windows are foundational to LLM applications. Developers need to understand how text becomes model inputs and how to fit relevant instructions and history within finite context limits.

**2. What is the novelty of your project?**  
The learning experience combines actual local tokenization with visible token IDs, hands-on prompt-budget challenges and a real-world chatbot memory workflow. The contribution is the instructional integration and transparent experimentation, not a new tokenizer algorithm.

**3. Why did you use tiktoken?**  
It provides actual OpenAI tokenizer encodings locally. It is lightweight for this demonstration and does not require an API key. I selected `cl100k_base` as a concrete encoding, while explicitly teaching that it is not universal.

**4. What is the difference between tokens and words?**  
Words are linguistic units; tokens are units defined by a tokenizer vocabulary and its segmentation rules. A token may be a whole word, a subword, punctuation or whitespace. One word can map to multiple tokens.

**5. What is a context window?**  
It is the finite amount of context a model can process for a request, generally measured in tokens. Depending on the model and API, accounting may include input and generated output.

**6. How does your application calculate tokens?**  
It calls `tiktoken.get_encoding("cl100k_base").encode(text, disallowed_special=())` and counts the returned IDs. The displayed IDs are the actual integers returned by that encoding.

**7. How do you manage conversation history?**  
A production application can retain recent turns, select older relevant turns, summarize older discussion, retrieve relevant stored information, and reserve output capacity. The app teaches these strategies through a simplified budget simulator.

**8. What happens when the context limit is exceeded?**  
There is no universal behavior. A provider may reject the request, or the application may select, summarize or truncate context. Developers should check model/API behavior and implement an explicit policy.

**9. How does tokenization affect API costs?**  
Many providers price usage by input and output tokens, sometimes at different rates. More tokens can increase cost and latency. Exact pricing is model- and provider-specific and should be checked at implementation time.

**10. What improvements would you make?**  
I would add tokenizer options for additional model families, persistent user accounts, instructor analytics, accessibility testing, more sophisticated context policies and human-reviewed semantic prompt evaluation.

**11. Does one token equal 0.75 words?**  
No. That is only a rough English-language planning heuristic. Actual tokenization depends on the encoding, language, punctuation, numbers and text patterns. This app measures with tiktoken instead of using that estimate.

**12. Is the challenge evaluator semantic?**  
No. It checks whether the prompt fits and includes at least 60% of required phrases. This is intentionally explainable and deterministic, but it cannot guarantee semantic preservation. The limitation is disclosed in the interface.

**13. Why is there no OpenAI API integration?**  
The assignment is to teach tokenization and context management. Local tokenization is sufficient to demonstrate the mechanism and avoids API keys, network dependency and usage charges.

**14. How is RAG related to context management?**  
RAG retrieves relevant external content and inserts selected chunks into the current model context. It helps avoid sending an entire knowledge base, but retrieved content still consumes context tokens.
