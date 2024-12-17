from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv(), override=True)
import os
from langchain_openai import OpenAIEmbeddings

st.set_page_config(
    page_title='Your Custom Assistant',
    page_icon='🤖'
)
# st.subheader('')

st.title("Your Custom ChatGPT 🤖")
st.write(
    "💬  This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    
)

api_key = st.text_input("OpenAI API Key", type="password")

def validate_openai_api_key(api_key):
    try:
        os.environ['OPENAI_API_KEY'] = api_key
        # Perform a simple operation to validate the key
        embeddings = OpenAIEmbeddings()
        embeddings.embed_query("test")  # Test query
        return True
    except Exception as e:
        st.error(f"Invalid OpenAI API Key: {e}")
        return False

if not api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

else:
    
    if validate_openai_api_key(api_key):
        st.write("Valid API")
        
    chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5, openai_api_key = api_key)

    # Initialize chat messages in the session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Sidebar configuration
    with st.sidebar:
        # Text input for system message
        system_message = st.text_input(label='System role')
        # Text input for user prompt
        user_prompt = st.text_input(label='Send a message')
        
        # Add a Clear Conversation button
        if st.button("Clear Conversation"):
            st.session_state.messages = []  # Reset the chat history

        if system_message:
            if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
                st.session_state.messages.append(
                    SystemMessage(content=system_message)
                )

        if user_prompt:
            st.session_state.messages.append(
                HumanMessage(content=user_prompt)
            )

            with st.spinner('Working on your request ...'):
                # Generate response from the model
                response = chat(st.session_state.messages)

            # Add response to session state
            st.session_state.messages.append(AIMessage(content=response.content))

    # Add default SystemMessage if none exists
    if len(st.session_state.messages) >= 1:
        if not isinstance(st.session_state.messages[0], SystemMessage):
            st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

    # Display chat history
    for i, msg in enumerate(st.session_state.messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=f'{i} + 🤓')  # User's message
        else:
            message(msg.content, is_user=False, key=f'{i} + 🤖')  # AI response
