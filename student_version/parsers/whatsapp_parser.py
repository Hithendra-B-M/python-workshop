"""
whatsapp_parser.py — STUDENT VERSION
Parse messy WhatsApp chat exports and run analytics.
Uses ONLY Python built-in libraries.

╔══════════════════════════════════════════════════════════╗
║  🎓 STUDENT EXERCISE                                    ║
║  There is 1 exercise in this file.                      ║
║  Look for: # ✏️ EXERCISE                                ║
╚══════════════════════════════════════════════════════════╝
"""

import re
import os
import sys
from collections import Counter
from datetime import datetime

# ── Allow imports from project root ──────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.cleaning import (
    normalize_whitespace, is_blank_or_junk,
    print_header, print_subheader, print_stat, print_table,
    print_warning, print_ok, color,
)

# ─── Constants ──────────────────────────────────────────────────────────────

# Regex that captures the timestamp + sender + message start
# Covers patterns like:
#   12/01/23, 9:05 AM - Sender: Message
#   01/12/2023, 10:30 - Sender: Message
_MSG_PATTERN = re.compile(
    r'^(\d{1,2}/\d{1,2}/\d{2,4},?\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)\s*-\s*(.+?):\s*(.*)',
    re.IGNORECASE,
)

# System messages (no sender)
_SYSTEM_PATTERN = re.compile(
    r'^(\d{1,2}/\d{1,2}/\d{2,4},?\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)\s*-\s*(.*)',
    re.IGNORECASE,
)

# Date formats to attempt (ordered by specificity)
_DATE_FMTS = [
    "%m/%d/%y, %I:%M %p",   # 12/01/23, 9:05 AM
    "%m/%d/%y, %H:%M %p",   # 12/01/23, 09:31 AM
    "%m/%d/%y, %H:%M",      # 12/01/23, 09:31
    "%d/%m/%Y, %H:%M",      # 01/12/2023, 10:30
    "%m/%d/%Y, %H:%M",      # 2/12/2023, 09:30
]

# Words to exclude from "most frequent word"
_STOP_WORDS = {
    "i", "me", "my", "the", "a", "an", "is", "are", "was", "were",
    "it", "to", "of", "in", "on", "for", "and", "or", "but", "not",
    "this", "that", "with", "at", "by", "from", "be", "have", "has",
    "had", "do", "does", "did", "will", "would", "can", "could",
    "should", "shall", "may", "might", "let", "so", "if", "we",
    "you", "he", "she", "they", "them", "us", "its", "our", "your",
    "their", "been", "being", "am", "just", "about", "up", "out",
    "what", "how", "when", "where", "who", "which", "some", "all",
    "no", "yes", "also", "here", "there", "-", "–", "<media", "omitted>",
}


# ─── Date Parsing ───────────────────────────────────────────────────────────

def _try_parse_date(raw: str) -> datetime | None:
    raw = raw.strip()
    for fmt in _DATE_FMTS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


# ─── Parsing ────────────────────────────────────────────────────────────────

def parse_whatsapp(filepath: str) -> tuple[list[dict], list[str]]:
    """
    Parse a WhatsApp chat export file.

    Returns
    -------
    messages : list[dict]
        Each dict has keys: 'datetime', 'sender', 'message'
    warnings : list[str]
        Lines that could not be parsed.
    """
    messages: list[dict] = []
    warnings: list[str] = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print_warning(f"File not found: {filepath}")
        return messages, [f"File not found: {filepath}"]

    for line in lines:
        line = line.rstrip("\n")

        # Skip blank lines
        if not line.strip():
            continue

        # Try sender message first
        m = _MSG_PATTERN.match(line)
        if m:
            dt = _try_parse_date(m.group(1))
            sender = normalize_whitespace(m.group(2))
            msg = m.group(3)
            if dt:
                messages.append({
                    "datetime": dt,
                    "sender": sender,
                    "message": msg,
                })
            else:
                warnings.append(f"Bad date: {line[:60]}")
            continue

        # Try system message (no sender)
        m = _SYSTEM_PATTERN.match(line)
        if m:
            # System message — skip for analytics
            continue

        # Continuation line — append to last message
        if messages:
            messages[-1]["message"] += "\n" + line
        else:
            warnings.append(f"Orphan line: {line[:60]}")

    return messages, warnings


