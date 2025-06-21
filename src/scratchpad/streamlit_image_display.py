import streamlit as st
from PIL import Image
from pathlib import Path

# Initialize session state
if "show_image" not in st.session_state:
    st.session_state.show_image = False

# Define the image path
image_path = Path(r"C:\Users\GopiP\OneDrive\Pictures\Screenshots\Screenshot 2025-01-06 192908.png")

# Display "Show Image" and "Close Image" buttons
if st.button("Show Image"):
    st.session_state.show_image = True

if st.button("Close Image"):
    st.session_state.show_image = False

# Display the image based on the session state
if st.session_state.show_image:
    image = Image.open(image_path)
    st.image(image, caption="Here is your image", use_container_width=True)

# Provide a link to open the image in a new window
image_url = f"file://{image_path}"
st.markdown(f"""
    <a href="{image_url}" target="_blank">
        <button style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;">
            Open Image in New Window
        </button>
    </a>
""", unsafe_allow_html=True)

