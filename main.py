from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Learning Objectives from Video Transcipt")
st.title("Course Development from Video Transript")

with st.sidebar:
    uploaded_file = st.file_uploader("Upload the .vtt transript from Media Plus", type=['vtt', 'txt'])

#get response
def get_repsonse(query, uploaded_file):
    template = """You are a helpful instructional designer. Take a look at the transcript for a lecture below.
    
    Transcript: {uploaded_file}

    Some addtional context: {query}

    Write 2 learning objectives using Bloom's Taxonomy that describe the kind of learning students should achieve by watching this lecture. They should finish the sentence, 'Student will be able to...'
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "uploaded_file": uploaded_file,
        "query": user_query
        })

#conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)
#chat input
user_query = st.chat_input("Upload .vtt file before chatting")
if user_query is not None and user_query !="":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_repsonse(user_query, uploaded_file)
        st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))    