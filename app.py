"""
app.py
Streamlit web application for the AI Social Media Content Generator.

Run with:
    streamlit run app.py

Requires the GROQ_API_KEY environment variable (or a key pasted into the
sidebar at runtime) — get a free key at https://console.groq.com/keys
"""

import os
import streamlit as st

from generator import generate_posts, PLATFORM_LIMITS

st.set_page_config(
    page_title="AI Social Media Content Generator",
    page_icon="✨",
    layout="wide",
)

# ---------- Sidebar: configuration ----------
with st.sidebar:
    st.header("⚙️ Settings")

    env_key = os.environ.get("GROQ_API_KEY", "")
    api_key_input = st.text_input(
        "Groq API key",
        value="",
        type="password",
        placeholder="gsk_..." if not env_key else "Using GROQ_API_KEY from environment",
        help="Get a free key at https://console.groq.com/keys. "
        "Leave blank to use the GROQ_API_KEY environment variable.",
    )
    active_key = api_key_input.strip() or env_key
    if active_key:
        os.environ["GROQ_API_KEY"] = active_key

    model = st.selectbox(
        "Model",
        options=["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
        help="Model availability can change over time on Groq's free tier.",
    )

    st.divider()
    st.caption(
        "This app calls the Groq API to generate captions, hashtags, and "
        "calls-to-action for your posts. Your API key stays local to this "
        "session and is never stored."
    )

# ---------- Main: inputs ----------
st.title("✨ AI Social Media Content Generator")
st.write(
    "Turn a short topic description into platform-ready captions, hashtags, "
    "and calls-to-action."
)

col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_area(
        "What's the post about?",
        placeholder="e.g. Launching our college tech fest next Friday",
        height=100,
    )

with col2:
    platform = st.selectbox("Platform", options=list(PLATFORM_LIMITS.keys()), index=0)
    tone = st.selectbox(
        "Tone",
        options=["Casual", "Funny", "Professional", "Inspirational", "Bold", "Minimal"],
        index=0,
    )
    variations = st.slider("Number of variations", min_value=1, max_value=6, value=3)
    include_cta = st.checkbox("Include a call-to-action", value=True)

generate_clicked = st.button("Generate posts", type="primary", use_container_width=True)

st.divider()

# ---------- Generation ----------
if generate_clicked:
    if not topic.strip():
        st.warning("Please enter a topic to generate posts about.")
    elif not os.environ.get("GROQ_API_KEY"):
        st.error(
            "No Groq API key found. Enter one in the sidebar, or set the "
            "GROQ_API_KEY environment variable before launching the app."
        )
    else:
        with st.spinner("Generating your posts..."):
            try:
                results = generate_posts(
                    topic=topic,
                    platform=platform,
                    tone=tone,
                    variations=variations,
                    include_cta=include_cta,
                    model=model,
                )
            except Exception as e:
                results = None
                st.error(f"Generation failed: {e}")

        if results:
            limit = PLATFORM_LIMITS.get(platform, 2200)
            for i, item in enumerate(results, start=1):
                caption = item.get("caption", "")
                cta = item.get("cta", "")
                hashtags = item.get("hashtags", [])
                char_count = len(caption)

                with st.container(border=True):
                    st.markdown(f"**Draft {i}**")
                    st.write(caption)
                    if cta:
                        st.write(f"*{cta}*")
                    if hashtags:
                        st.write(" ".join(f"#{h}" for h in hashtags))

                    if char_count > limit:
                        st.caption(
                            f":red[{char_count} / {limit} characters — over the {platform} limit]"
                        )
                    else:
                        st.caption(f"{char_count} / {limit} characters")

                    full_text = caption
                    if cta:
                        full_text += f"\n\n{cta}"
                    if hashtags:
                        full_text += "\n\n" + " ".join(f"#{h}" for h in hashtags)

                    st.download_button(
                        label="Copy / download this draft",
                        data=full_text,
                        file_name=f"draft_{i}.txt",
                        mime="text/plain",
                        key=f"download_{i}",
                    )
else:
    st.info("Fill in a topic on the left and click **Generate posts** to get started.")
