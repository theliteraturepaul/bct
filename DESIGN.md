# Design Specification — AI Story Generator

## 1. Visual Style: Glassmorphism

Frosted-glass surfaces floating over a soft gradient background. Depth comes from blur + transparency + subtle borders, not shadows or skeuomorphism.

**Core principles**
- Translucent panels (`backdrop-filter: blur`) over a colorful, blurred gradient background
- Thin, light-colored borders (1px) to fake the "edge of glass" refraction
- Soft, diffused shadows — never hard-edged
- Rounded corners everywhere (16–24px)
- Generous whitespace; content should float, not crowd

## 2. Color Palette

| Token | Value | Use |
|---|---|---|
| `--bg-gradient-start` | `#6D5BBA` | Background gradient top |
| `--bg-gradient-end` | `#8CB8FF` | Background gradient bottom |
| `--glass-bg` | `rgba(255, 255, 255, 0.12)` | Card/panel fill |
| `--glass-border` | `rgba(255, 255, 255, 0.25)` | Card border |
| `--glass-bg-strong` | `rgba(255, 255, 255, 0.22)` | Primary button fill |
| `--text-primary` | `#FFFFFF` | Headings, primary text |
| `--text-secondary` | `rgba(255, 255, 255, 0.75)` | Labels, helper text |
| `--accent` | `#FFD166` | Genre tags, highlights, focus rings |
| `--shadow` | `rgba(31, 38, 135, 0.25)` | Card drop shadow |

Background: a fixed, slowly-shifting diagonal gradient (`--bg-gradient-start` → `--bg-gradient-end`), optionally with 2–3 large blurred color blobs behind the glass layer for depth.

## 3. Typography

- Font: **Poppins** (headings) + **Inter** (body) — load both from Google Fonts
- H1 (app title): 32px, 600 weight, white, subtle text-shadow `0 2px 12px rgba(0,0,0,0.2)`
- Body/labels: 15–16px, 400–500 weight
- Story output: 17px, 1.7 line-height, serif-leaning font optional (e.g., "Lora") for readability of long text

## 4. Component Specs

**App background**
- Full-viewport gradient, fixed (doesn't scroll with content)
- 2 blurred radial color blobs (accent + secondary hue) positioned off-center for visual interest

**Main glass card (input panel)**
- `background: var(--glass-bg)`
- `backdrop-filter: blur(16px)`
- `border: 1px solid var(--glass-border)`
- `border-radius: 20px`
- `box-shadow: 0 8px 32px var(--shadow)`
- Padding: 32px

**Genre selector**
- Rendered as pill-style chips, not a plain dropdown, if time allows (falls back to `st.selectbox` styled to match glass theme if not)
- Selected chip: filled with `--accent`, dark text for contrast
- Unselected chip: glass style, white text

**Prompt input**
- Multi-line text area, glass-styled, `--text-primary` text on transparent fill
- Placeholder text in `--text-secondary`

**Length control**
- Segmented control or slider (Short / Medium / Long), glass-styled track

**Generate button**
- Full-width or prominent, `--glass-bg-strong` fill, `--accent` colored text or icon
- Hover: slight scale-up (1.02) + brighter glow
- Loading state: spinner + "Writing your story..." label, button disabled

**Story output card**
- Separate glass panel below the input, appears only after generation
- Rounded, blurred, same border treatment as input card
- Scrollable if content overflows a max-height
- "Regenerate" as a smaller secondary glass button beneath the story

## 5. Layout & Spacing

- Single centered column, max-width ~720px, on a full-bleed gradient background
- Vertical rhythm: 24px between major sections
- Mobile: card padding reduces to 20px, font sizes step down ~1px, single-column throughout (already default)

## 6. Accessibility Note (important — do not skip)

Glassmorphism's transparency can wreck text contrast. Enforce:
- Text is **always** `--text-primary` (white) or `--text-secondary` on glass — never dark text on light glass
- If a judge/user has a bright background image behind the glass, add a dark scrim (`rgba(0,0,0,0.15)`) between background and glass layer to guarantee contrast ratio ≥ 4.5:1 for body text
- Buttons need a visible focus outline (`--accent`, 2px) for keyboard navigation — don't rely on blur/glow alone

## 7. Implementation Note for Streamlit

Streamlit doesn't support this styling natively. It must be injected via:
```python
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```
This CSS block owns: the body background gradient, `.stApp` overrides, custom classes for glass cards wrapped around Streamlit's native containers, and Google Fonts `@import`. Keep all of this in one `assets/style.css` file, loaded once — do not scatter inline styles across the app.
