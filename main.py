from google import genai
from google.genai import types

import streamlit as st
import os

client = genai.Client(api_key='AIzaSyAwqzM4PEubbClKu0waIBmSW4RNmevTLz4')


print(response.text)

st.header('Augustus')

user_prompt = st.text_input('Preguntale a Augustus sobre cualquier tema de Propiedad Horizontal.')

if user_prompt:
    question = Message(content=user_prompt)
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction="""Eres un experto de propiedad horizontal en Colombia
    
        Debes responder a la pregunta del usuario
        Debes responder con términos de propiedad horizontal en Colombia.
        . """,
        temperature= 0.1,
        ),
    )

    st.write(response.text)
