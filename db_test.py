from db.crud import create_user, get_users, create_transaction, get_transaction, create_category, get_category
from db.database import init_db
from datetime import date as Date

def print_users():
    users = get_users()
    if not users:
        print("No users found.")
        return

    for user in users:
        print({k: v for k, v in vars(user).items() if not k.startswith("_")})

def add_user():
    email = input("Email: ")
    firstname = input("First name: ")
    lastname = input("Last name: ")
    username = input("Username: ")
    password = input("Password: ")

    success, result = create_user(email, firstname, lastname, username, password)
    
    if success:
        print("\nUser created.")
    else:
        print(f"\nError: {result}")

def menu():
    print("\n--- BudgetBuddy DB Test ---")
    print("1. Show users")
    print("2. Add user")
    print("3. Add transaction")
    print("4. Show transactions")
    print("5. Add category")
    print("6. Show categories")
    print("0. Exit")

def add_transaction():
    user_id = input("User ID: ")
    amount = input("Amount: ")
    category_name = input("Category: ")
    date_input = input("Date (YYYY-MM-DD): ")
    date = Date.fromisoformat(date_input)
    description = input("Description (optional): ")

    create_transaction(user_id, amount, category_name, date, description or None)
    print("Transaction created.\n")

def print_transactions():
    user_id = input("User ID: ")
    transactions = get_transaction(user_id)
    if not transactions:
        print("No transactions found")
        return
    for t in transactions:
        print({k: v for k, v in vars(t).items() if not k.startswith("_")})

def add_category():
    name = input("Category name: ")
    create_category(name)
    print("Category created.\n")


def print_categories():
    categories = get_category()
    if not categories:
        print("No categories found.")
        return
    for c in categories:
        print({k: v for k, v in vars(c).items() if not k.startswith("_")})

def main():
    init_db()
    while True:
        menu()
        choice = input("Select option: ")

        if choice == "1":
            print()
            print_users()

        elif choice == "2":
            print()
            add_user()

        elif choice == "3":
            add_transaction()

        elif choice == "4":
            print_transactions()

        elif choice == "5":
            add_category()

        elif choice == "6":
            print_categories()

        elif choice == "0":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()



