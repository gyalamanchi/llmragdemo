import os
import requests

from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.environ["API_TOKEN"] #Set a API_TOKEN environment variable before running
#API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(prompt):
    payload = {
        "inputs": prompt,
        "parameters": { #Try and experiment with the parameters
            "max_new_tokens": 250,
            "temperature": 0.6,
            "top_p": 0.9,
            "do_sample": False,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']

question = "What is the population of Jacksonville, Florida?"
context = "As of the most current census, Jacksonville, Florida has a population of 1 million."
prompt = f"""Use the following context to answer the question at the end.

{context}

Question: {question}
"""

print(query(prompt))
