"""
ATM Management System - Python OOP Mini Project
Educational console application; uses in-memory data only.
Do not use real PINs, OTPs, or bank account details.
"""

from dataclasses import dataclass, field
from datetime import datetime
import secrets
from typing import List


@dataclass
class Transaction:
    """Represents one ATM transaction."""
    transaction_type: str
    amount: float
    balance_after: float
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def display(self) -> None:
        print(f"{self.timestamp} | {self.transaction_type:<12} | "
              f"Amount: ₹{self.amount:.2f} | Balance: ₹{self.balance_after:.2f}")


class BankAccount:
    """Stores account information and implements banking operations."""

    def __init__(self, holder_name: str, account_number: str, ifsc: str,
                 pin: str, opening_balance: float = 1000.0):
        self.holder_name = holder_name
        self.__account_number = account_number
        self.ifsc = ifsc
        self.__pin = pin
        self.__balance = float(opening_balance)
        self.__transactions: List[Transaction] = []

    @property
    def account_number(self) -> str:
        """Return a masked account number."""
        return "*" * max(0, len(self.__account_number) - 4) + self.__account_number[-4:]

    @property
    def balance(self) -> float:
        return self.__balance

    def verify_pin(self, pin: str) -> bool:
        return secrets.compare_digest(self.__pin, pin)

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount % 100 != 0:
            raise ValueError("Withdrawal must be positive and in multiples of ₹100.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        self.__transactions.append(Transaction("WITHDRAWAL", amount, self.__balance))
        return True

    def deposit(self, amount: float) -> bool:
        if amount <= 0 or amount % 100 != 0:
            raise ValueError("Deposit must be positive and in multiples of ₹100.")
        self.__balance += amount
        self.__transactions.append(Transaction("DEPOSIT", amount, self.__balance))
        return True

    def change_pin(self, new_pin: str) -> None:
        if not (new_pin.isdigit() and len(new_pin) == 4):
            raise ValueError("PIN must contain exactly four digits.")
        self.__pin = new_pin

    def transaction_history(self) -> List[Transaction]:
        return list(self.__transactions)


class ATM:
    """Controls the ATM menu, authentication, and user interaction."""

    MAX_PIN_ATTEMPTS = 3

    def __init__(self, account: BankAccount):
        self.account = account
        self.card_blocked = False

    def authenticate(self) -> bool:
        attempts_left = self.MAX_PIN_ATTEMPTS
        while attempts_left > 0:
            pin = input("Enter your 4-digit ATM PIN: ").strip()
            if self.account.verify_pin(pin):
                print("\nWelcome to the ATM!")
                return True
            attempts_left -= 1
            if attempts_left:
                print(f"Incorrect PIN. Attempts remaining: {attempts_left}")
            else:
                self.card_blocked = True
                print("Too many incorrect attempts. Card blocked for this session.")
        return False

    def _generate_otp(self) -> str:
        # Demo only: in a real banking system OTP must be sent via a trusted channel.
        otp = f"{secrets.randbelow(9000) + 1000}"
        print(f"[DEMO ONLY] OTP: {otp}")
        return otp

    def _change_pin_flow(self) -> None:
        current_pin = input("Enter current PIN: ").strip()
        if not self.account.verify_pin(current_pin):
            print("Current PIN is incorrect.")
            return
        otp = self._generate_otp()
        if input("Enter the demo OTP shown above: ").strip() != otp:
            print("Invalid OTP.")
            return
        new_pin = input("Enter a new 4-digit PIN: ").strip()
        confirm_pin = input("Confirm the new PIN: ").strip()
        if new_pin != confirm_pin:
            print("PINs do not match.")
            return
        try:
            self.account.change_pin(new_pin)
            print("PIN changed successfully.")
        except ValueError as exc:
            print(f"Error: {exc}")

    def _show_history(self) -> None:
        history = self.account.transaction_history()
        if not history:
            print("No transactions recorded yet.")
            return
        print("\n--- Transaction History ---")
        for transaction in history:
            transaction.display()

    def _show_menu(self) -> None:
        print("\n========== ATM MENU ==========")
        print("1. Withdraw cash")
        print("2. Deposit cash")
        print("3. Check balance")
        print("4. Change PIN")
        print("5. Transaction history")
        print("6. Exit")
        print("==============================")

    def run(self) -> None:
        print("Welcome to the ATM Management System")
        if not self.authenticate():
            return

        while True:
            self._show_menu()
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                try:
                    amount = float(input("Enter withdrawal amount (multiples of ₹100): "))
                    self.account.withdraw(amount)
                    print(f"Please collect your cash: ₹{amount:.2f}")
                    print(f"Available balance: ₹{self.account.balance:.2f}")
                except ValueError as exc:
                    print(f"Error: {exc}")
            elif choice == "2":
                try:
                    amount = float(input("Enter deposit amount (multiples of ₹100): "))
                    self.account.deposit(amount)
                    print(f"Deposit successful. Available balance: ₹{self.account.balance:.2f}")
                except ValueError as exc:
                    print(f"Error: {exc}")
            elif choice == "3":
                print(f"Account: {self.account.account_number}")
                print(f"Available balance: ₹{self.account.balance:.2f}")
            elif choice == "4":
                self._change_pin_flow()
            elif choice == "5":
                self._show_history()
            elif choice == "6":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option. Please choose a number from 1 to 6.")


def main() -> None:
    # Demo credentials only; replace with dummy values for practice.
    account = BankAccount(
        holder_name="Demo User",
        account_number="000012345678",
        ifsc="DEMO0000001",
        pin="1234",
        opening_balance=1000.0,
    )
    atm = ATM(account)
    atm.run()


if __name__ == "__main__":
    main()
