"""
bank_parser.py — STUDENT VERSION
Parse messy bank statement CSVs and run analytics.
Uses ONLY Python built-in libraries.

╔══════════════════════════════════════════════════════════╗
║  🎓 STUDENT EXERCISE                                    ║
║  There is 1 exercise in this file.                      ║
║  Look for: # ✏️ EXERCISE                                ║
╚══════════════════════════════════════════════════════════╝
"""

import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.cleaning import (
    normalize_whitespace, safe_float, is_blank_or_junk,
    print_header, print_subheader, print_stat, print_table,
    print_warning, print_ok, print_error, color,
)


# ─── Date Parsing ───────────────────────────────────────────────────────────

def _parse_bank_date(raw: str) -> datetime | None:
    """
    Parse a date string that could be in any of these formats:
      - DD/MM/YYYY  (e.g., 01/03/2024)
      - YYYY-MM-DD  (e.g., 2024-03-02)
      - DD-MM-YYYY  (e.g., 03-03-2024)
      - MM/DD/YYYY  (e.g., 03/05/2024)

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE: Multi-Format Date Parser               ║
    ║                                                      ║
    ║  Bank statements use inconsistent date formats.      ║
    ║  Try each format with datetime.strptime() and        ║
    ║  return the first one that works.                    ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐ (Medium)                           ║
    ║  ESTIMATED TIME: 15 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Strip whitespace from raw input                  ║
    ║  2. Create a list of format strings to try:          ║
    ║     "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"  ║
    ║  3. Loop through formats, try strptime()             ║
    ║  4. If ValueError → try next format                  ║
    ║  5. If nothing works → return None                   ║
    ╚══════════════════════════════════════════════════════╝
    """
    # YOUR CODE HERE:
    # raw = raw.strip()
    # date_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
    # for fmt in date_formats:
    #     try:
    #         return datetime.strptime(raw, fmt)
    #     except ValueError:
    #         continue
    # return None
    pass  # ← Remove this when you add your code


# ─── Parsing ────────────────────────────────────────────────────────────────

def parse_bank_statement(filepath: str) -> tuple[list[dict], list[str]]:
    """
    Parse a messy bank statement CSV.

    Returns
    -------
    transactions : list[dict]
        Each dict: 'date' (datetime), 'description' (str),
                   'debit' (float|None), 'credit' (float|None),
                   'balance' (float|None)
    warnings : list[str]
    """
    transactions: list[dict] = []
    warnings: list[str] = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader, 1):
                try:
                    # Skip blank / junk rows
                    raw_line = ",".join(row)
                    if is_blank_or_junk(raw_line):
                        continue
                    if not row or all(c.strip() == "" for c in row):
                        continue

                    # Must have at least 3 columns (Date, Description, Debit)
                    if len(row) < 3:
                        warnings.append(f"Row {row_num}: too few columns → {raw_line[:60]}")
                        continue

                    date_str = normalize_whitespace(row[0])
                    description = normalize_whitespace(row[1])
                    debit_str = row[2].strip() if len(row) > 2 else ""
                    credit_str = row[3].strip() if len(row) > 3 else ""
                    balance_str = row[4].strip() if len(row) > 4 else ""

                    # Parse date — uses YOUR Exercise function!
                    dt = _parse_bank_date(date_str)
                    if dt is None:
                        warnings.append(f"Row {row_num}: bad date '{date_str}' → {raw_line[:60]}")
                        continue

                    # Skip rows with empty description
                    if not description:
                        warnings.append(f"Row {row_num}: empty description — skipped")
                        continue

                    # Parse amounts
                    debit = safe_float(debit_str)
                    credit = safe_float(credit_str)
                    balance = safe_float(balance_str)

                    # Skip rows with no financial data at all
                    if debit is None and credit is None and balance is None:
                        warnings.append(f"Row {row_num}: no numeric data → {raw_line[:60]}")
                        continue

                    # Treat debit=0 as no debit
                    if debit is not None and debit == 0.0:
                        debit = None

                    transactions.append({
                        "date": dt,
                        "description": description,
                        "debit": debit,
                        "credit": credit,
                        "balance": balance,
                    })

                except Exception as e:
                    warnings.append(f"Row {row_num}: unexpected error — {e}")

    except FileNotFoundError:
        warnings.append(f"File not found: {filepath}")

    return transactions, warnings


