
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