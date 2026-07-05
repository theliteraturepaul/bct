# Phase 1 — Project Setup & Backend Core

**Goal:** Working project skeleton + a Gemini-powered story generation function you can call and test from a script or bare Streamlit page, with zero styling. No glassmorphism yet — that's Phase 2.

**Depends on:** ARCHITECTURE.md (file structure, API contract, error handling table)

---

## Prompt for Antigravity 2.0

```
Objective:
Scaffold a Streamlit project for an AI story generator with a working Gemini API backend, following the exact file structure and API contract below. No custom CSS or styling in this phase — plain default Streamlit UI only.

Starting State:
Empty project folder.

Target State:
story-generator/
├── app.py
├── backend/
│   └── story_engine.py
├── .streamlit/
│   └── secrets.toml (placeholder key, gitignored)
├── requirements.txt
├── .gitignore
└── README.md (placeholder, one line)

backend/story_engine.py must expose:
- build_prompt(user_prompt: str, genre: str, length: str) -> str
- generate_story(user_prompt: str, genre: str, length: str) -> str
- a custom exception StoryGenerationError
- length mapping: short=150-250 words, medium=300-500 words, long=600-800 words
- prompt template: 'Write a {genre} short story based on this idea: "{user_prompt}". Length: approximately {word_count} words. Give it a clear beginning, middle, and end. Do not include a title unless it fits naturally.'
- Gemini client configured via st.secrets["GEMINI_API_KEY"], using model gemini-2.5-flash and the google-generativeai SDK
- generate_story must raise StoryGenerationError on API failure, timeout, or empty response — never let a raw exception propagate to app.py

app.py must:
- Load the Gemini key setup (no styling)
- Have a plain text input for the story prompt, a selectbox for genre (Fantasy, Sci-Fi, Mystery, Romance, Horror, Adventure), and a selectbox for length (short/medium/long)
- A "Generate Story" button that calls generate_story() and displays the result or a plain error message
- Use st.session_state to store the last prompt/genre/length/output so state survives reruns

Allowed Actions:
- Create all files listed above
- Install google-generativeai and streamlit, add both to requirements.txt
- Write a real .gitignore that excludes .streamlit/secrets.toml

Forbidden Actions:
- Do NOT add any custom CSS, HTML injection, or styling — plain Streamlit widgets only
- Do NOT commit or hardcode any real API key — use a placeholder string in secrets.toml
- Do NOT deploy or push to git
- Do NOT add features beyond what's specified (no multi-turn chat, no character fields)

Stop Conditions:
Pause and ask for human review when:
- The google-generativeai SDK's API differs meaningfully from what's assumed here (e.g. method names changed)
- An error can't be resolved in 2 attempts

Checkpoints:
After each file is created, output: ✅ [file path] — [one-line summary]
At the end, output a full summary of every file created and how to test locally (what to put in secrets.toml and how to run streamlit run app.py).
```

🎯 Target: Antigravity 2.0
💡 Optimized as an agentic build task with explicit scope locks (no styling yet, no deploy) so Antigravity doesn't jump ahead into Phase 2/3 work or attempt deployment prematurely.

**Before pasting:** review the scope locks and forbidden actions — this prompt intentionally keeps Antigravity from touching styling or deployment so it doesn't burn time/credits on the wrong phase.

**After this phase, verify:** you can run `streamlit run app.py` locally, paste a real Gemini key into `secrets.toml`, and get a story back in the plain UI before moving to Phase 2.
