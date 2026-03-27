# 🎓 Messy Export Parser — Student Workshop

> **Duration**: ~2 hours | **Difficulty**: Medium | **No external libraries needed**

---

## 🚀 Setup (5 minutes)

### Step 1: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Verify Setup

```bash
# Run the logs parser (this one is fully implemented)
python main.py logs
```

You should see colored output with usage log analytics. If this works, you're ready!

---

## 📋 Your Exercises (6 total)

You have **6 functions** to complete across 2 files. Each exercise has:
- ⭐ Difficulty rating
- ⏱️ Time estimate
- 💡 Detailed hints in the code comments

### WhatsApp Parser (`parsers/whatsapp_parser.py`)

| # | Exercise | Difficulty | Time | What You'll Learn |
|---|----------|-----------|------|-------------------|
| 1 | `parse_whatsapp()` — Multi-line message parsing | ⭐⭐⭐ | 25 min | Regex matching, line-by-line parsing, continuation handling |
| 2 | `_word_freq()` — Word frequency counter | ⭐⭐ | 15 min | Counter, text cleaning, stop word filtering |
| 3 | `_messages_per_hour()` — Hourly activity heatmap | ⭐⭐ | 15 min | Counter, datetime.hour, ASCII visualization |

### Bank Statement Parser (`parsers/bank_parser.py`)

| # | Exercise | Difficulty | Time | What You'll Learn |
|---|----------|-----------|------|-------------------|
| 4 | `_parse_bank_date()` — Multi-format date parser | ⭐⭐ | 15 min | datetime.strptime, try/except, multiple formats |
| 5 | `_top_merchants()` — Merchant spending extractor | ⭐⭐ | 20 min | String splitting, defaultdict, sorting |
| 6 | `_monthly_summary()` — Monthly aggregation | ⭐⭐ | 20 min | Date grouping, defaultdict, formatted output |

**Total estimated time**: ~110 minutes (~2 hours with breaks)

---

## 🎯 Recommended Order

```
Exercise 4  →  (unlocks the bank parser, so you see data flowing)
Exercise 1  →  (unlocks all WhatsApp analytics)
Exercise 2  →  (word frequency — builds on Exercise 1)
Exercise 3  →  (hourly chart — builds on Exercise 1)
Exercise 5  →  (merchant analysis)
Exercise 6  →  (monthly totals)
```

> **Start with Exercise 4** because it's the simplest and immediately
> unlocks the entire bank statement pipeline, giving you visible results fast!

---

## 🧪 How to Test Your Work

After completing each exercise, run the relevant parser:

```bash
# Test WhatsApp parser (after Exercises 1, 2, 3)
python main.py whatsapp

# Test Bank parser (after Exercises 4, 5, 6)
python main.py bank

# Test everything together
python main.py all
```

### Expected Output After All Exercises Complete

- **WhatsApp**: 50+ messages parsed, sender rankings, word cloud, hourly bars
- **Bank**: 25+ transactions, spending-per-day table, merchant rankings, monthly totals
- **Logs**: Already working — 60+ entries with error rates and user stats

---

## 💡 Key Concepts You'll Use

| Concept | Where |
|---------|-------|
| `datetime.strptime()` | Exercises 1, 4 |
| `try / except ValueError` | Exercises 1, 4 |
| `collections.Counter` | Exercises 2, 3 |
| `collections.defaultdict` | Exercises 5, 6 |
| `re.sub()` for text cleaning | Exercise 2 |
| String `.split("/")` | Exercise 5 |
| `strftime()` for grouping | Exercise 6 |
| ASCII bar charts | Exercise 3 |

---

## 📁 Project Structure

```
student_version/
├── sample_data/
│   ├── whatsapp_chat.txt     # Messy WhatsApp export (given)
│   ├── bank_statement.csv    # Messy bank CSV (given)
│   └── usage_logs.txt        # Messy usage logs (given)
├── parsers/
│   ├── whatsapp_parser.py    # ← 3 exercises here
│   ├── bank_parser.py        # ← 3 exercises here
│   └── logs_parser.py        # Fully implemented (reference)
├── utils/
│   └── cleaning.py           # Shared utilities (given)
├── main.py                   # CLI entry point (given)
└── INSTRUCTIONS.md           # ← You are here!
```

---

## ⚠️ Rules

- ❌ **No external libraries** — only `csv`, `datetime`, `re`, `collections`, `os`, `sys`
- ✅ Look for `# YOUR CODE HERE:` in the exercise functions
- ✅ Read the hints in the boxed comments carefully
- ✅ Use `logs_parser.py` as a reference — it shows the complete pattern
- ✅ Test frequently — run the parser after each exercise!

---

## 🏆 Done?

If you finish early, try these bonus challenges:

1. **Add emoji analysis** to the WhatsApp parser — which emoji is used most?
2. **Add weekend vs weekday spending** comparison to the bank parser
3. **Add a "suspicious activity" detector** — flag transactions above ₹10,000
4. **Write a 4th parser** for your own messy data file!

Good luck! 🚀
