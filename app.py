import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# --- INITIAL SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Mechanic Agent", layout="wide")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI LAYOUT ---
st.title("👨‍🔧 AI Master Mechanic Chat")
st.sidebar.header("Vehicle Profile")
car_info = st.sidebar.text_input("Current Vehicle", placeholder="e.g. 2017 Honda Civic")

# File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader("Upload Engine/Chassis Photo", type=['jpg', 'png'])

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT LOGIC ---
if prompt := st.chat_input("Ask about a code (e.g. P0301) or describe a symptom..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # Prepare content (Text + Image if available)
            content = [f"Context: {car_info}. Question: {prompt}"]
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            
            # Send to Gemini
            response = model.generate_content(content)
            full_response = response.text
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})