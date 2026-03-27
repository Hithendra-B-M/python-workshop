"""
bank_parser.py — STUDENT VERSION
Parse messy bank statement CSVs and run analytics.
Uses ONLY Python built-in libraries.

╔══════════════════════════════════════════════════════════╗
║  🎓 STUDENT EXERCISES                                   ║
║  Functions marked with TODO are YOUR tasks to complete.  ║
║  Look for: # ✏️ EXERCISE                                ║
║  There are 3 exercises in this file.                     ║
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
    ║  ✏️ EXERCISE 4: Multi-Format Date Parser             ║
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
    # date_formats = ["%d/%m/%Y", "%Y-%m-%d", ...]
    # for fmt in date_formats:
    #     try:
    #         return datetime.strptime(raw, fmt)
    #     except ValueError:
    #         continue
    # return None
    pass  # ← Remove this when you add your code


# ─── Parsing (provided) ─────────────────────────────────────────────────────

def parse_bank_statement(filepath: str) -> tuple[list[dict], list[str]]:
    """
    Parse a messy bank statement CSV.
    This function is PROVIDED — study it to understand how csv.reader
    handles messy data with error handling.

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

                    # Must have at least 3 columns
                    if len(row) < 3:
                        warnings.append(f"Row {row_num}: too few columns → {raw_line[:60]}")
                        continue

                    date_str = normalize_whitespace(row[0])
                    description = normalize_whitespace(row[1])
                    debit_str = row[2].strip() if len(row) > 2 else ""
                    credit_str = row[3].strip() if len(row) > 3 else ""
                    balance_str = row[4].strip() if len(row) > 4 else ""

                    # Parse date — uses YOUR Exercise 4 function!
                    dt = _parse_bank_date(date_str)
                    if dt is None:
                        warnings.append(f"Row {row_num}: bad date '{date_str}'")
                        continue

                    if not description:
                        warnings.append(f"Row {row_num}: empty description")
                        continue

                    debit = safe_float(debit_str)
                    credit = safe_float(credit_str)
                    balance = safe_float(balance_str)

                    if debit is None and credit is None and balance is None:
                        warnings.append(f"Row {row_num}: no numeric data")
                        continue

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
                    warnings.append(f"Row {row_num}: error — {e}")

    except FileNotFoundError:
        warnings.append(f"File not found: {filepath}")

    return transactions, warnings


# ─── Analytics ──────────────────────────────────────────────────────────────

def _top_merchants(transactions: list[dict]) -> None:
    """
    Extract and display the top spending merchants/categories.

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE 5: Merchant Spending Extractor          ║
    ║                                                      ║
    ║  Descriptions look like "UPI/Swiggy/Food Order".     ║
    ║  Extract the merchant name (2nd part after /)        ║
    ║  and sum up all debits per merchant.                 ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐ (Medium)                           ║
    ║  ESTIMATED TIME: 20 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Use a defaultdict(float) for totals              ║
    ║  2. Loop through transactions with debits            ║
    ║  3. Split description by "/" to get parts            ║
    ║  4. Merchant = parts[1] if len(parts) > 1           ║
    ║     else parts[0]                                    ║
    ║  5. Sort by total and display top 10                 ║
    ║  6. Use print_table(["Merchant","Spent"], rows)      ║
    ╚══════════════════════════════════════════════════════╝
    """
    print_subheader("Top Merchants / Categories")

    # YOUR CODE HERE:
    # desc_spending = defaultdict(float)
    # for t in transactions:
    #     if t["debit"] is not None:
    #         parts = t["description"].split("/")
    #         merchant = ...
    #         desc_spending[merchant] += t["debit"]
    # sorted_merchants = sorted(...)
    # rows = ...
    # print_table(["Merchant", "Total Spent"], rows)
    print("    (Not implemented yet — complete Exercise 5!)")


def _monthly_summary(transactions: list[dict]) -> None:
    """
    Display total debits and credits per month.

    ╔══════════════════════════════════════════════════════╗
    ║  ✏️ EXERCISE 6: Monthly Summary Aggregation          ║
    ║                                                      ║
    ║  Group all transactions by month and show            ║
    ║  total debits vs total credits per month.            ║
    ║                                                      ║
    ║  DIFFICULTY: ⭐⭐ (Medium)                           ║
    ║  ESTIMATED TIME: 20 minutes                          ║
    ║                                                      ║
    ║  HINTS:                                              ║
    ║  1. Use two defaultdict(float): one for debits,      ║
    ║     one for credits                                  ║
    ║  2. Get month key: t["date"].strftime("%Y-%m")       ║
    ║  3. Accumulate debits and credits separately         ║
    ║  4. Combine all month keys, sort them                ║
    ║  5. Display with print_table()                       ║
    ║  6. Format amounts as f"₹ {amt:,.2f}"               ║
    ╚══════════════════════════════════════════════════════╝
    """
    print_subheader("Monthly Summary")

    # YOUR CODE HERE:
    # monthly_debit = defaultdict(float)
    # monthly_credit = defaultdict(float)
    # for t in transactions:
    #     month_key = t["date"].strftime("%Y-%m")
    #     ...
    # rows = ...
    # print_table(["Month", "Total Debits", "Total Credits"], rows)
    print("    (Not implemented yet — complete Exercise 6!)")


def analyze_bank(filepath: str) -> None:
    """Parse and print full analytics for a bank statement."""

    print_header("🏦 Bank Statement Analysis")
    print_stat("File", filepath)

    transactions, warnings = parse_bank_statement(filepath)

    if not transactions:
        print_warning("No transactions parsed. Did you complete Exercise 4?")
        return

    print_ok(f"Parsed {len(transactions)} transactions successfully")
    if warnings:
        print_warning(f"Skipped {len(warnings)} problematic rows")
        for w in warnings[:5]:
            print_warning(f"  {w}")

    # ── Highest spending day (provided) ──────────────────────────────────
    print_subheader("Highest Spending Days")
    day_spending: defaultdict = defaultdict(float)
    for t in transactions:
        if t["debit"] is not None:
            day_spending[t["date"].strftime("%Y-%m-%d (%A)")] += t["debit"]
    sorted_days = sorted(day_spending.items(), key=lambda x: x[1], reverse=True)
    rows = [[day, f"₹ {amt:,.2f}"] for day, amt in sorted_days[:5]]
    print_table(["Day", "Total Spending"], rows)

    # ── Top merchants — EXERCISE 5 ──────────────────────────────────────
    _top_merchants(transactions)

    # ── Monthly summary — EXERCISE 6 ────────────────────────────────────
    _monthly_summary(transactions)

    # ── Transaction statistics (provided) ────────────────────────────────
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

    # ── Transaction type breakdown (provided) ────────────────────────────
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
