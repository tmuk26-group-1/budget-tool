from db.crud import create_user, get_users

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

    create_user(email, firstname, lastname, username, password)
    print("User created.\n")

def menu():
    print("\n--- BudgetBuddy DB Test ---")
    print("1. Show users")
    print("2. Add user")
    print("0. Exit")

def main():
    while True:
        menu()
        choice = input("Select option: ")

        if choice == "1":
            print()
            print_users()

        elif choice == "2":
            print()
            add_user()

        elif choice == "0":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()
