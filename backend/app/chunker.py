from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def chunk_text(text, max_tokens=500):
    """
    Tokenize text and split into chunks of maximum tokens.
    Returns list of text chunks.
    """
    if not text or len(text.strip()) == 0:
        return []
    
    tokens = tokenizer.encode(text)
    
    if len(tokens) == 0:
        return []
    
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i+max_tokens]
        decoded_chunk = tokenizer.decode(chunk)
        # Only add non-empty chunks
        if decoded_chunk and len(decoded_chunk.strip()) > 0:
            chunks.append(decoded_chunk)
    
    return chunks
