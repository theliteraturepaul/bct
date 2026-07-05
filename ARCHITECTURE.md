# System Architecture — AI Story Generator

## 1. Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Frontend/App framework | Streamlit | Single-page app, fastest path to deploy |
| LLM | Gemini API — `gemini-2.5-flash` | Free tier via Google AI Studio |
| SDK | `google-generativeai` (Python) | Official Gemini Python SDK |
| Styling | Custom CSS (glassmorphism) injected via `st.markdown` | See DESIGN.md |
| Hosting | Streamlit Community Cloud | Same as prior hackathon deployment |
| Secrets | `.streamlit/secrets.toml` (local) / Streamlit Cloud Secrets (deployed) | Never committed to git |

## 2. High-Level Data Flow

```
User (browser)
   │
   ▼
Streamlit UI (app.py)
   │  collects: prompt text, genre, length
   ▼
generate_story() [backend/story_engine.py]
   │  builds final prompt from template
   ▼
Gemini API (gemini-2.5-flash)
   │  returns generated text
   ▼
app.py renders result in glass output card
   │
   ▼
User reads / clicks Regenerate (loops back to generate_story())
```

## 3. File Structure

```
story-generator/
├── app.py                  # Streamlit entrypoint — UI + orchestration only
├── backend/
│   └── story_engine.py     # Gemini API call, prompt construction, error handling
├── assets/
│   └── style.css           # All glassmorphism CSS lives here
├── .streamlit/
│   ├── config.toml         # Streamlit theme base overrides (optional)
│   └── secrets.toml        # LOCAL ONLY — GEMINI_API_KEY (gitignored)
├── requirements.txt
├── .gitignore               # must include .streamlit/secrets.toml
└── README.md
```

## 4. Core Modules & Responsibilities

**`app.py`**
- Renders UI (title, prompt input, genre selector, length control, buttons)
- Loads `assets/style.css` once at startup
- Calls `story_engine.generate_story(...)` on button click
- Holds session state: last prompt/genre/length (so "Regenerate" can reuse them), last story output, loading flag
- Does NOT contain API call logic directly — keep that in `backend/story_engine.py`

**`backend/story_engine.py`**
- Owns the Gemini client configuration (reads key from `st.secrets`)
- `build_prompt(user_prompt, genre, length) -> str` — constructs the final prompt sent to Gemini
- `generate_story(user_prompt, genre, length) -> str` — calls the API, returns story text or raises a handled exception
- All Gemini-specific error handling lives here, not in `app.py`

## 5. API Contract

```python
def generate_story(user_prompt: str, genre: str, length: str) -> str:
    """
    user_prompt: free-text idea from the user
    genre: one of the predefined genre options
    length: "short" | "medium" | "long" -> maps to a word-count instruction
    Returns: generated story text
    Raises: StoryGenerationError on API failure or empty response
    """
```

**Prompt template (used inside `build_prompt`)**
```
Write a {genre} short story based on this idea: "{user_prompt}".
Length: approximately {word_count} words.
Give it a clear beginning, middle, and end. Do not include a title unless it fits naturally.
```
Length → word count mapping: short = 150–250, medium = 300–500, long = 600–800.

## 6. Error Handling Strategy

| Failure | Handling |
|---|---|
| Empty/blank prompt | Block the API call client-side; show inline validation message on the glass card |
| Gemini API error / timeout | Catch in `story_engine.py`, raise `StoryGenerationError`, `app.py` shows a friendly glass-styled error banner — never a raw stack trace |
| Rate limit hit | Show "Too many requests — try again in a moment" message; do not retry automatically more than once |
| Empty/garbled response from model | Treat as failure, same friendly error path, offer Regenerate |

## 7. Secrets Management

- Local dev: `.streamlit/secrets.toml` → `GEMINI_API_KEY = "..."`, accessed via `st.secrets["GEMINI_API_KEY"]`
- Deployed: same key set in Streamlit Community Cloud → App Settings → Secrets
- `.gitignore` must exclude `.streamlit/secrets.toml` before the first commit — verify this before pushing

## 8. Known Constraints

- Streamlit re-runs the whole script on every interaction — session state must be used deliberately to avoid re-triggering API calls unintentionally
- `backdrop-filter` blur has inconsistent support in some older browsers — acceptable for a hackathon demo, not a production concern
- Gemini free tier has request-per-minute limits — fine for a live demo with judges, not for hundreds of concurrent users
