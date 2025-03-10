class ATM:
    def __init__(self):
        self.balance = 10000

    def check_balance(self):
        print(f"Your balance is: Rs.{self.balance}")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            self.balance += amount
            print(f"Deposited Rs.{amount} successfully!")
        else:
            print("Invalid amount.")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn Rs.{amount} successfully!")
        else:
            print("Invalid amount or insufficient balance.")

    def run(self):
        while True:
            print("\nATM Menu:")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Exit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                print("Thank you!! Visit Again!!!")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    atm = ATM()
    atm.run()
