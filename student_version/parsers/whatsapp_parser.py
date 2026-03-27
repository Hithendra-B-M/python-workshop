"""
whatsapp_parser.py — STUDENT VERSION
Parse messy WhatsApp chat exports and run analytics.
Uses ONLY Python built-in libraries.

╔══════════════════════════════════════════════════════════╗
║  🎓 STUDENT EXERCISES                                   ║
║  Functions marked with TODO are YOUR tasks to complete.  ║
║  Look for: # ✏️ EXERCISE                                ║
║  There are 3 exercises in this file.                     ║
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


# ─── Date Parsing (provided) ────────────────────────────────────────────────

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

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE 1: Multi-line Message Handling          ║
    ║                                                      ║
    ║  WhatsApp messages can span multiple lines.          ║
    ║  A continuation line does NOT start with a           ║
    ║  timestamp pattern. You need to append it to         ║
    ║  the previous message.                               ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐⭐ (Medium-Hard)                   ║
    ║  ESTIMATED TIME: 25 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Read all lines from the file                     ║
    ║  2. For each line, try to match _MSG_PATTERN         ║
    ║  3. If it matches → new message dict                 ║
    ║  4. If not, try _SYSTEM_PATTERN → skip               ║
    ║  5. Otherwise → it's a continuation line,            ║
    ║     append it to messages[-1]["message"]             ║
    ╚══════════════════════════════════════════════════════╝
    """
    messages: list[dict] = []
    warnings: list[str] = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print_warning(f"File not found: {filepath}")
        return messages, [f"File not found: {filepath}"]

    # ─── TODO: Implement the parsing loop ────────────────────────────────
    #
    # Loop through each line and:
    #   1. Skip blank lines
    #   2. Try matching _MSG_PATTERN → extract datetime, sender, message
    #   3. Try matching _SYSTEM_PATTERN → skip (system message)
    #   4. If no match → continuation line, append to last message
    #
    # Each message dict should look like:
    #   {"datetime": <datetime obj>, "sender": "Name", "message": "text"}
    #
    # Use _try_parse_date() to parse the timestamp string.
    # Use normalize_whitespace() to clean the sender name.
    #
    # YOUR CODE HERE:
    # for line in lines:
    #     ...
    pass  # ← Remove this when you add your code

    return messages, warnings


# ─── Analytics ──────────────────────────────────────────────────────────────

def _word_freq(messages: list[dict]) -> Counter:
    """
    Count word frequency across all messages, ignoring stop words.

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE 2: Word Frequency Counter               ║
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
    #     ...
    pass  # ← Remove this when you add your code

    return counter


def _messages_per_hour(messages: list[dict]) -> None:
    """
    Print a horizontal bar chart showing message count per hour (0–23).

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE 3: Hourly Activity Heatmap              ║
    ║                                                      ║
    ║  Create a bar chart showing how many messages        ║
    ║  were sent during each hour of the day.              ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐ (Medium)                           ║
    ║  ESTIMATED TIME: 15 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Use Counter() to count messages by hour          ║
    ║     (msg["datetime"].hour gives you the hour)        ║
    ║  2. Find the max count (for bar scaling)             ║
    ║  3. Loop 0..23 and print a bar:                      ║
    ║     "█" * int(count / max_count * 30)                ║
    ║                                                      ║
    ║  Expected output format:                             ║
    ║     08:00 │ ████████████████ 12                      ║
    ║     09:00 │ █████████ 7                              ║
    ╚══════════════════════════════════════════════════════╝
    """
    print_subheader("Messages Per Hour")

    # YOUR CODE HERE:
    # hour_counts = Counter(...)
    # bar_max = ...
    # for h in range(24):
    #     ...
    print("    (Not implemented yet — complete Exercise 3!)")


def analyze_whatsapp(filepath: str) -> None:
    """Parse and print full analytics for a WhatsApp chat export."""

    print_header("📱 WhatsApp Chat Analysis")
    print_stat("File", filepath)

    messages, warnings = parse_whatsapp(filepath)

    if not messages:
        print_warning("No messages parsed. Did you complete Exercise 1?")
        return

    print_ok(f"Parsed {len(messages)} messages successfully")
    if warnings:
        print_warning(f"Skipped {len(warnings)} problematic lines")

    # ── Most active sender (provided) ────────────────────────────────────
    print_subheader("Most Active Senders")
    sender_counts = Counter(m["sender"] for m in messages)
    rows = [[name, str(count)] for name, count in sender_counts.most_common()]
    print_table(["Sender", "Messages"], rows)

    # ── Busiest day (provided) ───────────────────────────────────────────
    print_subheader("Busiest Days")
    day_counts = Counter(m["datetime"].strftime("%Y-%m-%d (%A)") for m in messages)
    rows = [[day, str(count)] for day, count in day_counts.most_common(5)]
    print_table(["Day", "Messages"], rows)

    # ── Messages per hour — EXERCISE 3 ──────────────────────────────────
    _messages_per_hour(messages)

    # ── Most frequent words — EXERCISE 2 ─────────────────────────────────
    print_subheader("Top 15 Most Frequent Words")
    wf = _word_freq(messages)
    if wf:
        rows = [[word, str(count)] for word, count in wf.most_common(15)]
        print_table(["Word", "Count"], rows)
    else:
        print("    (Not implemented yet — complete Exercise 2!)")

    # ── Media messages (provided) ────────────────────────────────────────
    print_subheader("Media Summary")
    media_count = sum(1 for m in messages if "<media omitted>" in m["message"].lower())
    print_stat("Media messages", media_count)
    print_stat("Text messages", len(messages) - media_count)

    # ── Avg message length (provided) ────────────────────────────────────
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
