import os
import time
from cosdata import Client
from sentence_transformers import SentenceTransformer

# --- CONFIG ---
GLOBAL_COLLECTION = "legal_aid_global_v1"
# Ensure this matches what works for you (http://127.0.0.1:8443 or just IP)
COSDATA_HOST = "http://127.0.0.1:8443" 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# --------------

print(f"Loading embedding model: {EMBEDDING_MODEL}...")
model = SentenceTransformer(EMBEDDING_MODEL)

def get_client():
    # Use the admin/empty password we found
    return Client(host=COSDATA_HOST, username="admin", password="")

def get_global_collection():
    client = get_client()
    try:
        existing = client.get_collection(GLOBAL_COLLECTION)
        if existing:
            return existing
    except Exception:
        pass 

    print(f"Creating GLOBAL collection: {GLOBAL_COLLECTION}")
    collection = client.create_collection(
        name=GLOBAL_COLLECTION,
        dimension=384
    )
    collection.create_index(distance_metric="cosine")
    return collection

def smart_chunker(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def index_document(full_text, session_id, doc_name="uploaded_doc"):
    # We accept session_id to ensure uniqueness
    collection = get_global_collection()
    chunks = smart_chunker(full_text)
    
    print(f"Indexing {len(chunks)} chunks for {doc_name} ({session_id})...")
    txn = collection.create_transaction()
    try:
        for i, chunk in enumerate(chunks):
            # UNIQUE ID: session_id + filename + chunk_index
            # This prevents "contract.pdf" from User A mixing with User B
            vector_id = f"{session_id}___{doc_name}___{i}"
            
            embedding = model.encode(chunk).tolist()
            
            payload = {
                "id": vector_id,
                "dense_values": embedding,
                "document_id": chunk 
            }
            txn.upsert_vector(payload)
        
        txn.commit()
    except Exception as e:
        print(f"Error during indexing: {e}")
        txn.abort()
        raise e
            
    return len(chunks)

def query_cosdata(user_question, session_id, active_doc_name, top_k=5):
    collection = get_global_collection()
    query_vec = model.encode(user_question).tolist()
    
    # We create a specific prefix to filter by
    target_prefix = f"{session_id}___{active_doc_name}"
    print(f"Searching for prefix: '{target_prefix}'...")
    
    # Retrieve more candidates because we will filter many out
    search_results = collection.search.dense(
        query_vector=query_vec,
        top_k=50 
    )
    
    final_results = []
    found_count = 0
    
    for res in search_results.get('results', []):
        vec_id = res.get('id')
        
        # --- THE SAFETY GUARD ---
        # Only accept results that belong to THIS session and THIS document
        if vec_id and str(vec_id).startswith(target_prefix):
            try:
                full_doc = collection.vectors.get(vec_id)
                text = None
                if isinstance(full_doc, dict):
                    text = full_doc.get('document_id')
                else:
                    text = getattr(full_doc, 'document_id', None)

                if text:
                    final_results.append(text)
                    found_count += 1
            except Exception as e:
                print(f"Failed to fetch {vec_id}: {e}")
        
        if found_count >= top_k:
            break
            
    return final_results
