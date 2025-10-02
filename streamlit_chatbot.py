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
def load_llm(model_name, temperature):
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

# Page configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Initialize session state for settings
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.0
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-2.5-flash"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with controls
with st.sidebar:
    st.header("Chat Controls")
    
    # Temperature slider
    new_temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=2.0, 
        value=st.session_state.temperature,
        step=0.1,
        help="Higher values make output more random, lower values more focused"
    )
    
    # Model selection
    model_options = [
        "gemini-2.5-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-2.5-flash-lite-preview-06-17"
    ]
    
    new_model = st.selectbox(
        "Select Model",
        options=model_options,
        index=model_options.index(st.session_state.model_name),
        help="Choose the Gemini model to use"
    )
    
    # Update settings button
    if st.button("Apply Changes", type="primary"):
        if new_temperature != st.session_state.temperature or new_model != st.session_state.model_name:
            st.session_state.temperature = new_temperature
            st.session_state.model_name = new_model
            # Clear cache to reload LLM with new settings
            st.cache_resource.clear()
            st.success("Settings updated! New settings will apply to next message.")
            st.rerun()
    
    st.markdown("---")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Current Settings:**")
    st.write(f"Model: {st.session_state.model_name}")
    st.write(f"Temperature: {st.session_state.temperature}")
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.write("- Adjust temperature for creativity")
    st.write("- Select different models")
    st.write("- Click 'Apply Changes' to update")
    st.write("- Type your message in the chat input")
    st.write("- Press Enter to send")

# Load LLM with current settings
llm = load_llm(st.session_state.model_name, st.session_state.temperature)

st.caption(f"Chat Model: {st.session_state.model_name} | Temperature: {st.session_state.temperature}")

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