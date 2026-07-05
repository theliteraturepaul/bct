import traceback

import google.generativeai as genai
import streamlit as st


class StoryGenerationError(Exception):
    pass


_configured = False


def _ensure_configured():
    """Configure the Gemini client once, and fail fast with a clear error
    if the API key is missing or empty — this is the #1 cause of silent
    'something went wrong' errors on Streamlit Cloud."""
    global _configured
    if _configured:
        return

    api_key = st.secrets.get("GEMINI_API_KEY", "").strip() if hasattr(st.secrets, "get") else None
    if not api_key:
        raise StoryGenerationError(
            "The AI service isn't configured correctly. "
            "(GEMINI_API_KEY is missing — check your app's Secrets settings.)"
        )

    genai.configure(api_key=api_key)
    _configured = True


def build_prompt(user_prompt: str, genre: str, length: str) -> str:
    word_count_map = {
        "short": "150-250",
        "medium": "300-500",
        "long": "600-800",
    }
    word_count = word_count_map.get(length.lower(), "150-250")

    template = (
        f'Write a {genre} short story based on this idea: "{user_prompt}". '
        f'Length: approximately {word_count} words. '
        f'Give it a clear beginning, middle, and end. Do not include a title unless it fits naturally.'
    )
    return template


def generate_story(user_prompt: str, genre: str, length: str) -> str:
    # Let configuration errors (e.g. missing key) surface with their own
    # specific message instead of being caught by the generic handler below.
    _ensure_configured()

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = build_prompt(user_prompt, genre, length)

        response = model.generate_content(prompt)

        # Check for safety/content blocks BEFORE touching response.text,
        # since accessing .text on a blocked response raises internally
        # rather than returning empty.
        if not response.candidates:
            block_reason = getattr(response.prompt_feedback, "block_reason", None)
            raise StoryGenerationError(
                "The story couldn't be generated for this prompt. "
                "Try rephrasing your idea."
                if block_reason
                else "The AI didn't return a story. Please try again."
            )

        finish_reason = getattr(response.candidates[0], "finish_reason", None)
        if finish_reason is not None and str(finish_reason) not in ("1", "STOP"):
            raise StoryGenerationError(
                "The story couldn't be completed for this prompt. Try rephrasing your idea."
            )

        if not response.text or not response.text.strip():
            raise StoryGenerationError("Empty response from the model. Please try again.")

        return response.text

    except StoryGenerationError:
        raise

    except Exception as e:
        traceback.print_exc()  # full traceback lands in Streamlit Cloud logs
        error_msg = str(e).lower()

        if "429" in error_msg or "quota" in error_msg or "rate limit" in error_msg:
            raise StoryGenerationError("Too many requests — try again in a moment") from e

        if (
            "403" in error_msg
            or "permission" in error_msg
            or "api key not valid" in error_msg
            or "unauthenticated" in error_msg
        ):
            raise StoryGenerationError(
                "The AI service rejected the request. (Check that your API key is valid.)"
            ) from e

        if "404" in error_msg or "not found" in error_msg:
            raise StoryGenerationError(
                "The AI model couldn't be reached. (Check the model name is still valid.)"
            ) from e

        raise StoryGenerationError(
            "Something went wrong while communicating with the AI. Please try again."
        ) from e
