import google.generativeai as genai
import json

# Load API key from config.json
with open("config.json") as f:
    config = json.load(f)

api_key = config["GOOGLE_API_KEY"]

# Configure Gemini API
genai.configure(api_key=api_key)

# List all available models
models = genai.list_models()

# Print model names and descriptions
for model in models:
    print(f"Model Name: {model.name}")
    print(f"  Description: {model.description}")
    print(f"  Input Token Limit: {model.input_token_limit}")
    print(f"  Output Token Limit: {model.output_token_limit}")
    print()
