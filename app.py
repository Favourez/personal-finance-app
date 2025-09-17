from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime, date
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            color TEXT DEFAULT '#3498db'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            category_id INTEGER,
            amount REAL NOT NULL,
            description TEXT,
            type TEXT NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            amount REAL NOT NULL,
            period TEXT DEFAULT 'monthly',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # Insert default categories if they don't exist
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ('Food & Dining', 'expense', '#e74c3c'),
            ('Transportation', 'expense', '#f39c12'),
            ('Shopping', 'expense', '#9b59b6'),
            ('Entertainment', 'expense', '#e67e22'),
            ('Bills & Utilities', 'expense', '#34495e'),
            ('Healthcare', 'expense', '#1abc9c'),
            ('Salary', 'income', '#27ae60'),
            ('Freelance', 'income', '#2ecc71'),
            ('Savings', 'savings', '#3498db'),
            ('Investment', 'investment', '#8e44ad')
        ]
        cursor.executemany('INSERT INTO categories (name, type, color) VALUES (?, ?, ?)', default_categories)
    
    # Insert default accounts if they don't exist
    cursor.execute('SELECT COUNT(*) FROM accounts')
    if cursor.fetchone()[0] == 0:
        default_accounts = [
            ('Main Bank Account', 'bank', 0.0),
            ('Mobile Money', 'momo', 0.0),
            ('Cash', 'cash', 0.0)
        ]
        cursor.executemany('INSERT INTO accounts (name, type, balance) VALUES (?, ?, ?)', default_accounts)
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

# API Routes
@app.route('/api/dashboard-data')
def get_dashboard_data():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Get total balance
    cursor.execute('SELECT SUM(balance) FROM accounts')
    total_balance = cursor.fetchone()[0] or 0
    
    # Get recent transactions
    cursor.execute('''
        SELECT t.id, t.amount, t.description, t.type, t.date, c.name as category, a.name as account
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN accounts a ON t.account_id = a.id
        ORDER BY t.created_at DESC
        LIMIT 5
    ''')
    recent_transactions = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    
    # Get monthly spending by category
    cursor.execute('''
        SELECT c.name, SUM(t.amount) as total, c.color
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.type = 'expense' AND strftime('%Y-%m', t.date) = strftime('%Y-%m', 'now')
        GROUP BY c.id, c.name, c.color
        ORDER BY total DESC
    ''')
    monthly_spending = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'monthly_spending': monthly_spending
    })

@app.route('/api/accounts')
def get_accounts():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts ORDER BY name')
    accounts = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(accounts)

@app.route('/api/categories')
def get_categories():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY type, name')
    categories = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(categories)

@app.route('/api/transactions', methods=['GET', 'POST'])
def handle_transactions():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO transactions (account_id, category_id, amount, description, type, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['account_id'], data['category_id'], data['amount'], 
              data['description'], data['type'], data['date']))
        
        # Update account balance
        if data['type'] == 'expense':
            cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', 
                         (data['amount'], data['account_id']))
        else:
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', 
                         (data['amount'], data['account_id']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    else:
        cursor.execute('''
            SELECT t.*, c.name as category_name, c.color, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            ORDER BY t.date DESC, t.created_at DESC
        ''')
        transactions = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        conn.close()
        return jsonify(transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
