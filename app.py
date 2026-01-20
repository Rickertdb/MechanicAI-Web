import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API Key securely
try:
    # Use st.secrets to keep your key private
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()

# 2. Set the model (using -latest to avoid 404 errors)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("👨‍🔧 AI Mechanic Online")

# Sidebar for inputs
car_model = st.sidebar.text_input("Car Model", "2018 Toyota Camry")
uploaded_file = st.sidebar.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # Combine text and image for the AI
            content = [f"Vehicle: {car_model}. Problem: {prompt}"]
            if uploaded_file:
                content.append(Image.open(uploaded_file))
            
            try:
                response = model.generate_content(content)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
