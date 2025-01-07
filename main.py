from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
load_dotenv()

llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0.1, google_api_key='AIzaSyAwqzM4PEubbClKu0waIBmSW4RNmevTLz4')

import streamlit as st
import os

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
    )
    }
)
    response = augustus_crew.kickoff()
    st.write(response.raw)
