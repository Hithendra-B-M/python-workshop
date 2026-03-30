# 🎓 Messy Export Parser — Student Workshop

> **Duration**: ~30 minutes | **Difficulty**: Medium | **No external libraries needed**

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
# Run the logs parser (fully implemented)
python main.py logs

# Run the WhatsApp parser (fully implemented except word frequency)
python main.py whatsapp
```

You should see colored output with analytics. If this works, you're ready!

---

## 📋 Your Exercises (2 total)

You have **2 functions** to complete across 2 files:

| # | Exercise | File | Difficulty | Time | What You'll Learn |
|---|----------|------|-----------|------|-------------------|
| 1 | `_word_freq()` — Word frequency counter | `whatsapp_parser.py` | ⭐⭐ | 15 min | Counter, text cleaning, stop word filtering |
| 2 | `_parse_bank_date()` — Multi-format date parser | `bank_parser.py` | ⭐⭐ | 15 min | datetime.strptime, try/except, multiple formats |

---

## 🎯 Recommended Order

```
Exercise 2  →  (unlocks the entire bank parser — instant visible results!)
Exercise 1  →  (adds word frequency to WhatsApp analytics)
```

> **Start with Exercise 2** — it's simple and immediately unlocks
> ALL the bank statement analytics, giving you visible results fast!

---

## 🧪 How to Test Your Work

```bash
# Test bank parser (after Exercise 2)
python main.py bank

# Test WhatsApp word frequency (after Exercise 1)
python main.py whatsapp

# Test everything together
python main.py all
```

### Expected Output After Both Exercises Complete

- **WhatsApp**: 70+ messages, sender rankings, hourly chart, **word frequency table**, media stats
- **Bank**: 25+ transactions, spending-per-day, merchant rankings, monthly totals
- **Logs**: Already working — 60+ entries with error rates and user stats

---

## 💡 Key Concepts You'll Use

| Concept | Where |
|---------|-------|
| `collections.Counter` | Exercise 1 |
| `re.sub()` for text cleaning | Exercise 1 |
| `datetime.strptime()` | Exercise 2 |
| `try / except ValueError` | Exercise 2 |

---

## 📁 Project Structure

```
student_version/
├── sample_data/
│   ├── whatsapp_chat.txt     # Messy WhatsApp export (given)
│   ├── bank_statement.csv    # Messy bank CSV (given)
│   └── usage_logs.txt        # Messy usage logs (given)
├── parsers/
│   ├── whatsapp_parser.py    # ← 1 exercise (_word_freq)
│   ├── bank_parser.py        # ← 1 exercise (_parse_bank_date)
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

---

## 🏆 Done?

If you finish early, try these bonus challenges:

1. **Add emoji analysis** to the WhatsApp parser — which emoji is used most?
2. **Add weekend vs weekday spending** comparison to the bank parser
3. **Add a "suspicious activity" detector** — flag transactions above ₹10,000
4. **Write a 4th parser** for your own messy data file!

Good luck! 🚀
