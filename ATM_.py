# ATM Management System
# A beginner-friendly project using Python and OOP concepts.
# Demo project only: data is stored in memory and resets when the program exits.

class Transaction:
    def __init__(self, transaction_type, amount, balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after

    def display(self):
        print(
            self.transaction_type,
            "| Amount: Rs.", self.amount,
            "| Balance after transaction: Rs.", self.balance_after
        )


class BankAccount:
    def __init__(self, name, account_number, pin, balance=1000):
        self.name = name
        self.account_number = account_number
        self.__pin = pin
        self.__balance = balance
        self.transactions = []

    def check_pin(self, entered_pin):
        return entered_pin == self.__pin

    def check_balance(self):
        print("Current balance: Rs.", self.__balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        self.__balance += amount
        transaction = Transaction("Deposit", amount, self.__balance)
        self.transactions.append(transaction)
        print("Deposit successful.")
        self.check_balance()

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > self.__balance:
            print("Insufficient balance.")
        else:
            self.__balance -= amount
            transaction = Transaction("Withdrawal", amount, self.__balance)
            self.transactions.append(transaction)
            print("Please collect your cash.")
            self.check_balance()

    def change_pin(self, current_pin, new_pin):
        if current_pin != self.__pin:
            print("Current PIN is incorrect.")
        elif len(new_pin) != 4 or not new_pin.isdigit():
            print("New PIN must contain exactly four digits.")
        else:
            self.__pin = new_pin
            print("PIN changed successfully.")


class ATM:
    def __init__(self, account):
        self.account = account

    def login(self):
        attempts = 3

        while attempts > 0:
            entered_pin = input("Enter your 4-digit PIN: ")

            if self.account.check_pin(entered_pin):
                print("Welcome,", self.account.name)
                return True

            attempts -= 1
            print("Incorrect PIN. Attempts left:", attempts)

        print("Too many incorrect attempts. Exiting.")
        return False

    def show_menu(self):
        print("\n===== ATM MENU =====")
        print("1. Check balance")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Change PIN")
        print("5. Transaction history")
        print("6. Exit")

    def show_transaction_history(self):
        if len(self.account.transactions) == 0:
            print("No transactions yet.")
        else:
            print("\n===== TRANSACTION HISTORY =====")
            for transaction in self.account.transactions:
                transaction.display()

    def run(self):
        if not self.login():
            return

        while True:
            self.show_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                self.account.check_balance()

            elif choice == "2":
                try:
                    amount = float(input("Enter deposit amount: "))
                    self.account.deposit(amount)
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "3":
                try:
                    amount = float(input("Enter withdrawal amount: "))
                    self.account.withdraw(amount)
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "4":
                current_pin = input("Enter current PIN: ")
                new_pin = input("Enter new 4-digit PIN: ")
                self.account.change_pin(current_pin, new_pin)

            elif choice == "5":
                self.show_transaction_history()

            elif choice == "6":
                print("Thank you for using the ATM.")
                break

            else:
                print("Invalid choice. Please select 1 to 6.")


def main():
    # Demo details only. Do not use real account information.
    account = BankAccount(
        name="Demo User",
        account_number="1234567890",
        pin="1234",
        balance=1000
    )

    atm = ATM(account)
    atm.run()


if __name__ == "__main__":
    main()
