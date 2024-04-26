from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="CLO Builder")
st.title("CLO Builder")
with st.sidebar:
    course_name = st.text_input('Course Prefix and Number')
    course_description = st.text_area("Course Description")
    sm_content = st.text_area("List of Topics for Course")

#get response
def get_repsonse(course_name, course_description, sm_content, query):
    template = """You are a helpful instructional designer who is an expert in identifying, crafting, and editing Learning Objectives. Learning objectives (also known as learning outcomes) are essential for effective learning. They help to articulate what students should be able to do as a result of the instruction and consequently aid in designing more effective instruction planning, activities, and assessments. When developing learning objectives, carefully consider what students should learn and be able to accomplish from the instruction. The revised Bloom’s Taxonomy is very helpful for writing action-based learning objectives and identifying the appropriate cognitive level. A basic formula for creating a learning objective is:
    Students will be able to:
    List of Learning objectives that start with Action (verb) + Skill/Knowledge/Ability
    In particular, Learning Objectives should:
    1. be specific, identifying exactly what students should be able to do to meet them; and
    2. require students to do something measurable or performance-based, so that someone other than the student can identify whether the objective has been achieved.
    AVOID verbs like understand or know when writing cognitive learning objectives because they describe outcomes that are neither specific nor measurable.

    You are working on the {course_name}. 
    Here is the Course Description: {course_description}
    Here is a list of the content that should be covered in the course: {sm_content}

    Some addtional context: {query}

    Create a maximum of  5 LO for each course.
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"course_name": course_name, "course_description": course_description,"sm_content" : sm_content, "query" : user_query})


#chat input
user_query = st.chat_input("Add any addtional context about the course that should be included in the CLOs")
if user_query is not None and user_query !="":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_repsonse(course_name, course_description, sm_content, user_query)
        st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))  

    #conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)