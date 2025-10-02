import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
import dotenv

# Load environment variables
dotenv.load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

llm = load_llm()

# Page configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")
st.caption(f"Chat Model: {llm.model}")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt)
            st.markdown(response.content)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.content})

# Sidebar with controls
with st.sidebar:
    st.header("Chat Controls")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Model Info:**")
    st.write(f"Model: {llm.model}")
    st.write(f"Temperature: {llm.temperature}")
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.write("- Type your message in the chat input")
    st.write("- Press Enter to send")
    st.write("- Use 'Clear Chat History' to reset")