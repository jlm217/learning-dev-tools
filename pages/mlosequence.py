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