# ─── Analytics ──────────────────────────────────────────────────────────────

def _word_freq(messages: list[dict]) -> Counter:
    """
    Count word frequency across all messages, ignoring stop words.

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE: Word Frequency Counter                 ║
    ║                                                      ║
    ║  Count how often each word appears across all        ║
    ║  messages, but SKIP words in _STOP_WORDS and         ║
    ║  words shorter than 2 characters.                    ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐ (Medium)                           ║
    ║  ESTIMATED TIME: 15 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Create a Counter() object                        ║
    ║  2. Loop through each message's text                 ║
    ║  3. Convert to lowercase                             ║
    ║  4. Use re.sub(r'[^\w\s]', ' ', text) to remove     ║
    ║     emojis and special chars                         ║
    ║  5. Split into words → filter → count                ║
    ╚══════════════════════════════════════════════════════╝
    """
    counter: Counter = Counter()

    # YOUR CODE HERE:
    # for msg in messages:
    #     text = msg["message"].lower()
    #     text = re.sub(r'[^\w\s]', ' ', text)
    #     words = text.split()
    #     for w in words:
    #         if w not in _STOP_WORDS and len(w) > 1:
    #             counter[w] += 1
    pass  # ← Remove this when you add your code

    return counter


def analyze_whatsapp(filepath: str) -> None:
    """Parse and print full analytics for a WhatsApp chat export."""

    print_header("📱 WhatsApp Chat Analysis")
    print_stat("File", filepath)

    messages, warnings = parse_whatsapp(filepath)

    if not messages:
        print_warning("No messages parsed. Check the file format.")
        return

    print_ok(f"Parsed {len(messages)} messages successfully")
    if warnings:
        print_warning(f"Skipped {len(warnings)} problematic lines")

    # ── Most active sender ───────────────────────────────────────────────
    print_subheader("Most Active Senders")
    sender_counts = Counter(m["sender"] for m in messages)
    rows = [[name, str(count)] for name, count in sender_counts.most_common()]
    print_table(["Sender", "Messages"], rows)

    # ── Busiest day ──────────────────────────────────────────────────────
    print_subheader("Busiest Days")
    day_counts = Counter(m["datetime"].strftime("%Y-%m-%d (%A)") for m in messages)
    rows = [[day, str(count)] for day, count in day_counts.most_common(5)]
    print_table(["Day", "Messages"], rows)

    # ── Messages per hour ────────────────────────────────────────────────
    print_subheader("Messages Per Hour")
    hour_counts = Counter(m["datetime"].hour for m in messages)
    bar_max = max(hour_counts.values()) if hour_counts else 1
    for h in range(24):
        count = hour_counts.get(h, 0)
        bar = "█" * int(count / bar_max * 30) if bar_max else ""
        label = f"{h:02d}:00"
        print(f"    {label} │ {bar} {count}")

    # ── Most frequent words — EXERCISE ───────────────────────────────────
    print_subheader("Top 15 Most Frequent Words")
    wf = _word_freq(messages)
    if wf:
        rows = [[word, str(count)] for word, count in wf.most_common(15)]
        print_table(["Word", "Count"], rows)
    else:
        print("    (Not implemented yet — complete the Exercise!)")

    # ── Media messages ───────────────────────────────────────────────────
    print_subheader("Media Summary")
    media_count = sum(1 for m in messages if "<media omitted>" in m["message"].lower())
    print_stat("Media messages", media_count)
    print_stat("Text messages", len(messages) - media_count)

    # ── Avg message length ───────────────────────────────────────────────
    print_subheader("Message Length Stats")
    lengths = [len(m["message"]) for m in messages if "<media omitted>" not in m["message"].lower()]
    if lengths:
        print_stat("Average length", f"{sum(lengths)/len(lengths):.1f} chars")
        print_stat("Longest message", f"{max(lengths)} chars")
        print_stat("Shortest message", f"{min(lengths)} chars")

    print()


# ─── Standalone execution ───────────────────────────────────────────────────

if __name__ == "__main__":
    default = os.path.join(os.path.dirname(__file__), "..", "sample_data", "whatsapp_chat.txt")
    path = sys.argv[1] if len(sys.argv) > 1 else default
    analyze_whatsapp(path)
