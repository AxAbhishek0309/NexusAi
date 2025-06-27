import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (
    load_gemini_pro_model,
    gemini_pro_response,
    gemini_pro_vision_response,
    embeddings_model_response
)

# Set working directory and app config
working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Nexus AI",
    page_icon="🧠",
    layout="wide"
)

# Sidebar with navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712105.png", width=120)
    st.markdown("## Nexus AI Assistant")
    st.markdown("Your multi-modal AI-powered companion.")
    selected = option_menu(
        "Nexus AI",
        ['ChatBot', 'Image Captioning', 'Embed text', 'Ask me anything'],
        menu_icon='robot',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0
    )

# Utility: role translation for chat history
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# -------------------- Chatbot Page --------------------
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("🤖 Nexus AI ChatBot")

    # Create a container for chat messages (top)
    chat_placeholder = st.container()

    # Create an empty slot at the bottom for input
    input_placeholder = st.empty()

    # Show chat history
    with chat_placeholder:
        for message in st.session_state.chat_session.history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(message.parts[0].text)

    # Place input at the bottom of the screen
    with input_placeholder:
        user_input = st.chat_input("Ask Nexus AI...")

    # When user sends a message
    if user_input:
        # Display user message
        with chat_placeholder:
            st.chat_message("user").markdown(user_input)

        # Get AI response
        gemini_response = st.session_state.chat_session.send_message(user_input)

        # Display response
        with chat_placeholder:
            st.chat_message("assistant").markdown(gemini_response.text)

        


# -------------------- Image Captioning --------------------
if selected == "Image Captioning":
    st.title("📸 Snap Narrate")
    st.markdown("Upload an image and let Nexus AI describe it!")

    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_image and st.button("🖼️ Generate Caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)

        with col1:
            st.image(image.resize((800, 500)), caption="Uploaded Image")

        with col2:
            prompt = "Write a short caption for this image"
            caption = gemini_pro_vision_response(prompt, image)
            st.markdown("#### 🧠 AI-Generated Caption:")
            st.success(caption)

# -------------------- Embeddings --------------------
if selected == "Embed text":
    st.title("🧩 Embed Text")
    st.markdown("Convert any piece of text into a numerical vector using Nexus AI embeddings.")

    user_prompt = st.text_area("Enter text below 👇")

    if user_prompt and st.button("📊 Generate Embedding"):
        embedding = embeddings_model_response(user_prompt)
        st.markdown("#### 🧠 Embedding Result:")
        st.code(embedding, language="json")

# -------------------- Ask Me Anything --------------------
if selected == "Ask me anything":
    st.title("❓ Ask Me Anything")
    st.markdown("Type your question and let Nexus AI answer it!")

    user_prompt = st.text_area("Your question")

    if user_prompt and st.button("🎯 Get Answer"):
        answer = gemini_pro_response(user_prompt)
        st.markdown("#### 🤖 Gemini says:")
        st.info(answer)
