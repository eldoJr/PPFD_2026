FILE_NAME = "finance_data.txt"


def add_entry(entry_type):
    description = input("Enter description: ").strip()

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    with open(FILE_NAME, "a") as file:
        file.write(f"{entry_type},{description},{amount}\n")

    print(f"{entry_type.capitalize()} added successfully.\n")


def calculate_summary():
    total_income = 0.0
    total_expense = 0.0

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                entry_type, _, amount = line.strip().split(",")
                amount = float(amount)

                if entry_type == "income":
                    total_income += amount
                elif entry_type == "expense":
                    total_expense += amount
    except FileNotFoundError:
        print("No data found yet.")
        return

    balance = total_income - total_expense

    print("\n------ Financial Summary ------")
    print(f"Total Income   : ₹{total_income:.2f}")
    print(f"Total Expense  : ₹{total_expense:.2f}")
    print(f"Balance        : ₹{balance:.2f}")
    print("--------------------------------\n")


def show_menu():
    print("====== Personal Finance Tracker ======")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Summary")
    print("4. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_entry("income")
        elif choice == "2":
            add_entry("expense")
        elif choice == "3":
            calculate_summary()
        elif choice == "4":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    main()