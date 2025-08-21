import json
from datetime import datetime


# Data Structure

transactions = []  # Each item: {"date": str, "type": str, "amount": float, "category": str}


# Save & Load


def save_data():
    with open("transactions.json", "w") as f:
        json.dump(transactions, f, indent=4)

def load_data():
    global transactions
    try:
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
    except FileNotFoundError:
        transactions = []


# Core Functions


def add_transaction():
    t_type = input("Enter type (income/expense): ").lower()
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    transactions.append({
        "date": date,
        "type": t_type,
        "amount": amount,
        "category": category
    })
    print("Transaction added!")


def view_transactions():
    if not transactions:
        print("No transactions recorded.")
        return
    for i, t in enumerate(transactions, 1):
        print(f"{i}. {t['date']} | {t['type'].title()} | ${t['amount']} | {t['category']}")


def sort_transactions():
    key = input("Sort by (date/amount/type/category): ").lower()
    sorted_data = sorted(transactions, key=lambda x: x[key])
    for t in sorted_data:
        print(f"{t['date']} | {t['type'].title()} | ${t['amount']} | {t['category']}")


def search_transactions():
    keyword = input("Enter keyword to search (type/category/date): ").lower()
    results = [t for t in transactions if keyword in str(t.values()).lower()]
    if results:
        for t in results:
            print(f"{t['date']} | {t['type']} | ${t['amount']} | {t['category']}")
    else:
        print("No results found.")


def filter_expenses_over():
    threshold = float(input("Show expenses over amount: "))
    results = [t for t in transactions if t["type"] == "expense" and t["amount"] > threshold]
    if results:
        for t in results:
            print(f"{t['date']} | {t['type']} | ${t['amount']} | {t['category']}")
    else:
        print("No expenses above threshold.")

# ============================
# Bonus: ASCII Bar Chart
# ============================

def monthly_spending_chart():
    monthly = {}
    for t in transactions:
        if t["type"] == "expense":
            month = t["date"][:7]  # YYYY-MM
            monthly[month] = monthly.get(month, 0) + t["amount"]

    if not monthly:
        print("No expenses recorded.")
        return

    print("\nMonthly Spending Chart:")
    for month, total in monthly.items():
        bars = "#" * (int(total) // 10)  # 1 bar per $10
        print(f"{month}: ${total:.2f} | {bars}")


# Main Menu


def main():
    load_data()
    while True:
        print("\n==== Personal Finance Tracker ====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Sort Transactions")
        print("4. Search Transactions")
        print("5. Filter Expenses Over X")
        print("6. Show Monthly Spending Chart")
        print("7. Save & Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            sort_transactions()
        elif choice == "4":
            search_transactions()
        elif choice == "5":
            filter_expenses_over()
        elif choice == "6":
            monthly_spending_chart()
        elif choice == "7":
            save_data()
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
