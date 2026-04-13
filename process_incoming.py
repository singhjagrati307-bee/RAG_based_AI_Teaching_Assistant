## Using Joblib to save dataframe
1)
## create embeddings from multiple JSON files
import requests
import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from read_chunks import create_embeddings

df =  joblib.load('embeddings.joblib')



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



#2)


import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding


df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
print(similarities)
top_results = 3
max_indx = similarities.argsort()[::-1][0:top_results]
print(max_indx)
new_df = df.loc[max_indx] 
print(new_df[["title", "number", "text"]])


##3)
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding


df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 30
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx] 
# print(new_df[["title", "number", "text"]])

for index, item in new_df.iterrows():
    print(index, item["title"], item["number"], item["text"], item["start"], item["end"])



##4)


import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding


df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 30
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx] 
# print(new_df[["title", "number", "text"]])

prompt= f'''In the manufacturing process machining lecture series by professor Joyjeet Ghose sir Here are video chunks containing video title,video number,start time in seconds, end time in seconds, the text at that at that time:

{new_df[["title","number","start","end","text"]].to_json()}

-------------------------------------

"{incoming_query}"
user asked this question related to the video chunks,you have to answer where and how much content is taught where (in which video and at what time stamp) and guide the user to go to that particular video. if user asks unrelated question ,tell him that you can only answer related to the course '''


with open ("prompt.txt","w") as f:
    f.write(prompt)
# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])


## 5) 
## getting responses from the LLM


import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx] 
# print(new_df[["title", "number", "text"]])

prompt = f'''In the manufacturing process machining lecture series by professor Joyjeet Ghose sir Here are video. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
user asked this question related to the video chunks,you have to answer where and how much content is taught where (in which video and at what time stamp) and guide the user to go to that particular video. if user asks unrelated question ,tell him that you can only answer related to the course
'''
with open("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]
print(response)

with open("response.txt", "w") as f:
    f.write(response)
# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])



## 6)

import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests
from openai import OpenAI
import os
from config import api_key

api_key="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"

client = OpenAI(api_key=api_key)



def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

def inference_openai (prompt):
    response = client.response.create()
    model="gpt-5",
    input= prompt
    return response.output_text
                  

df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx] 
# print(new_df[["title", "number", "text"]])

prompt = f'''In the manufacturing process machining lecture series by professor Joyjeet Ghose sir Here are video. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
user asked this question related to the video chunks,you have to answer where and how much content is taught where (in which video and at what time stamp) and guide the user to go to that particular video. if user asks unrelated question ,tell him that you can only answer related to the course
'''
with open("prompt.txt", "w") as f:
    f.write(prompt)

# response = inference(prompt)["response"]
# print(response)
response = inference_openai(prompt)

with open("response.txt", "w") as f:
    f.write(response)
# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])





import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
from openai import OpenAI
import os

# ✅ Load API key safely
from config import api_key  # make sure config.py contains: api_key = "sk-..."

import os
api_key = os.getenv("OPENAI_API_KEY")
client =OpenAI 
api_key="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"


def create_embedding(text_list):
    """Generate embedding using Ollama API."""
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    r.raise_for_status()
    return r.json()["embeddings"]


def inference(prompt):
    """Use Ollama (local model) for inference."""
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    r.raise_for_status()
    return r.json()["response"]


def inference_openai(prompt):
    """Use OpenAI API (GPT-5) for inference."""
    response = client.responses.create(   # ✅ corrected API method
        model="gpt-5",
        input=prompt
    )
    return response.output_text           # ✅ returns text result


# ✅ Load precomputed embeddings
df = joblib.load('embeddings.joblib')

incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]

# ✅ Compute cosine similarity
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
top_results = 5
max_indx = similarities.argsort()[::-1][:top_results]
new_df = df.loc[max_indx]

# ✅ Construct prompt
prompt = f'''
In the manufacturing process machining lecture series by Professor Joyjeet Ghose sir,
here are video subtitle chunks (title, number, start time, end time, text):

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

---------------------------------
User asked: "{incoming_query}"

Please answer:
1. In which video(s) and timestamps the topic is discussed.
2. How much content covers it.
3. If unrelated, politely say it’s outside the course.
'''

# ✅ Save prompt for reference
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

# ✅ Choose which inference to use
# response_text = inference(prompt)              # Local (Ollama)
response_text = inference_openai(prompt)         # OpenAI GPT-5

print("\n=== RESPONSE ===\n", response_text)

# ✅ Save response
with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response_text)






import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests
from openai import OpenAI
import os

# Your API key
api_key = "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"

client = OpenAI(api_key=api_key)

def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
         "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

def inference_openai(prompt):
    """Fixed OpenAI function to properly call GPT-4o (GPT-5 not yet available)"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o as GPT-5 is not yet available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about manufacturing process machining lectures. You should guide users to specific video content and timestamps when relevant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Sorry, I encountered an error while processing your request."

def main():
    # Load the embeddings dataframe
    df = joblib.load('embeddings.joblib')
    incoming_query = input("Ask a Question: ")
    question_embedding = create_embedding([incoming_query])[0] 

    # Find similarities of question_embedding with other embeddings
    similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
    
    top_results = 5
    max_indx = similarities.argsort()[::-1][0:top_results]
    new_df = df.loc[max_indx] 

    prompt = f'''In the manufacturing process machining lecture series by professor Joyjeet Ghose sir Here are video. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
user asked this question related to the video chunks,you have to answer where and how much content is taught where (in which video and at what time stamp) and guide the user to go to that particular video. if user asks unrelated question ,tell him that you can only answer related to the course
'''
    
    # Save prompt to file
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    # Use OpenAI instead of local LLM for better quality
    response = inference_openai(prompt)
    print(f"\nResponse: {response}")

    # Save response to file
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response)
        if __name__ == "__main__":
          main()