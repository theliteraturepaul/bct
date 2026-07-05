import html
import os

import streamlit as st

from backend.story_engine import StoryGenerationError, generate_story

# Must be the very first Streamlit command
st.set_page_config(page_title="AI Story Generator", layout="centered")


def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def glass_error(message: str):
    safe_message = html.escape(message)
    st.markdown(
        f'''
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
            ⚠️ {safe_message}
        </div>
        ''',
        unsafe_allow_html=True,
    )


def run_generation(prompt: str, genre: str, length: str):
    """Runs generation and returns (story, error_message). Never raises —
    on failure returns (None, message) so callers can decide what to keep
    on screen instead of the caller having to catch exceptions itself."""
    try:
        with st.spinner("Writing your story..."):
            story = generate_story(prompt, genre, length)
        return story, None
    except StoryGenerationError as e:
        return None, str(e)


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

    genre_options = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure"]
    length_options = ["short", "medium", "long"]
    length_labels = {"short": "Short", "medium": "Medium", "long": "Long"}

    # Main Input Card
    with st.container(border=True):
        prompt = st.text_area(
            "Story Idea",
            value=st.session_state.prompt,
            placeholder="A knight who is afraid of swords...",
            key="prompt_input",
        )

        genre = st.radio(
            "Genre",
            genre_options,
            index=genre_options.index(st.session_state.genre)
            if st.session_state.genre in genre_options
            else 0,
            horizontal=True,
            key="genre_input",
        )

        length = st.radio(
            "Length",
            length_options,
            index=length_options.index(st.session_state.length)
            if st.session_state.length in length_options
            else 0,
            horizontal=True,
            format_func=lambda opt: length_labels[opt],
            key="length_input",
        )

        if st.button("Generate Story", type="primary", use_container_width=True):
            if not prompt.strip():
                glass_error("Please enter a story idea before generating.")
            else:
                st.session_state.prompt = prompt.strip()
                st.session_state.genre = genre
                st.session_state.length = length

                story, error = run_generation(
                    st.session_state.prompt, st.session_state.genre, st.session_state.length
                )
                if error:
                    # Keep any prior successful story on screen — don't wipe
                    # a good result just because a new attempt failed.
                    glass_error(error)
                else:
                    st.session_state.output = story

    # Story Output Card
    if st.session_state.output:
        with st.container(border=True):
            st.markdown(
                f'<div class="story-output-text">{st.session_state.output}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Regenerate", type="secondary"):
                story, error = run_generation(
                    st.session_state.prompt, st.session_state.genre, st.session_state.length
                )
                if error:
                    glass_error(error)  # old story stays visible until next successful run
                else:
                    st.session_state.output = story
                    st.rerun()


if __name__ == "__main__":
    main()
