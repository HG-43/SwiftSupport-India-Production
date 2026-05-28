import json
import os
import numpy as np
from openai import OpenAI

# --- HARDENED API KEY GATEWAY RETRIEVAL ---
api_key = os.environ.get("OPENROUTER_API_KEY")

# Automatically pull from your local Streamlit secrets file if running standalone
if not api_key and os.path.exists(os.path.join(".streamlit", "secrets.toml")):
    try:
        with open(os.path.join(".streamlit", "secrets.toml"), "r", encoding="utf-8") as f:
            for line in f:
                if "OPENROUTER_API_KEY" in line and "=" in line:
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
                    break
    except Exception as e:
        print(f"Note: Could not parse local secrets.toml file: {e}")

if not api_key or api_key == "placeholder_key":
    print("❌ Error: OPENROUTER_API_KEY is missing. Please check your secrets.toml configuration.")
    st.stop() if "st" in globals() else exit()

# OpenRouter utilizes structured namespace routes for OpenAI embedding endpoints
EMBEDDING_MODEL = "openai/text-embedding-3-small"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def chunk_text(text, max_chars=300):
    """Splits a document cleanly by sentences or logical boundaries."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_embeddings():
    if not os.path.exists("core_policy.txt"):
        print("❌ Error: core_policy.txt not found in this working directory.")
        return

    with open("core_policy.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 1. Semantic Chunking
    chunks = chunk_text(raw_text)
    print(f"✨ Generated {len(chunks)} structural context chunks.")

    vector_database = []

    # 2. Vector Generation Loop
    for i, chunk in enumerate(chunks):
        print(f"Vectorizing chunk {i+1}/{len(chunks)}...")
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=chunk
            )
            embedding = response.data[0].embedding
            
            vector_database.append({
                "id": i,
                "text": chunk,
                "vector": embedding
            })
        except Exception as e:
            print(f"❌ Failed to generate embedding for chunk {i}: {e}")
            return

    # 3. Commit to Storage (Fixed parameter typo here)
    with open("vector_store.json", "w", encoding="utf-8") as f:
        json.dump(vector_database, f, ensure_ascii=False, indent=2)
    print("🚀 Success: Vector database written cleanly to vector_store.json!")

if __name__ == "__main__":
    generate_embeddings()