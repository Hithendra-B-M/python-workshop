"""
cleaning.py — Shared utility functions for data cleaning.
Uses ONLY Python built-in libraries.
"""

import re
from datetime import datetime


# ─── Whitespace & Text Cleaning ─────────────────────────────────────────────

def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs into a single space and strip edges."""
    return re.sub(r'[ \t]+', ' ', text).strip()


def is_blank_or_junk(line: str) -> bool:
    """Return True if the line is empty, whitespace-only, or a repeated header."""
    stripped = line.strip()
    if not stripped:
        return True
    # Detect repeated CSV headers
    if stripped.lower().startswith("date,description") or stripped.lower().startswith("timestamp\t"):
        return True
    return False


# ─── Date Parsing ───────────────────────────────────────────────────────────

# Ordered so more specific / unambiguous formats are tried first.
_DATE_FORMATS = [
    # ISO-style
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    # DD/MM/YYYY
    "%d/%m/%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    # DD-MM-YYYY
    "%d-%m-%Y",
    "%d-%m-%Y %H:%M:%S",
    # MM/DD/YY  (WhatsApp US export)
    "%m/%d/%y",
    "%m/%d/%y, %I:%M %p",
    "%m/%d/%y, %H:%M",
    # DD/MM/YYYY without time (for bank statement)
    "%d/%m/%Y",
    # MM/DD/YYYY (alternate)
    "%m/%d/%Y %H:%M:%S",
]

# WhatsApp-specific patterns
_WHATSAPP_DATE_FORMATS = [
    "%m/%d/%y, %I:%M %p",      # 12/01/23, 9:05 AM
    "%d/%m/%Y, %H:%M",         # 01/12/2023, 10:30
    "%m/%d/%y, %H:%M",         # 12/01/23, 09:31
]


def parse_flexible_date(text: str, formats=None) -> datetime | None:
    """
    Try multiple datetime formats and return the first match.
    Returns None if nothing works.
    """
    if formats is None:
        formats = _DATE_FORMATS
    text = text.strip()
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def parse_whatsapp_date(text: str) -> datetime | None:
    """Parse WhatsApp-style dates that may use 12h or 24h format."""
    text = text.strip()
    for fmt in _WHATSAPP_DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    # Fallback to the general parser
    return parse_flexible_date(text)


# ─── Numeric Parsing ────────────────────────────────────────────────────────

_CURRENCY_RE = re.compile(r'[₹$€£,\s]')

def safe_float(text: str) -> float | None:
    """
    Parse a string that may contain currency symbols, commas, and spaces
    into a float.  Returns None on failure.
    """
    if text is None:
        return None
    cleaned = _CURRENCY_RE.sub('', text.strip())
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


# ─── Pretty Printing Helpers ────────────────────────────────────────────────

_COLORS = {
    "HEADER":  "\033[95m",
    "BLUE":    "\033[94m",
    "CYAN":    "\033[96m",
    "GREEN":   "\033[92m",
    "YELLOW":  "\033[93m",
    "RED":     "\033[91m",
    "BOLD":    "\033[1m",
    "RESET":   "\033[0m",
}


def color(text: str, name: str) -> str:
    """Wrap text with ANSI color codes."""
    return f"{_COLORS.get(name, '')}{text}{_COLORS['RESET']}"


def print_header(title: str) -> None:
    """Print a prominent section header."""
    width = 60
    print()
    print(color("═" * width, "CYAN"))
    print(color(f"  {title}", "BOLD"))
    print(color("═" * width, "CYAN"))


def print_subheader(title: str) -> None:
    """Print a subsection header."""
    print(f"\n  {color('▸ ' + title, 'YELLOW')}")


def print_stat(label: str, value, indent: int = 4) -> None:
    """Print a labeled statistic."""
    prefix = " " * indent
    print(f"{prefix}{color(label + ':', 'GREEN')} {value}")


def print_table(headers: list[str], rows: list[list[str]], indent: int = 4) -> None:
    """Print a simple ASCII table."""
    prefix = " " * indent
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Header
    header_line = " │ ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    separator = "─┼─".join("─" * widths[i] for i in range(len(headers)))
    print(f"{prefix}{color(header_line, 'BOLD')}")
    print(f"{prefix}{separator}")

    # Rows
    for row in rows:
        line = " │ ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row) if i < len(widths))
        print(f"{prefix}{line}")


def print_warning(msg: str) -> None:
    """Print a warning line."""
    print(f"    {color('⚠ ' + msg, 'YELLOW')}")


def print_error(msg: str) -> None:
    """Print an error line."""
    print(f"    {color('✗ ' + msg, 'RED')}")


def print_ok(msg: str) -> None:
    """Print a success line."""
    print(f"    {color('✓ ' + msg, 'GREEN')}")
