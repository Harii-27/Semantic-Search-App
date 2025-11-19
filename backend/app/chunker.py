from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def chunk_text(text, max_tokens=500):
    tokens = tokenizer.encode(text)
    chunks=[]
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i+max_tokens]
        chunks.append(tokenizer.decode(chunk))
    return chunks
