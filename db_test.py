from db.crud import create_user, get_users, create_transaction, get_transaction, create_category, get_category, update_goal
from db.database import init_db
from datetime import date as Date


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


def print_users():
    users = get_users()
    if not users:
        print("\nNo users found.")

    for user in users:
        print({k: v for k, v in vars(user).items() if not k.startswith("_")})


def add_transaction():
    user_id = input("User ID: ")
    amount = input("Amount: ")
    category_name = input("Category: ")
    date_input = input("Date (YYYY-MM-DD): ")
    date = Date.fromisoformat(date_input)
    description = input("Description (optional): ")

    success, result = create_transaction(user_id, amount, category_name, date, description or None)
    if success:
        print("\nTransaction created.")
    else:
        print(f"\nError: {result}")


def print_transactions():
    user_id = input("User ID: ")
    year = input("Year: ")
    month = input("Month: ")
    transactions = get_transaction(user_id, year, month)
    if not transactions:
        print("\nNo transactions found")
    for t in transactions:
        print({k: v for k, v in vars(t).items() if not k.startswith("_")})


def add_category():
    success, result = create_category(input("Category name: "))
    if success:
        print("\nCategory created.")
    else:
        print(f"\nError: {result}")


def print_categories():
    categories = get_category()
    if not categories:
        print("\nNo categories found.")
    for c in categories:
        print({k: v for k, v in vars(c).items() if not k.startswith("_")})


def update_user_goal():
    email = input("User email: ")
    amount = input("Amount: ")
    amount = None if amount.strip() in ("", "None", "none") else int(amount)
    success, result = update_goal(email, amount)

    if success:
        print("\nGoal updated.")
    else:
        print(f"\nError: {result}")
        

def menu():
    print("\n--- BudgetBuddy DB Test ---")
    print("1. Add user")
    print("2. Show users")
    print("3. Add transaction")
    print("4. Show transactions")
    print("5. Add category")
    print("6. Show categories")
    print("7. Update user goal")
    print("0. Exit")


def main():
    init_db()
    while True:
        menu()
        choice = input("Select option: ")

        if choice == "1":
            print()
            add_user()

        elif choice == "2":
            print()
            print_users()

        elif choice == "3":
            add_transaction()

        elif choice == "4":
            print_transactions()

        elif choice == "5":
            add_category()

        elif choice == "6":
            print_categories()

        elif choice == "7":
            update_user_goal()

        elif choice == "0":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()



