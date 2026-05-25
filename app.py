import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="AI Agent by Tirumalarao",
    page_icon="🤖",
    layout="centered"
)

# Header
st.title("🤖 AI Agent")
st.subheader("Ask me anything — I'll think and answer")
st.markdown("---")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Ask your question here...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful AI agent. Answer clearly and concisely."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            st.write(answer)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
