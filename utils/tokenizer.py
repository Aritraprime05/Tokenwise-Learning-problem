from functools import lru_cache
import tiktoken

ENCODING_NAME = "cl100k_base"

@lru_cache(maxsize=1)
def get_encoding():
    """Return the real tiktoken encoding used throughout this course."""
    return tiktoken.get_encoding(ENCODING_NAME)

def tokenize(text: str) -> list[dict]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    enc = get_encoding()
    ids = enc.encode(text, disallowed_special=())
    return [{"id": int(token_id), "piece": enc.decode_single_token_bytes(token_id).decode("utf-8", errors="replace")}
            for token_id in ids]

def count_tokens(text: str) -> int:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return len(get_encoding().encode(text, disallowed_special=()))

def decode_ids(ids: list[int]) -> str:
    return get_encoding().decode(ids)

def text_stats(text: str) -> dict:
    tokens = tokenize(text)
    words = text.split()
    return {
        "tokens": len(tokens),
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": len("".join(text.split())),
        "average_tokens_per_word": round(len(tokens) / len(words), 2) if words else 0.0,
        "token_to_word_ratio": round(len(tokens) / len(words), 2) if words else 0.0,
        "token_details": tokens,
    }
