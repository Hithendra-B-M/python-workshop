"""
main.py — CLI entry point for the Messy Export Parser.
Run:  python main.py [whatsapp|bank|logs|all]
"""

import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(__file__))

from parsers.whatsapp_parser import analyze_whatsapp
from parsers.bank_parser import analyze_bank
from parsers.logs_parser import analyze_logs
from utils.cleaning import print_header, print_stat, color


# ─── Default data paths ────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
DEFAULTS = {
    "whatsapp": os.path.join(DATA_DIR, "whatsapp_chat.txt"),
    "bank":     os.path.join(DATA_DIR, "bank_statement.csv"),
    "logs":     os.path.join(DATA_DIR, "usage_logs.txt"),
}


# ─── Banner ─────────────────────────────────────────────────────────────────

BANNER = r"""
  ███╗   ███╗███████╗███████╗███████╗██╗   ██╗
  ████╗ ████║██╔════╝██╔════╝██╔════╝╚██╗ ██╔╝
  ██╔████╔██║█████╗  ███████╗███████╗ ╚████╔╝
  ██║╚██╔╝██║██╔══╝  ╚════██║╚════██║  ╚██╔╝
  ██║ ╚═╝ ██║███████╗███████║███████║   ██║
  ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  █ E X P O R T   P A R S E R              █
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""


def show_usage():
    print(color(BANNER, "CYAN"))
    print(color("  Usage:", "BOLD"))
    print("    python main.py whatsapp   — Parse & analyze WhatsApp chat")
    print("    python main.py bank       — Parse & analyze bank statement")
    print("    python main.py logs       — Parse & analyze usage logs")
    print("    python main.py all        — Run all three analyses")
    print()
    print(color("  Options:", "BOLD"))
    print("    python main.py whatsapp <filepath>  — Use a custom file")
    print("    python main.py bank <filepath>")
    print("    python main.py logs <filepath>")
    print()


def main():
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(0)

    command = sys.argv[1].lower()
    custom_path = sys.argv[2] if len(sys.argv) > 2 else None

    print(color(BANNER, "CYAN"))

    if command == "whatsapp":
        path = custom_path or DEFAULTS["whatsapp"]
        analyze_whatsapp(path)

    elif command == "bank":
        path = custom_path or DEFAULTS["bank"]
        analyze_bank(path)

    elif command == "logs":
        path = custom_path or DEFAULTS["logs"]
        analyze_logs(path)

    elif command == "all":
        analyze_whatsapp(DEFAULTS["whatsapp"])
        analyze_bank(DEFAULTS["bank"])
        analyze_logs(DEFAULTS["logs"])

        print_header("✅ All Analyses Complete")
        print_stat("Parsers run", "3/3 (WhatsApp, Bank, Logs)")
        print()

    else:
        print(color(f"  Unknown command: '{command}'", "RED"))
        print()
        show_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
