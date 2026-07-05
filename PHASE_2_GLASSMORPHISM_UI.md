# Phase 2 — Glassmorphism UI

**Goal:** Apply the full glassmorphism visual design on top of the working Phase 1 app, without touching backend logic.

**Depends on:** DESIGN.md (full spec — colors, typography, component styles), Phase 1 completed and working

---

## Prompt for Antigravity 2.0

```
Context (carry forward):
- Phase 1 is complete: app.py has a working Gemini-backed story generator using plain Streamlit widgets, backend logic lives in backend/story_engine.py and must not change.
- Tech stack: Streamlit, custom CSS injected via st.markdown(unsafe_allow_html=True).

Objective:
Restyle the existing Streamlit app with a glassmorphism visual design, exactly matching the design spec below. Do not change any backend logic, function signatures, or app behavior — visual layer only.

Starting State:
Working, unstyled Streamlit app from Phase 1 (app.py + backend/story_engine.py).

Target State:
- New file: assets/style.css containing all glassmorphism CSS
- app.py loads style.css once at startup via st.markdown
- Visual result matches this spec:
  - Background: fixed diagonal gradient from #6D5BBA to #8CB8FF, full viewport, with 2 blurred radial color blobs for depth
  - Fonts: Poppins (headings) + Inter (body) loaded from Google Fonts via @import
  - Glass cards: background rgba(255,255,255,0.12), backdrop-filter blur(16px), border 1px solid rgba(255,255,255,0.25), border-radius 20px, box-shadow 0 8px 32px rgba(31,38,135,0.25), padding 32px
  - All text on glass surfaces is white (#FFFFFF) or rgba(255,255,255,0.75) for secondary text — never dark text on glass
  - Main input card: prompt textarea, genre selector styled as pill chips (selected = filled #FFD166 background with dark text, unselected = glass style), length control as a segmented control
  - Generate button: glass fill rgba(255,255,255,0.22), accent-colored label, hover scale 1.02 with brighter glow, disabled+spinner state while loading with label "Writing your story..."
  - Story output: separate glass card below input, appears only after generation, max-height with scroll if long, "Regenerate" as a smaller secondary glass button beneath it
  - Layout: single centered column, max-width ~720px, 24px vertical spacing between sections
  - Mobile: card padding reduces to 20px, still single column

Allowed Actions:
- Create assets/style.css
- Edit app.py only to add st.markdown CSS injection, wrap existing widgets in styled container divs, and adjust widget labels/layout as needed to match the spec
- Reorganize widget layout/order in app.py if needed to match the component spec

Forbidden Actions:
- Do NOT modify backend/story_engine.py
- Do NOT change generate_story's signature, the prompt template, or any word-count logic
- Do NOT remove the session_state handling from Phase 1
- Do NOT deploy or push to git

Stop Conditions:
Pause and ask for human review when:
- Streamlit's native widgets can't be styled to match a spec point (e.g. pill-chip genre selector) — propose the closest achievable alternative (e.g. styled st.radio or button group) instead of silently skipping it
- An error can't be resolved in 2 attempts

Checkpoints:
After each major step (background/gradient, cards, buttons, output panel, mobile pass), output: ✅ [what was completed]
At the end, output a full summary of every file changed and a short note on any spec point that had to be approximated due to Streamlit limitations.
```

🎯 Target: Antigravity 2.0
💡 Scoped strictly to styling with an explicit "do not touch backend" lock, since the most common failure mode here is an agent "helpfully" refactoring working logic while restyling.

**Before pasting:** confirm Phase 1's file paths (`app.py`, `backend/story_engine.py`) match what's in your actual project before running this.
