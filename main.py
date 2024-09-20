from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pinecone_plugins.assistant.models.chat import Message
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os

os.environ["GROQ_API_KEY"] = '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'
os.environ["COHERE_API_KEY"] = 'hgNPboby7mr6AErA1L7CRP7P969JquZZE2XnGKoW'
os.environ["PINECONE_API_KEY"] = '44c0e7c6-a11c-4c77-aee5-a951e43cd2a1'

pc = Pinecone()

llm = ChatGroq(model='llama-3.1-70b-versatile', temperature=0.1)

embeddings = CohereEmbeddings(
    model="embed-multilingual-v3.0",
)

assistant = pc.assistant.Assistant(
    assistant_name="prueba", 
)

def assistant_prompt():
    prompt = ChatPromptTemplate.from_messages(
    ("human", """ # Rol
     Tu nombre es Augustus. Eres un asistente virtual especializado en leyes, específicamente en el campo de propiedad horizontal en Colombia. Tienes que resolver conflictos de propiedad horizontal basándote en las leyes de Colombia, y debes responder en base al contexto.\n\n
    
    Question: {question}  Contexto: {context}
    """))
    return prompt

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

st.header('Augustus')

user_prompt = st.text_input('Preguntale a Augustus sobre cualquier tema de Propiedad Horizontal.')

if user_prompt:
    msg = Message(content=user_prompt)
    resp = assistant.chat_completions(messages=[msg])

    prompt = assistant_prompt()


    response_assitant = resp['choices'][0]['message']['content']

    rag_chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = rag_chain.invoke({'context': response_assitant, 'question': user_prompt})

    st.write(response)
