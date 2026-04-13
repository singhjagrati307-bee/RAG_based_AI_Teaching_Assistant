## chunks convert into vectors
## cos 0=1,cos 90=0
## Embeddings- are numerical vector representations of data (like words, sentences, images, or even products) that capture their meaning or relationship in a mathematical form.
## bge-m3   = help in embeddings
## run in terminal-ollama pull bge-m3

##1)
##using Ollama’s local API to generate embeddings from the model bge-m3.


import requests

r=requests.post("http://localhost:11434/api/embeddings", json={
    "model":"bge-m3",
    "prompt":"Rishu is a good boy"
        
})

embedding=r.json()['embedding']
print(embedding[0:5])

##2) defining a function to create embeddings

import requests

def create_embedding(text):
    r=requests.post("http://localhost:11434/api/embeddings", json={
    "model":"bge-m3",
    "prompt":"Rishu is a good boy"     
    })

    embedding=r.json()['embedding']
    return embedding

a=create_embedding("cat sat on the mat")
print(a)


##3)
# Bulk Embeddings & Chunk Loading with Pandas

import requests
import os
import json
import pandas as pd

# Use your full JSON folder path
json_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\jsons"

def create_embedding(text_list):
    # Call Ollama local API to generate embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    
    # Raise error if request failed
    r.raise_for_status()
    
    embedding = r.json()["embeddings"]
    return embedding


# List all JSON files from the folder
jsons = os.listdir(json_folder)
my_dicts = []
chunk_id = 0

for json_file in jsons:
    file_path = os.path.join(json_folder, json_file)
    
    # Read the JSON file
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    
    print(f"Creating Embeddings for {json_file} ...")
    
    # Create embeddings for all text chunks in this file
    embeddings = create_embedding([c['text'] for c in content['chunks']])
    
    # Attach embeddings and chunk IDs
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)

# Convert to DataFrame
df = pd.DataFrame.from_records(my_dicts)
print(df.head())

# Optional: Save for later use
df.to_csv("all_embeddings.csv", index=False)
print("\n Embeddings saved to all_embeddings.csv")

##4)

## create embeddings from multiple JSON files
import requests
import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):
    # Create embeddings using Ollama API
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    r.raise_for_status()  # Raise error if request fails
    embedding = r.json()["embeddings"]
    return embedding

#  Use raw string or double backslashes in path
json_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\jsons"  

# Check if path exists
if not os.path.exists(json_folder):
    raise FileNotFoundError(f"Path not found: {json_folder}")

# List all JSON files
jsons = [f for f in os.listdir(json_folder) if f.endswith(".json")]
my_dicts = []
chunk_id = 0

for json_file in jsons:
    json_path = os.path.join(json_folder, json_file)
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    
    print(f"Creating embeddings for {json_file}...")
    text_chunks = [c['text'] for c in content.get('chunks', [])]
    
    if not text_chunks:
        print(f" No chunks found in {json_file}, skipping.")
        continue

    embeddings = create_embedding(text_chunks)
       
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)
    break  # Remove this if you want to process all files

# Convert to DataFrame
df = pd.DataFrame.from_records(my_dicts)

## save this dataframe 
joblib.dump(df,'embeddings.joblib')

incoming_query = input("\nAsk a Question: ")
question_embedding = create_embedding([incoming_query])[0]

# Compute cosine similarity
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

# Show top 3 results
top_results = 3
max_indx = similarities.argsort()[::-1][:top_results]
new_df = df.iloc[max_indx]

print("\nTop matching results:\n")
print(new_df[["title", "number", "text"]])