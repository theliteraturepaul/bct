# AI Story Generator

An interactive, AI-powered short story generator built with Streamlit and the Gemini API. Featuring a custom glassmorphism design system (inspired by modern pastel themes), users can input a prompt, select their favorite genre, and choose a length to instantly generate compelling stories.

## Tech Stack
- **Frontend Framework:** Streamlit
- **Language Model:** Gemini API (`gemini-2.5-flash`)
- **SDK:** `google-generativeai` (Python)
- **Styling:** Custom injected CSS (Light Pastel Glassmorphism UI)

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd story-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Create a `.streamlit/secrets.toml` file in the project root and add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Live Demo
[Live Demo Link (to be added after deployment)](#)
