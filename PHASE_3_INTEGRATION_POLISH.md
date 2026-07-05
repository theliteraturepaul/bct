# Phase 3 — Integration, Error Handling & Polish

**Goal:** Make the app demo-safe — handle bad input, API failures, and rough edges gracefully, using the Browser Subagent to actually click through the running app.

**Depends on:** ARCHITECTURE.md (error handling table), Phase 1 + Phase 2 completed

---

## Prompt for Antigravity 2.0

```
Context (carry forward):
- Phase 1 (backend) and Phase 2 (glassmorphism styling) are complete and working together.
- backend/story_engine.py raises StoryGenerationError on failure; app.py currently may not handle all edge cases gracefully yet.

Objective:
Harden the app against real-world failure cases and polish the interaction flow, using the error-handling rules below. Then use the browser subagent to test the running app end-to-end and fix anything broken.

Starting State:
Fully styled, functionally working app from Phase 2.

Target State:
- Blank/whitespace-only prompt: blocked client-side in app.py before calling generate_story, with an inline validation message shown in the existing glass-card style (not a plain st.error, match the visual design)
- StoryGenerationError from the backend: caught in app.py, shown as a friendly glass-styled error banner — no raw stack traces or exception text visible to the user
- Rate limit / repeated failures: show "Too many requests — try again in a moment", do not auto-retry more than once
- Loading state: Generate button shows spinner + "Writing your story..." and is disabled while a request is in flight (verify this actually works, not just styled to look disabled)
- Regenerate button: reuses the last prompt/genre/length from session_state and calls generate_story again without requiring the user to retype anything
- After implementing, use the browser subagent to: submit a valid prompt and confirm a story renders; submit an empty prompt and confirm the validation message appears; verify Regenerate works after a successful generation

Allowed Actions:
- Edit app.py to add validation, error handling, and loading-state logic
- Edit backend/story_engine.py only to adjust exception messages if needed for clearer user-facing errors — do not change its core logic or signature
- Use the browser subagent to run and click through the live app

Forbidden Actions:
- Do NOT change the visual design established in Phase 2
- Do NOT change the API contract (generate_story signature) or prompt template
- Do NOT deploy or push to git in this phase

Stop Conditions:
Pause and ask for human review when:
- The Gemini API key isn't set and the browser subagent can't actually test generation — report this instead of faking a pass
- An error can't be resolved in 2 attempts

Checkpoints:
After each fix, output: ✅ [what was completed]
At the end, output a full summary of every file changed and the results of each browser subagent test performed.
```

🎯 Target: Antigravity 2.0
💡 Explicitly directs the agent to use its browser subagent for real verification rather than just claiming the fixes work, since unverified "done" reports are the most common trust gap in agentic coding tools.

**Before pasting:** make sure a real (not placeholder) Gemini API key is in `.streamlit/secrets.toml` locally, or the browser subagent test step won't produce meaningful results.
