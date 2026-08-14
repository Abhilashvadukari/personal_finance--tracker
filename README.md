# Personal Finance Tracker

A simple web app to track income and expenses, view monthly summaries, and
see a category-wise breakdown of spending. Built with **Python (Flask)** and
**SQLite**, with a plain **HTML/CSS** frontend.

## Features

- Add income and expense transactions with category, date, and notes
- Monthly summary: total income, total expense, and balance
- Category-wise expense breakdown with proportional bars
- Filter transactions by month
- Delete transactions
- Relational database design (categories ↔ transactions via foreign key)

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via `sqlite3`)
- **Frontend:** HTML, CSS, Jinja2 templates

## Project Structure

```
finance-tracker/
├── app.py              # Flask routes
├── models.py            # OOP data layer (FinanceTracker, Transaction, Category)
├── schema.sql            # Database schema + seed categories
├── requirements.txt
├── templates/
│   └── index.html        # Main page template
└── static/
    └── style.css          # Styling
```

## Setup & Run

1. Clone the repository and move into it:
   ```bash
   git clone https://github.com/Abhilashvadukari/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. (Optional but recommended) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser at **http://127.0.0.1:5000**

The SQLite database (`finance.db`) and default categories are created
automatically on first run.

## How It Works

- `models.py` defines a `FinanceTracker` class that wraps all SQL queries —
  adding/deleting transactions, and aggregating totals with `SUM` and
  `GROUP BY` for the summary and category breakdown.
- `app.py` exposes Flask routes that call into `FinanceTracker` and render
  `index.html` with the results.
- The frontend is a single Jinja2 template styled with plain CSS — no
  frontend framework or build step required.

## Possible Improvements

- Multi-user login/authentication
- Export monthly report as PDF/CSV
- Charts for spending trends over time
- Budget limits per category with alerts
