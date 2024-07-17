from dotenv import load_dotenv
load_dotenv() ## load

import os
import streamlit as st
import google.generativeai as genai

from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms import gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import SimpleDirectoryReader
genai.configure(api_key="AIzaSyB3OOe60G5hDivzp0G0m57qJ_TlW88P20U")  # Replace "YOUR_API_KEY" with your actual API key
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])
def getgemini_response(question):
    response = chat.send_message(question, stream=True)
    print(response)
    return response