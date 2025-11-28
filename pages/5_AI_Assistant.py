import streamlit as st
from google import genai

cient = genai.Client(api_key=st.secrets["GENAI_API_KEY"])
st.subheader("AI Assistant")
#Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "model":
        role = "AI Assistant"
    else:
        role = message["role"]
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])
        
        


