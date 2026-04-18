#!/usr/bin/env python3
"""Seed realistic dummy expenses for a specific user."""

import sys
import random
from datetime import datetime, timedelta
from database.db import get_db


def parse_args(args):
    """Parse command line arguments."""
    if len(args) != 3:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    try:
        user_id = int(args[0])
        count = int(args[1])
        months = int(args[2])
        return user_id, count, months
    except ValueError:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)


def verify_user(user_id):
    """Verify user exists in database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print(f"No user found with id {user_id}.")
        sys.exit(1)

    return user


def generate_expenses(user_id, count, months):
    """Generate realistic Indian expenses."""
    # Category definitions with Indian context
    categories = {
        'Food': {'min': 50, 'max': 800, 'weight': 25, 'desc': ['Lunch at office', 'Dinner with family', 'Street food', 'Grocery shopping', 'Restaurant meal', 'Tea and snacks', 'Weekend brunch']},
        'Transport': {'min': 20, 'max': 500, 'weight': 15, 'desc': ['Auto rickshaw', 'Metro card recharge', 'Uber ride', 'Bus pass', 'Fuel', 'Taxi fare']},
        'Bills': {'min': 200, 'max': 3000, 'weight': 12, 'desc': ['Electricity bill', 'Water bill', 'Internet recharge', 'Mobile postpaid', 'Gas cylinder', 'Maintenance charges']},
        'Health': {'min': 100, 'max': 2000, 'weight': 8, 'desc': ['Doctor consultation', 'Medicines', 'Health checkup', 'Dental visit', 'Lab tests']},
        'Entertainment': {'min': 100, 'max': 1500, 'weight': 10, 'desc': ['Movie tickets', 'OTT subscription', 'Concert entry', 'Gaming', 'Park entry']},
        'Shopping': {'min': 200, 'max': 5000, 'weight': 18, 'desc': ['New clothes', 'Electronics', 'Home decor', 'Gifts', 'Festive shopping', 'Shoes']},
        'Other': {'min': 50, 'max': 1000, 'weight': 12, 'desc': ['Donation', 'Stationery', 'Pet supplies', 'Car wash', 'Salon visit']},
    }

    # Build weighted category list
    weighted_cats = []
    for cat, data in categories.items():
        weighted_cats.extend([cat] * data['weight'])

    expenses = []
    today = datetime.now()

    for _ in range(count):
        # Random date within past months
        days_back = random.randint(0, months * 30)
        expense_date = (today - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Select category by weight
        category = random.choice(weighted_cats)
        cat_data = categories[category]

        # Generate amount
        amount = round(random.uniform(cat_data['min'], cat_data['max']), 2)

        # Select description
        description = random.choice(cat_data['desc'])

        expenses.append((user_id, amount, category, expense_date, description))

    return expenses, today - timedelta(days=months * 30), today


def insert_expenses(expenses):
    """Insert all expenses in a single transaction."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('BEGIN TRANSACTION')
        cursor.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expenses
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        return False
    finally:
        conn.close()


def main():
    args = sys.argv[1:]
    user_id, count, months = parse_args(args)

    # Verify user exists
    user = verify_user(user_id)
    print(f"Found user: {user['name']} ({user['email']})")

    # Generate expenses
    expenses, start_date, end_date = generate_expenses(user_id, count, months)

    # Insert expenses
    if insert_expenses(expenses):
        print(f"\nSuccessfully inserted {count} expenses")
        print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        # Show sample of 5 records
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, amount, category, date, description FROM expenses WHERE user_id = ? ORDER BY RANDOM() LIMIT 5',
            (user_id,)
        )
        sample = cursor.fetchall()
        conn.close()

        print("\nSample records:")
        print("-" * 70)
        for row in sample:
            print(f"ID: {row['id']}, Amount: Rs. {row['amount']:.2f}, Category: {row['category']}, Date: {row['date']}, Description: {row['description']}")
    else:
        print("Failed to insert expenses.")
        sys.exit(1)


if __name__ == '__main__':
    main()
