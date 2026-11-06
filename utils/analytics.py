import pandas as pd

def comparison_frame(word_count: int, token_count: int) -> pd.DataFrame:
    return pd.DataFrame({"Unit": ["Whitespace-separated words", "cl100k_base tokens"],
                         "Count": [word_count, token_count]})

def token_piece_insight(piece: str) -> str:
    if not piece:
        return "This token has no visible text when decoded with replacement handling."
    if piece.isspace():
        return "Whitespace can be represented as part of a token; it is not always separate."
    if any(ord(ch) > 127 for ch in piece):
        return "Unicode characters may require multiple bytes and can map to one or several tokens."
    if piece.isdigit():
        return "Numbers can split into multiple tokens depending on their digit pattern and encoding."
    if piece.isalpha():
        return "Subword pieces are common: frequent fragments may be represented separately from a full word."
    return "Punctuation and symbols can be attached to neighboring text or represented as their own token."
