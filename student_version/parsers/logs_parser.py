"""
logs_parser.py — Parse messy application usage logs and run analytics.
Uses ONLY Python built-in libraries.
"""

import re
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.cleaning import (
    normalize_whitespace, is_blank_or_junk,
    print_header, print_subheader, print_stat, print_table,
    print_warning, print_ok, color,
)

# ─── Date formats in log files ──────────────────────────────────────────────

_DATE_FMTS = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%Y-%m-%d %H:%M",
]

def _parse_log_date(raw: str) -> datetime | None:
    raw = raw.strip()
    for fmt in _DATE_FMTS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


# ─── Regex for a valid log line ─────────────────────────────────────────────

# Captures: timestamp, user_id, action, module, status, duration
_LOG_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})'
    r'[\t ]+(\w+)'          # user_id
    r'[\t ]+(\w+)'          # action
    r'[\t ]+(\w+)'          # module
    r'[\t ]+(\w+)'          # status
    r'(?:[\t ]+(.*))?$'     # duration (optional)
)

# Pattern for lines that have data but are missing user_id (only 5 fields)
_LOG_PATTERN_NO_USER = re.compile(
    r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})'
    r'[\t ]+(\w+)'          # action (no user_id)
    r'[\t ]+(\w+)'          # module
    r'[\t ]+(\w+)'          # status
    r'(?:[\t ]+(.*))?$'     # duration (optional)
)


# ─── Parsing ────────────────────────────────────────────────────────────────

def parse_usage_logs(filepath: str) -> tuple[list[dict], list[str]]:
    """
    Parse a messy usage log file.

    Returns
    -------
    entries : list[dict]
        Each dict: 'datetime', 'user_id', 'action', 'module', 'status', 'duration_ms'
    warnings : list[str]
    """
    entries: list[dict] = []
    warnings: list[str] = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return entries, [f"File not found: {filepath}"]

    for line_num, line in enumerate(lines, 1):
        line = line.rstrip("\n")

        # Skip blank, junk, or header lines
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.upper().startswith("TIMESTAMP"):
            continue  # header row

        # Try full pattern (6 fields)
        m = _LOG_PATTERN.match(stripped)
        if m:
            ts_raw, user_id, action, module, status, dur_raw = m.groups()
            dt = _parse_log_date(ts_raw)
            if dt is None:
                warnings.append(f"Line {line_num}: bad timestamp '{ts_raw}'")
                continue

            # Parse duration
            duration = None
            if dur_raw:
                dur_raw = dur_raw.strip()
                try:
                    duration = int(dur_raw)
                except ValueError:
                    # Non-numeric duration (e.g., "timeout") — keep as note
                    duration = None

            entries.append({
                "datetime": dt,
                "user_id": user_id,
                "action": action,
                "module": module,
                "status": status.upper(),
                "duration_ms": duration,
            })
            continue

        # Try pattern without user_id (5 fields)
        m = _LOG_PATTERN_NO_USER.match(stripped)
        if m:
            ts_raw, action, module, status, dur_raw = m.groups()
            dt = _parse_log_date(ts_raw)
            if dt is None:
                warnings.append(f"Line {line_num}: bad timestamp '{ts_raw}'")
                continue

            duration = None
            if dur_raw:
                try:
                    duration = int(dur_raw.strip())
                except ValueError:
                    duration = None

            entries.append({
                "datetime": dt,
                "user_id": "UNKNOWN",
                "action": action,
                "module": module,
                "status": status.upper(),
                "duration_ms": duration,
            })
            warnings.append(f"Line {line_num}: missing user_id — recorded as UNKNOWN")
            continue

        # Continuation or corrupt line
        if stripped.lower().startswith("continuation"):
            # Attach as note to previous entry
            if entries:
                prev = entries[-1]
                prev["action"] += f" (+continuation)"
            continue

        warnings.append(f"Line {line_num}: unparseable → {stripped[:60]}")

    return entries, warnings


# ─── Analytics ──────────────────────────────────────────────────────────────

