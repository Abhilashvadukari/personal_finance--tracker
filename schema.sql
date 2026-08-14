-- Personal Finance Tracker Database Schema

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    category_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- Seed some default categories
INSERT OR IGNORE INTO categories (name, type) VALUES
    ('Salary', 'income'),
    ('Freelance', 'income'),
    ('Other Income', 'income'),
    ('Food', 'expense'),
    ('Rent', 'expense'),
    ('Transport', 'expense'),
    ('Utilities', 'expense'),
    ('Entertainment', 'expense'),
    ('Shopping', 'expense'),
    ('Other Expense', 'expense');