# ─── Analytics ──────────────────────────────────────────────────────────────

def analyze_bank(filepath: str) -> None:
    """Parse and print full analytics for a bank statement."""

    print_header("🏦 Bank Statement Analysis")
    print_stat("File", filepath)

    transactions, warnings = parse_bank_statement(filepath)

    if not transactions:
        print_warning("No transactions parsed. Did you complete the Exercise?")
        return

    print_ok(f"Parsed {len(transactions)} transactions successfully")
    if warnings:
        print_warning(f"Skipped {len(warnings)} problematic rows")
        for w in warnings[:5]:
            print_warning(f"  {w}")
        if len(warnings) > 5:
            print_warning(f"  … and {len(warnings) - 5} more")

    # ── Highest spending day ─────────────────────────────────────────────
    print_subheader("Highest Spending Days")
    day_spending: defaultdict = defaultdict(float)
    for t in transactions:
        if t["debit"] is not None:
            day_spending[t["date"].strftime("%Y-%m-%d (%A)")] += t["debit"]
    sorted_days = sorted(day_spending.items(), key=lambda x: x[1], reverse=True)
    rows = [[day, f"₹ {amt:,.2f}"] for day, amt in sorted_days[:5]]
    print_table(["Day", "Total Spending"], rows)

    # ── Top merchants / descriptions ─────────────────────────────────────
    print_subheader("Top Merchants / Categories")
    desc_spending: defaultdict = defaultdict(float)
    for t in transactions:
        if t["debit"] is not None:
            # Extract merchant from description like "UPI/Swiggy/Food Order"
            parts = t["description"].split("/")
            merchant = parts[1] if len(parts) > 1 else parts[0]
            desc_spending[merchant.strip()] += t["debit"]
    sorted_merchants = sorted(desc_spending.items(), key=lambda x: x[1], reverse=True)
    rows = [[name, f"₹ {amt:,.2f}"] for name, amt in sorted_merchants[:10]]
    print_table(["Merchant", "Total Spent"], rows)

    # ── Monthly totals ───────────────────────────────────────────────────
    print_subheader("Monthly Summary")
    monthly_debit: defaultdict = defaultdict(float)
    monthly_credit: defaultdict = defaultdict(float)
    for t in transactions:
        month_key = t["date"].strftime("%Y-%m")
        if t["debit"]:
            monthly_debit[month_key] += t["debit"]
        if t["credit"]:
            monthly_credit[month_key] += t["credit"]
    all_months = sorted(set(list(monthly_debit.keys()) + list(monthly_credit.keys())))
    rows = [
        [m, f"₹ {monthly_debit.get(m, 0):,.2f}", f"₹ {monthly_credit.get(m, 0):,.2f}"]
        for m in all_months
    ]
    print_table(["Month", "Total Debits", "Total Credits"], rows)

    # ── Average transaction ──────────────────────────────────────────────
    print_subheader("Transaction Statistics")
    debits = [t["debit"] for t in transactions if t["debit"] is not None]
    credits = [t["credit"] for t in transactions if t["credit"] is not None]
    if debits:
        print_stat("Total debits", f"₹ {sum(debits):,.2f}")
        print_stat("Average debit", f"₹ {sum(debits)/len(debits):,.2f}")
        print_stat("Largest debit", f"₹ {max(debits):,.2f}")
        print_stat("Smallest debit", f"₹ {min(debits):,.2f}")
    if credits:
        print_stat("Total credits", f"₹ {sum(credits):,.2f}")
        print_stat("Average credit", f"₹ {sum(credits)/len(credits):,.2f}")

    # ── Transaction type breakdown ───────────────────────────────────────
    print_subheader("Transaction Type Breakdown")
    type_counts: Counter = Counter()
    for t in transactions:
        parts = t["description"].split("/")
        txn_type = parts[0].strip() if parts else "Unknown"
        type_counts[txn_type] += 1
    rows = [[typ, str(c)] for typ, c in type_counts.most_common()]
    print_table(["Type", "Count"], rows)

    print()


# ─── Standalone execution ───────────────────────────────────────────────────

if __name__ == "__main__":
    default = os.path.join(os.path.dirname(__file__), "..", "sample_data", "bank_statement.csv")
    path = sys.argv[1] if len(sys.argv) > 1 else default
    analyze_bank(path)
