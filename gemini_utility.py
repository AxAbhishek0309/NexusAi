import os
import json
from PIL import Image
import google.generativeai as genai

# Working directory and config path
working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))

# Configure Gemini API
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model for general use (chat/text)
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    return gemini_pro_model

# Gemini Vision response: prompt + image
def gemini_pro_vision_response(prompt, image):
    gemini_vision_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = gemini_vision_model.generate_content([prompt, image])
    return response.text

# Embeddings from text
def embeddings_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(
        model=embedding_model,
        content=input_text,
        task_type="retrieval_document"
    )
    return embedding["embedding"]

# Get response from Gemini model for text prompt
def gemini_pro_response(user_prompt):
    gemini_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = gemini_model.generate_content(user_prompt)
    return response.text



# result = gemini_pro_response("What is Machine Learning")
# print(result)
# print("-"*50)
#
#
# image = Image.open("test_image.png")
# result = gemini_pro_vision_response("Write a short caption for this image", image)
# print(result)
# print("-"*50)
#
#
# result = embeddings_model_response("Machine Learning is a subset of Artificial Intelligence")
# print(result) 
 