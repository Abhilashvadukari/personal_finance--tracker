"""
app.py
Flask web application for the Personal Finance Tracker.
Run with: python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request, redirect, url_for
from models import FinanceTracker

app = Flask(__name__)
tracker = FinanceTracker()


@app.route("/")
def index():
    selected_month = request.args.get("month", FinanceTracker.current_month())

    transactions = tracker.get_transactions(month=selected_month)
    summary = tracker.get_summary(month=selected_month)
    breakdown = tracker.get_category_breakdown(month=selected_month)
    categories = tracker.get_categories()

    return render_template(
        "index.html",
        transactions=transactions,
        summary=summary,
        breakdown=breakdown,
        categories=categories,
        selected_month=selected_month,
    )


@app.route("/add", methods=["POST"])
def add_transaction():
    amount = float(request.form["amount"])
    type_ = request.form["type"]
    category_id = int(request.form["category_id"])
    txn_date = request.form["date"]
    note = request.form.get("note", "")

    tracker.add_transaction(amount, type_, category_id, txn_date, note)
    return redirect(url_for("index", month=txn_date[:7]))


@app.route("/delete/<int:txn_id>", methods=["POST"])
def delete_transaction(txn_id):
    month = request.form.get("month", FinanceTracker.current_month())
    tracker.delete_transaction(txn_id)
    return redirect(url_for("index", month=month))


if __name__ == "__main__":
    app.run(debug=True)
