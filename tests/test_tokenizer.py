import pytest
pytest.importorskip('tiktoken', reason='Install requirements.txt to run tokenizer integration tests')
from utils.tokenizer import count_tokens, tokenize, text_stats, decode_ids, get_encoding

def test_empty_input():
    assert count_tokens("") == 0
    assert tokenize("") == []
    assert text_stats("")["words"] == 0

@pytest.mark.parametrize("text",[
    "Hello, world!",
    "A long paragraph " * 100,
    "Numbers 123456789 and punctuation?!",
    "नमस्ते दुनिया",
    "Emoji 😀🚀☕️",
    "Special chars <>&/\\|{}[]"
])
def test_tokenizer_returns_real_ids_and_pieces(text):
    tokens = tokenize(text)
    assert len(tokens) == count_tokens(text)
    assert all(isinstance(t["id"], int) for t in tokens)
    assert all(isinstance(t["piece"], str) for t in tokens)

def test_decode_roundtrip():
    text = "TokenWise — café 🌍"
    ids = get_encoding().encode(text, disallowed_special=())
    assert decode_ids(ids) == text

def test_stats():
    stats = text_stats("one two three")
    assert stats["words"] == 3
    assert stats["tokens"] == count_tokens("one two three")
