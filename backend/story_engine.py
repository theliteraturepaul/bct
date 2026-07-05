import google.generativeai as genai
import streamlit as st

class StoryGenerationError(Exception):
    pass

def build_prompt(user_prompt: str, genre: str, length: str) -> str:
    word_count_map = {
        "short": "150-250",
        "medium": "300-500",
        "long": "600-800"
    }
    word_count = word_count_map.get(length.lower(), "150-250")
    
    template = (
        f'Write a {genre} short story based on this idea: "{user_prompt}". '
        f'Length: approximately {word_count} words. '
        f'Give it a clear beginning, middle, and end. Do not include a title unless it fits naturally.'
    )
    return template

def generate_story(user_prompt: str, genre: str, length: str) -> str:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = build_prompt(user_prompt, genre, length)
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise StoryGenerationError("Empty response from the model.")
            
        return response.text
        
    except Exception as e:
        if isinstance(e, StoryGenerationError):
            raise
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg or "rate limit" in error_msg:
            raise StoryGenerationError("Too many requests — try again in a moment")
        raise StoryGenerationError("Something went wrong while communicating with the AI. Please try again.")
