# AI Social Media Content Generator

A generative AI application that creates platform-ready social media captions, hashtags, and calls-to-action from a short topic description.

The project uses an LLM through Groq and provides both a Streamlit web interface and a command-line interface.

**🔗 Live demo (interactive preview):** https://ai-social-media-content-generator-mv7injpvb5pndh52tupsqc.streamlit.app/

## Features

- AI-generated social media captions
- Hashtag generation
- Optional calls-to-action
- Multiple content variations
- Platform-aware content generation
- Tone selection
- Character-count validation
- Streamlit web interface
- Command-line interface
- Structured JSON response parsing

## Tech Stack

- Python
- Streamlit
- Groq API
- Generative AI / LLM
- JSON
- Prompt Engineering

## Project Structure

| File | Purpose |
|---|---|
| `generator.py` | Core generation and prompt logic |
| `app.py` | Streamlit web application |
| `cli.py` | Command-line interface |
| `requirements.txt` | Python dependencies |

## Installation

```bash
git clone <your-repository-url>
cd AI-Social-Media-Content-Generator
pip install -r requirements.txt
```

## API Key Configuration

Create a Groq API key (free) at https://console.groq.com/keys and store it as an environment variable — or paste it directly into the app's sidebar at runtime.

**Windows:**
```bash
setx GROQ_API_KEY "your-key-here"
```

Open a new terminal after setting the variable.

**macOS/Linux:**
```bash
export GROQ_API_KEY="your-key-here"
```

Never commit API keys or other secrets to GitHub.

## Run the Web App

```bash
streamlit run app.py
```

This opens the app at `http://localhost:8501`. Enter a topic, pick a platform/tone/number of variations, and click **Generate posts**.

## Run the CLI

```bash
python cli.py "Launching our college tech fest" --platform instagram --tone Funny
```

## Deploying Your Own Public Link

To get a real, shareable `*.streamlit.app` URL (Streamlit Community Cloud is free):

1. Push this project to a public (or private) GitHub repo.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select the repo and branch, and set the main file to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your-key-here"
   ```
5. Click **Deploy**. Your app will be live at `https://<your-app-name>.streamlit.app` within a minute or two.

## Live Demo

A working interactive preview of the generator's UI and logic is hosted here:

**👉https://ai-social-media-content-generator-mv7injpvb5pndh52tupsqc.streamlit.app/
> Note: the hosted preview is an HTML/JS recreation of this Streamlit app for quick testing without any setup — it uses Claude instead of Groq under the hood, so wording will differ slightly from your local Streamlit app. For the real Groq-backed Streamlit app, run it locally or deploy it yourself with the steps above.

## How It Works

```text
User Input
    ↓
Prompt Construction
    ↓
LLM Inference
    ↓
JSON Parsing
    ↓
Content Validation
    ↓
Generated Social Media Content
```

1. The user provides a topic, platform, tone, and desired number of variations.
2. The application builds a structured prompt.
3. The prompt is sent to the selected LLM through Groq.
4. The generated response is parsed into structured JSON.
5. The application displays captions, hashtags, CTAs, and character counts.

## Model Configuration

The model is configured in `generator.py` (and selectable in the Streamlit sidebar). Model availability can change over time, so use a currently supported Groq model when configuring the application.

## Possible Extensions

- Add image generation
- Suggest optimal posting times
- Save generated posts to CSV or SQLite
- Add content-calendar functionality
- Add more platform-specific controls