def analyze_logs(filepath: str) -> None:
    """Parse and print full analytics for usage logs."""

    print_header("📊 Usage Logs Analysis")
    print_stat("File", filepath)

    entries, warnings = parse_usage_logs(filepath)

    if not entries:
        print_warning("No log entries parsed.")
        return

    print_ok(f"Parsed {len(entries)} log entries successfully")
    if warnings:
        print_warning(f"{len(warnings)} warnings during parsing")
        for w in warnings[:5]:
            print_warning(f"  {w}")
        if len(warnings) > 5:
            print_warning(f"  … and {len(warnings) - 5} more")

    # ── Most used features / actions ─────────────────────────────────────
    print_subheader("Most Used Features (Actions)")
    action_counts = Counter(e["action"] for e in entries)
    rows = [[action, str(count)] for action, count in action_counts.most_common(10)]
    print_table(["Action", "Count"], rows)

    # ── Module usage ─────────────────────────────────────────────────────
    print_subheader("Module Usage")
    module_counts = Counter(e["module"] for e in entries)
    rows = [[mod, str(count)] for mod, count in module_counts.most_common()]
    print_table(["Module", "Count"], rows)

    # ── Peak usage hour ──────────────────────────────────────────────────
    print_subheader("Activity by Hour")
    hour_counts = Counter(e["datetime"].hour for e in entries)
    bar_max = max(hour_counts.values()) if hour_counts else 1
    for h in range(24):
        count = hour_counts.get(h, 0)
        bar = "█" * int(count / bar_max * 30) if bar_max else ""
        print(f"    {h:02d}:00 │ {bar} {count}")

    peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else None
    if peak_hour is not None:
        print_stat("Peak hour", f"{peak_hour:02d}:00 ({hour_counts[peak_hour]} events)")

    # ── Error rate ───────────────────────────────────────────────────────
    print_subheader("Error Analysis")
    total = len(entries)
    errors = [e for e in entries if e["status"] in ("ERROR", "FAILED")]
    error_rate = len(errors) / total * 100 if total else 0
    print_stat("Total events", total)
    print_stat("Errors / Failures", len(errors))
    print_stat("Error rate", f"{error_rate:.1f}%")

    if errors:
        print_subheader("Error Breakdown")
        error_actions = Counter(
            f"{e['action']} ({e['module']})" for e in errors
        )
        rows = [[action, str(count)] for action, count in error_actions.most_common()]
        print_table(["Action (Module)", "Count"], rows)

    # ── Unique users ─────────────────────────────────────────────────────
    print_subheader("User Activity")
    user_counts = Counter(e["user_id"] for e in entries)
    print_stat("Unique users", len(user_counts))
    rows = [[uid, str(count)] for uid, count in user_counts.most_common()]
    print_table(["User", "Events"], rows)

    # ── Response time stats ──────────────────────────────────────────────
    print_subheader("Response Time (where available)")
    durations = [e["duration_ms"] for e in entries if e["duration_ms"] is not None]
    if durations:
        print_stat("Average", f"{sum(durations)/len(durations):.0f} ms")
        print_stat("Min", f"{min(durations)} ms")
        print_stat("Max", f"{max(durations)} ms")
        print_stat("P50 (median)", f"{sorted(durations)[len(durations)//2]} ms")
        p95_idx = int(len(durations) * 0.95)
        print_stat("P95", f"{sorted(durations)[p95_idx]} ms")
    else:
        print_warning("No duration data available")

    # ── Daily activity ───────────────────────────────────────────────────
    print_subheader("Daily Activity")
    day_counts = Counter(e["datetime"].strftime("%Y-%m-%d (%A)") for e in entries)
    rows = [[day, str(count)] for day, count in sorted(day_counts.items())]
    print_table(["Day", "Events"], rows)

    print()


# ─── Standalone execution ───────────────────────────────────────────────────

if __name__ == "__main__":
    default = os.path.join(os.path.dirname(__file__), "..", "sample_data", "usage_logs.txt")
    path = sys.argv[1] if len(sys.argv) > 1 else default
    analyze_logs(path)
