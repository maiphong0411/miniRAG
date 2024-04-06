from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
gemini_api = os.environ.get("GEMINI_API_KEY")

def load_model(gemini_api=gemini_api):
    """
    Load a generative model using the provided Gemini API key and safety settings.
    
    :param gemini_api: The API key for the Gemini service.
    :return: The loaded GenerativeModel object.
    """
    genai.configure(api_key=gemini_api)
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    GEMINI = genai.GenerativeModel('gemini-pro', safety_settings = safety_settings)
    return GEMINI