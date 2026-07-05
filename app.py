import streamlit as st
import os
from backend.story_engine import generate_story, StoryGenerationError

# Must be the very first Streamlit command
st.set_page_config(page_title="AI Story Generator", layout="centered")

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def glass_error(message):
    st.markdown(f'''
        <div style="
            background: rgba(255, 99, 71, 0.25);
            border: 1px solid rgba(255, 99, 71, 0.4);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            color: #33334D;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        ">
            ⚠️ {message}
        </div>
    ''', unsafe_allow_html=True)

def main():
    load_css()
    
    st.markdown("<h1>AI Story Generator</h1>", unsafe_allow_html=True)
    
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""
    if "genre" not in st.session_state:
        st.session_state.genre = "Fantasy"
    if "length" not in st.session_state:
        st.session_state.length = "short"
    if "output" not in st.session_state:
        st.session_state.output = ""
        
    # Main Input Card
    with st.container(border=True):
        prompt = st.text_area("Story Idea", value=st.session_state.prompt, placeholder="A knight who is afraid of swords...")
        
        genre_options = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure"]
        genre = st.radio("Genre", genre_options, index=genre_options.index(st.session_state.genre) if st.session_state.genre in genre_options else 0, horizontal=True)
        
        length_options = ["short", "medium", "long"]
        length = st.radio("Length", length_options, index=length_options.index(st.session_state.length) if st.session_state.length in length_options else 0, horizontal=True)
        
        if st.button("Generate Story", type="primary", use_container_width=True):
            if not prompt.strip():
                glass_error("Please enter a story idea before generating.")
            else:
                st.session_state.prompt = prompt
                st.session_state.genre = genre
                st.session_state.length = length
                
                try:
                    with st.spinner("Writing your story..."):
                        story = generate_story(prompt, genre, length)
                        st.session_state.output = story
                except StoryGenerationError as e:
                    glass_error(str(e))
                    st.session_state.output = ""

    # Story Output Card
    if st.session_state.output:
        with st.container(border=True):
            st.markdown(f'<div class="story-output-text">{st.session_state.output}</div>', unsafe_allow_html=True)
            if st.button("Regenerate", type="secondary"):
                if not st.session_state.prompt.strip():
                    glass_error("Please enter a story idea before generating.")
                else:
                    try:
                        with st.spinner("Writing your story..."):
                            story = generate_story(st.session_state.prompt, st.session_state.genre, st.session_state.length)
                            st.session_state.output = story
                            st.rerun()
                    except StoryGenerationError as e:
                        glass_error(str(e))
                        st.session_state.output = ""

if __name__ == "__main__":
    main()
