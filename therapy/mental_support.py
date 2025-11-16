import streamlit as st
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key="GEMINI_API_KEY")  
model = genai.GenerativeModel("models/gemini-2.5-flash")


st.set_page_config(page_title="Mental Health Chatbot")

def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("therapy/background.png")

st.markdown(f"""
    <style>
        .main{{
            background-image:url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat:no-repeat;
        }}
    </style>
""", unsafe_allow_html=True)


st.session_state.setdefault('conversation_history', [])


def generate_response(user_message):
    st.session_state['conversation_history'].append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    chat = model.start_chat(
        history=st.session_state['conversation_history']
    )

    response = chat.send_message(
        [{"text": user_message}]
    )

    ai_reply = response.text

    st.session_state['conversation_history'].append({
        "role": "model",
        "parts": [{"text": ai_reply}]
    })

    return ai_reply




def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = model.generate_content(prompt)
    return response.text


def generate_meditation_guide():
    prompt = "Provide a calming 5-minute guided meditation script to help someone relax."
    response = model.generate_content(prompt)
    return response.text



st.title("🧠 Mental Health Support Agent")

# Display conversation
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['parts'][0]['text']}")


# Input
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
