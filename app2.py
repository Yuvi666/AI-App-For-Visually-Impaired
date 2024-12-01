import os
from PIL import Image
import pytesseract
import pyttsx3
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Google Generative AI API Key
GEMINI_API_KEY = "AIzaSyA00INMMFhBtfRlZBezunMrg92-YA4EPqs"  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Streamlit Page Configuration
st.set_page_config(page_title="Vocalize AI", layout="centered", page_icon="📜")

def setup_sidebar():
    """Configures the sidebar."""
    st.sidebar.header("🔧 Features")
    st.sidebar.markdown("""
    - **Scene Understanding**: Describe the scene in an image.
    - **Text-to-Speech**: Hear the extracted text or scene description.
    - **OCR**: Extract text from images.
    """)

def display_header():
    """Displays the main header."""
    st.title("Vocalize AI 📜🔊")
    st.markdown("""
    **Assistive tool for visually impaired individuals.**
    Upload an image to get started!
    """)

def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    bytes_data = uploaded_file.getvalue()
    return [{"mime_type": uploaded_file.type, "data": bytes_data}]

def main():
    # Sidebar and Header
    setup_sidebar()
    display_header()

    # File Upload
    uploaded_file = st.file_uploader("📤 Upload an Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Display Uploaded Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Functional Buttons
        st.markdown("### Select an Action")
        col1, col2, col3 = st.columns(3)
        with col1:
            scene_button = st.button("🔍 Describe Scene")
        with col2:
            ocr_button = st.button("📝 Extract Text")
        with col3:
            tts_button = st.button("🔊 Text-to-Speech")

        # Input Prompt for Scene Understanding
        input_prompt = """
        You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
        1. List of items detected in the image with their purpose.
        2. Overall description of the image.
        3. Suggestions for actions or precautions for the visually impaired.
        """

        # Process User Actions
        image_data = input_image_setup(uploaded_file)

        if scene_button:
            with st.spinner("Generating scene description..."):
                response = generate_scene_description(input_prompt, image_data)
                st.subheader("Scene Description")
                st.write(response)
                # Convert the scene description to speech
                text_to_speech(response)

        if ocr_button:
            with st.spinner("Extracting text from image..."):
                text = extract_text_from_image(image)
                st.subheader("Extracted Text")
                st.write(text)

        if tts_button:
            with st.spinner("Converting text to speech..."):
                text = extract_text_from_image(image)
                if text.strip():
                    text_to_speech(text)
                    st.success("Text-to-Speech Conversion Completed!")
                else:
                    st.warning("No text found in the image.")
    else:
        st.info("👆 Upload an image to get started.")

# Run the app
if __name__ == "__main__":
    main()
