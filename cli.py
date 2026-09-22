"""
cli.py
Command-line version of the AI Social Media Content Generator.

Example:
    python cli.py "Launching our college tech fest" --platform instagram --tone Funny --variations 3
"""

import argparse
from generator import generate_posts


def main():
    parser = argparse.ArgumentParser(description="AI Social Media Content Generator (CLI)")
    parser.add_argument("topic", help="What the post should be about")
    parser.add_argument(
        "--platform",
        default="instagram",
        choices=["instagram", "twitter", "linkedin", "facebook"],
    )
    parser.add_argument("--tone", default="Casual")
    parser.add_argument("--variations", type=int, default=3)
    parser.add_argument("--no-cta", action="store_true", help="Exclude a call-to-action")
    args = parser.parse_args()

    results = generate_posts(
        topic=args.topic,
        platform=args.platform,
        tone=args.tone,
        variations=args.variations,
        include_cta=not args.no_cta,
    )

    for i, item in enumerate(results, start=1):
        print(f"\n--- Draft {i} ({args.platform}) ---")
        print(item.get("caption", ""))
        if item.get("cta"):
            print(item["cta"])
        hashtags = item.get("hashtags", [])
        if hashtags:
            print(" ".join(f"#{h}" for h in hashtags))


if __name__ == "__main__":
    main()
