"""
models.py
Core OOP classes and database access layer for the Personal Finance Tracker.
"""

import sqlite3
from dataclasses import dataclass
from datetime import date

DB_NAME = "finance.db"


@dataclass
class Category:
    id: int
    name: str
    type: str  # 'income' or 'expense'


@dataclass
class Transaction:
    id: int
    amount: float
    type: str  # 'income' or 'expense'
    category_id: int
    category_name: str
    date: str
    note: str


class FinanceTracker:
    """Handles all database operations for categories and transactions."""

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        """Create tables and seed default categories if they don't exist."""
        with self._connect() as conn:
            with open("schema.sql", "r") as f:
                conn.executescript(f.read())

    # ---------- Categories ----------

    def get_categories(self, type_filter: str = None):
        with self._connect() as conn:
            if type_filter:
                rows = conn.execute(
                    "SELECT * FROM categories WHERE type = ? ORDER BY name",
                    (type_filter,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM categories ORDER BY type, name"
                ).fetchall()
            return [Category(row["id"], row["name"], row["type"]) for row in rows]

    def add_category(self, name: str, type_: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO categories (name, type) VALUES (?, ?)", (name, type_)
            )

    # ---------- Transactions ----------

    def add_transaction(
        self, amount: float, type_: str, category_id: int, txn_date: str, note: str = ""
    ):
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO transactions (amount, type, category_id, date, note)
                   VALUES (?, ?, ?, ?, ?)""",
                (amount, type_, category_id, txn_date, note),
            )

    def delete_transaction(self, txn_id: int):
        with self._connect() as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))

    def get_transactions(self, month: str = None):
        """Return all transactions, optionally filtered by month (YYYY-MM)."""
        query = """
            SELECT t.id, t.amount, t.type, t.category_id, c.name AS category_name,
                   t.date, t.note
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
        """
        params = ()
        if month:
            query += " WHERE t.date LIKE ?"
            params = (f"{month}%",)
        query += " ORDER BY t.date DESC, t.id DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                Transaction(
                    row["id"],
                    row["amount"],
                    row["type"],
                    row["category_id"],
                    row["category_name"],
                    row["date"],
                    row["note"],
                )
                for row in rows
            ]

    # ---------- Summary / Reporting ----------

    def get_summary(self, month: str = None):
        """Return total income, total expense, and balance for a given month (or all time)."""
        query = "SELECT type, SUM(amount) as total FROM transactions"
        params = ()
        if month:
            query += " WHERE date LIKE ?"
            params = (f"{month}%",)
        query += " GROUP BY type"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        totals = {"income": 0.0, "expense": 0.0}
        for row in rows:
            totals[row["type"]] = row["total"] or 0.0

        return {
            "income": totals["income"],
            "expense": totals["expense"],
            "balance": totals["income"] - totals["expense"],
        }

    def get_category_breakdown(self, month: str = None):
        """Return expense totals grouped by category for a given month (or all time)."""
        query = """
            SELECT c.name AS category_name, SUM(t.amount) AS total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type = 'expense'
        """
        params = ()
        if month:
            query += " AND t.date LIKE ?"
            params = (f"{month}%",)
        query += " GROUP BY c.name ORDER BY total DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [{"category": row["category_name"], "total": row["total"]} for row in rows]

    @staticmethod
    def current_month():
        return date.today().strftime("%Y-%m")
