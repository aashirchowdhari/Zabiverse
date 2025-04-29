# model.py

import faiss
import json
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyAJ6XO12knSASoygKg0iiAipHGcl-qJIH8")

# Load model
model = SentenceTransformer('all-mpnet-base-v2')

# Global FAISS index and metadata
index = None
metadata = None

def initialize_resources():
    global index, metadata
    try:
        print("Initializing FAISS resources...")
        index = faiss.read_index("final_vector_database.index")
        with open("final_vector_metadata.json", "r") as f:
            metadata = json.load(f)
        print(f"FAISS and metadata loaded successfully! FAISS Index Dimension: {index.d}")
    except Exception as e:
        print(f"Error initializing FAISS resources: {e}")

def search_vector_db(query, k=5):
    query_embedding = model.encode(query).reshape(1, -1).astype('float32')
    D, I = index.search(query_embedding, k)
    results = []
    for i in range(k):
        results.append({
            'distance': D[0][i],
            'content': metadata[I[0][i]]['content'],
            'metadata': metadata[I[0][i]],
            'chunk_id': I[0][i],
            'file_name': metadata[I[0][i]].get('file_name', 'N/A')
        })
    return results

def generate_response(query, chat_history=None, k=5):
    print("\n[DEBUG] --- generate_response called ---")
    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Initial Chat History: {chat_history}")

    try:
        if chat_history is None:
            chat_history = []
            print("[DEBUG] Chat history was None; initialized to empty list.")

        # Search the vector DB
        print("[DEBUG] Performing vector search...")
        results = search_vector_db(query, k)
        print(f"[DEBUG] Retrieved {len(results)} results from FAISS.")

        if not results:
            print("[WARNING] No results returned from search_vector_db.")

        # Build context from results
        context = ""
        for i, result in enumerate(results):
            print(f"[DEBUG] Result {i+1}: Chunk ID = {result['chunk_id']}, Distance = {result['distance']}")
            context += f"Source {i+1} (Chunk ID: {result['chunk_id']}, Distance: {result['distance']}, REFERENCE: {result['file_name']}):\n{result['content']}\n\n"

        # Format prompt
        prompt = f"""
You are a helpful university assistant. Use the following context and conversation history to answer the user's question.
If the context does not contain enough information, respond politely that you're not sure.  
Cite the sources you used in your response (Source 1, Source 2, etc.). Add the reference filenames too.

## Conversation History:
{json.dumps(chat_history)}

## User Question:
{query}

## Context:
{context}

## Answer:
"""
        print("[DEBUG] Prompt prepared. Preview (first 500 chars):")
        print(prompt[:500])

        # Generate content
        print("[DEBUG] Calling Gemini model...")
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        response = gemini_model.generate_content(prompt)
        print("[DEBUG] Gemini API response received.")

        # Parse response
        if hasattr(response, 'text'):
            final_response = response.text.strip()
            print("[DEBUG] Parsed Gemini response using `.text`")
        elif hasattr(response, 'candidates') and response.candidates:
            final_response = response.candidates[0].content.strip()
            print("[DEBUG] Parsed Gemini response using `.candidates[0].content`")
        else:
            print("[ERROR] Gemini response format unexpected.")
            final_response = "Sorry, I couldn't understand the response format from the AI model."

        # Update chat history
        chat_history.append({"user": query, "bot": final_response})
        print("[DEBUG] Final Response:", final_response)
        return final_response, chat_history

    except Exception as e:
        import traceback
        print("[ERROR] Exception occurred in generate_response():", str(e))
        print(traceback.format_exc())
        return "Sorry, I encountered an internal error while processing your query.", chat_history
