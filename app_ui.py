import os
import requests
import chainlit as cl
import json


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN") #Set a API_TOKEN environment variable before running
#API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
#API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
#API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
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



@cl.on_chat_start
async def on_chat_start():
    # Sending an image with the local file path
    elements = [
    cl.Image(name="image1", display="inline", path="./IMG_0624.jpg")
    ]
    await cl.Message(content="Hello there, Welcome to AskAnyQuery related to Data!", elements=elements).send()
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # Decode the file
    text = file.content.decode("utf-8")

    texts = text

    cl.user_session.set("texts", texts)

    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()




@cl.on_message
async def main(message):
    texts = cl.user_session.get("texts")

    question = message.content 
    context = texts
    #context = "Vladimir Vladimirovich Putin[c] (born 7 October 1952) is a Russian politician and former intelligence officer who is the President of Russia. Putin has held continuous positions as president or prime minister since 1999:[d] as prime minister from 1999 to 2000 and from 2008 to 2012, and as president from 2000 to 2008 and since 2012.[e][7] He is the longest-serving Russian or Soviet leader since Joseph Stalin."
    prompt = f"""Use the following context to answer the question at the end.

    {context}

    Question: {question}
    """
    print(prompt)
    answer = query(prompt)
    print(answer)
    await cl.Message(answer).send()