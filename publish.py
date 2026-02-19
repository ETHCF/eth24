#!/usr/bin/env python3
"""Format ETH24 output for CLI or tweet preview."""

import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG = json.loads((SCRIPT_DIR / "config.json").read_text())


def format_tweet(ranked):
    """Format ranked data as a single tweet."""
    stories = ranked.get("stories", [])
    highlights = ranked.get("highlights", "")
    date_label = ranked.get("date_label", datetime.now().strftime("%-m/%d/%y"))
    brand = CONFIG.get("brand", {})

    lines = [f"{brand.get('name', 'ETH24')} - {date_label}"]

    if highlights:
        lines.append(f"\n{highlights}")

    for s in stories:
        tweet_url = s.get("tweet_url", "")
        if not tweet_url:
            continue
        commentary = s.get("commentary", "")
        lines.append(f"\n{commentary}\n{tweet_url}")

    return "\n".join(lines)


def format_cli(ranked):
    """Format ranked data as plain text for stdout."""
    stories = ranked.get("stories", [])
    highlights = ranked.get("highlights", "")
    date_label = ranked.get("date_label", datetime.now().strftime("%-m/%d/%y"))
    brand = CONFIG.get("brand", {})

    lines = [f"{brand.get('name', 'ETH24')} - {date_label}"]

    if highlights:
        lines.append(f"\n{highlights}")

    for s in stories:
        tweet_url = s.get("tweet_url", "")
        if not tweet_url:
            continue
        commentary = s.get("commentary", "")
        lines.append(f"\n{commentary}\n  {tweet_url}")

    return "\n".join(lines)


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    ranked_path = SCRIPT_DIR / "output" / today / "ranked.json"

    if ranked_path.exists():
        ranked = json.loads(ranked_path.read_text())
    else:
        ranked = json.loads(sys.stdin.read())

    print(format_cli(ranked))


if __name__ == "__main__":
    main()
