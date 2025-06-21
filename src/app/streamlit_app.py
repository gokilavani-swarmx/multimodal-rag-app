import streamlit as st
from streamlit.web import cli as stcli
import sys
from sidebar import display_sidebar
from chat_interface_v1 import display_chat_interface

from PIL import Image

image_directory = "./src/app/favicon.png"
image = Image.open(image_directory)

PAGE_CONFIG = {"page_title":"Instant-RAG", 
               "page_icon":image, 
               "layout":"wide", 
               "initial_sidebar_state":"auto"}

st.set_page_config(**PAGE_CONFIG)
#
# st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; font-family: Calibri;'>An Open-Source Multimodal Instant-RAG Framework</h1>", unsafe_allow_html=True)
# st.title("Langchain RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Display the sidebar
display_sidebar()

# Display the chat interface
display_chat_interface()

# if __name__ == '_main_':
#     sys.argv = ["streamlit", "run", "streamlit_app.py"]
#     sys.exit(stcli.main())'
