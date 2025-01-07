from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
load_dotenv()

llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.1)

import streamlit as st
import os

os.environ["GROQ_API_KEY"] = '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'
os.environ["COHERE_API_KEY"] = 'hgNPboby7mr6AErA1L7CRP7P969JquZZE2XnGKoW'
os.environ["PINECONE_API_KEY"] = '44c0e7c6-a11c-4c77-aee5-a951e43cd2a1'

tool = SerperDevTool(
    country="col",
    locale="col",
    location="Colombia",
    n_results=2,
)

augustus = Agent(
    role='Experto en propiedad horizontal',
    goal='Debes responder preguntas de propiedad horizontal en Colombia',
    backstory='Eres un experto en propiedad horizontal en Colombia, debes responder de manera precisa. Tu nombre es Augustus',
    tools=[tool],
    llm=llm,
    verbose=True
)

def augustus_task(prompt): 
    return Task(
    description=f"""
    Eres un experto de propiedad horizontal en Colombia

    Debes responder a la siguiente pregunta del usuario: {prompt}
    
    si puedes responder con base a tus conocimientos hazlo, si no tienes los conocimientos entonces usa la herramienta para buscar en internet. """,
    agent=augustus,
    expected_output='Respuesta precisa'
)

st.header('Augustus')

user_prompt = st.text_input('Preguntale a Augustus sobre cualquier tema de Propiedad Horizontal.')

if user_prompt:
    question = Message(content=user_prompt)
    
    augustus_crew = Crew(
    agents=[augustus],
    tasks=[augustus_task(question)],
    verbose=True,
    memory=True,
    embedder={
        "provider": "cohere",
        "config": {
            "api_key": "hgNPboby7mr6AErA1L7CRP7P969JquZZE2XnGKoW",
            "model_name": "embed-multilingual-v3.0"
        }
    }
)
    response = augustus_crew.kickoff()
    st.write(response.raw)
