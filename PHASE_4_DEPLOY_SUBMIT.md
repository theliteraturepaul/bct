# Phase 4 — Deployment & Submission Prep

**Goal:** Get the app live on Streamlit Community Cloud and produce a submission-ready README, safely (no leaked keys).

**Depends on:** Phase 1–3 complete and tested locally

---

## Prompt for Antigravity 2.0

```
Context (carry forward):
- App is fully built, styled, and tested locally (Phases 1-3 complete).
- Secrets currently live only in local .streamlit/secrets.toml, which is gitignored.

Objective:
Prepare the repository for a clean GitHub push and Streamlit Community Cloud deployment, and write a submission-ready README. Do not attempt to create Streamlit Cloud accounts or perform the actual cloud deployment click-through — that requires human action in a browser with login.

Starting State:
Working local app, not yet pushed to GitHub.

Target State:
- .gitignore verified to exclude .streamlit/secrets.toml and any __pycache__/venv artifacts
- requirements.txt verified to contain exact packages used (streamlit, google-generativeai) with no unused entries
- README.md written with: project title, one-paragraph description, tech stack, setup instructions (clone, pip install -r requirements.txt, add GEMINI_API_KEY to .streamlit/secrets.toml, streamlit run app.py), and a placeholder line for the live demo link to be filled in after deployment
- A final local smoke test: run the app one more time and confirm no console errors on startup

Allowed Actions:
- Edit .gitignore, requirements.txt, README.md
- Run the app locally to smoke test
- Initialize git and stage files if not already a git repo (do not push)

Forbidden Actions:
- Do NOT push to GitHub or any remote
- Do NOT include any real API key anywhere in tracked files
- Do NOT create or log into any external accounts (GitHub, Streamlit Cloud) — flag these as manual human steps instead

Stop Conditions:
Pause and ask for human review when:
- Any file staged for commit contains what looks like a real API key or secret
- Before any git push is attempted (should not happen per Forbidden Actions, but stop immediately if it does)

Checkpoints:
After each step, output: ✅ [what was completed]
At the end, output the exact remaining manual steps for the human: push to GitHub, create the Streamlit Cloud app pointing at the repo, add GEMINI_API_KEY under App Settings > Secrets, and verify the live link.
```

🎯 Target: Antigravity 2.0
💡 Deliberately walls off account creation and git push as human-only steps — an agent pushing to a public repo or handling real cloud credentials unsupervised is exactly the failure mode worth avoiding the night before a submission.

**Manual steps after this phase (do these yourself):**
1. Push the repo to GitHub
2. Go to share.streamlit.io → New app → point at your repo/branch/`app.py`
3. In the deployed app's Settings → Secrets, add `GEMINI_API_KEY = "your-real-key"`
4. Open the live link and test it exactly like a judge would — empty prompt, normal prompt, and Regenerate
5. Drop the live link into your README and into your submission form
