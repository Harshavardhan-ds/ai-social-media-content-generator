"""
generator.py
Core generative-AI logic for the AI Social Media Content Generator.

This module builds a prompt from the user's inputs, sends it to an LLM
via the Groq API (free), and parses the model's response into
structured post variations.
"""

import os
import json
import re
from typing import List, Dict

from groq import Groq

# Approximate character limits per platform (used for validation/warnings)
PLATFORM_LIMITS = {
    "instagram": 2200,
    "twitter": 280,
    "linkedin": 3000,
    "facebook": 63206,
}


def build_prompt(topic: str, platform: str, tone: str, variations: int, include_cta: bool) -> str:
    """Construct the prompt sent to the LLM (prompt engineering step)."""
    limit = PLATFORM_LIMITS.get(platform, 2200)
    cta_instruction = (
        "Each post must end with a short, natural call-to-action."
        if include_cta
        else "Do not include a call-to-action."
    )

    return f"""You are a social media copywriter. Generate {variations} distinct social
media post variations for the platform "{platform}" (character limit roughly
{limit}) about the following topic/product:

"{topic}"

Tone: {tone}.
{cta_instruction}

Respond with ONLY valid JSON, no markdown fences, no preamble, in exactly this shape:
[
  {{"caption": "string", "hashtags": ["tag1", "tag2"], "cta": "string or empty"}}
]

Rules:
- caption must fit within the platform's character limit, excluding hashtags.
- hashtags: 3 to 8 relevant, platform-appropriate hashtags, no "#" symbol included,
  lowercase, no spaces.
- Keep language natural and human, not robotic.
- Each variation should feel meaningfully different in angle or wording, not
  just a synonym swap."""


def extract_json(text: str) -> List[Dict]:
    """Strip any accidental markdown fences and parse the JSON array."""
    cleaned = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    json_slice = cleaned[start : end + 1] if start != -1 and end != -1 else cleaned
    return json.loads(json_slice)


def generate_posts(
    topic: str,
    platform: str = "instagram",
    tone: str = "Casual",
    variations: int = 3,
    include_cta: bool = True,
    model: str = "openai/gpt-oss-120b",
) -> List[Dict]:
    """
    Generate social media post variations using an LLM hosted on Groq (free tier).

    Requires the GROQ_API_KEY environment variable to be set.
    Returns a list of dicts: [{"caption": ..., "hashtags": [...], "cta": ...}, ...]
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Get a free key from https://console.groq.com/keys and set it, e.g.\n"
            "  export GROQ_API_KEY='your-key-here'   (Mac/Linux)\n"
            "  setx GROQ_API_KEY \"your-key-here\"     (Windows)"
        )

    client = Groq(api_key=api_key)
    prompt = build_prompt(topic, platform, tone, variations, include_cta)

    response = client.chat.completions.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    if not text:
        raise RuntimeError("Model returned no text content.")

    return extract_json(text)
