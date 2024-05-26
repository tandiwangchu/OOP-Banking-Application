import random # To create random numbers for creating our account, we use import random function.
import os # To work within the operating system(os), we use import os funtion.

class Account: # We establish a base class that is Account.
    def __init__(self, acc_no, pin, acc_purpose, balance=0): # Account number establishment
        self.acc_no = acc_no
        self.pin = pin # Putting in pin for authentication and verification.
        self.acc_purpose = acc_purpose # Stating why we want to create the account(Is it business or personal?)
        self.balance = balance # At start, our default balance will always be 0
    
    def deposit(self, cash): # Depositing money or cash to our existing balance
        self.balance += cash
        print(f"Acc credited with Nu.{cash}. Current acc balance: Nu. {self.balance}")
    
    def withdraw(self, cash):
        if cash > self.balance:
            print("Low funds.Please recharge.") # Verifying whether the withdrawable amount is within the account balanc/ Checking if we have sufficient cash.
        else:
            self.balance -= cash # Deducting our specified cash from our balance.
            print(f"Acc debited with Nu.{cash}. Current acc balance: Nu. {self.balance}")
    
    def check_balance(self):
        return self.balance # Shows us our current account balance

    def transfer(self, cash, beneficiary_acc):
        if cash > self.balance:
            print("Low funds.Please recharge.") # Verifying whether we have enough funds to send the specified money to others from our own balance account
        else:
            self.withdraw(cash) # Cashing out funds from our own account
            beneficiary_acc.deposit(cash) # Deposit cash to the beneficiary account
            print(f"Sent cash Nu. {cash} to account {beneficiary_acc.acc_no}")

    def change_acc_no(self, new_acc_no):
        self.acc_no = new_acc_no # Altering/changing our account number

    def change_pin(self, new_pin): 
        self.pin = new_pin # Account pin to be altered or changed

class BusinessAccount(Account): # Introducing a subclass for a business account
    def __init__(self, acc_no, pin, balance=0, business_name=""):
        super().__init__(acc_no, pin, "Business", balance) # Calling the parent class constructor
        self.business_name = business_name # Business name for which we created the account

class PersonalAccount(Account): # Introducing a subclass for a personal account
    def __init__(self, acc_no, pin, balance=0, user_name=""):
        super().__init__(acc_no, pin, "Personal", balance) # Calling the parent class constructor
        self.user_name = user_name # Stating name of the user for which we created the account

def save_accounts_to_file(accounts): # A file storing  all single accounts and storing information.
    with open('accounts.txt', 'w') as f:
        for acc in accounts.values():
            f.write(f"{acc.acc_no},{acc.pin},{acc.acc_purpose},Nu. {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'user_name', '')}\n") # Writing account details for the file 

def save_account(account): # Save a single account to a file
    accounts = load_accounts() # Load existing accounts
    accounts[account.acc_no] = account #  Adding or updating the acc
    save_accounts_to_file(accounts) # Save all accounts to a file

def load_accounts(): #Load all accounts from tne file
    accounts = {}
    if os.path.exists('accounts.txt'):
        with open('accounts.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                acc_no, pin, acc_purpose, balance = parts[:4]
                balance = float(balance.split()[1]) # Displaying/obtaining balance value
                if acc_purpose == "Business":
                    business_name = parts[4]
                    accounts[acc_no] = BusinessAccount(acc_no, pin, balance, business_name)
                elif acc_purpose == "Personal":
                    user_name = parts[5]
                    accounts[acc_no] = PersonalAccount(acc_no, pin, balance, user_name)
    return accounts

def create_account():
    acc_no = str(random.randint(100000000, 999999999)) # Coming up with a random 9 digit number from the existing range
    pin = str(random.randint(1000, 9999)) # Coming up/ Assigning a random pin
    acc_purpose = input("State purpose of the account (Business/Personal): ").capitalize()
    
    if acc_purpose == "Business":
        business_name = input("State name for the business: ")
        account = BusinessAccount(acc_no, pin, business_name=business_name)
    elif acc_purpose == "Personal":
        user_name = input("State owner name: ")
        account = PersonalAccount(acc_no, pin, user_name=user_name)
    else:
        print("Acc returns error!.")
        return

    save_account(account) # Saves the created accounted to file
    print(f"Account created! Your account number is {acc_no} and pin is {pin}")

def login(accounts): # Logging in to our existing account
    acc_no = input("Input your acc_no: ")
    pin = input("Input pin: ")
    
    account = accounts.get(acc_no)
    if account and account.pin == pin:
        print(f"Kuzuzangpola, {account.acc_purpose} account owner!")
        return account
    else:
        print("Invalid account number or pin.")
        return None

def delete_account(account): # Doing away with or deleting  our account
    accounts = load_accounts()
    if account.acc_no in accounts:
        del accounts[account.acc_no] # Eliminating the existing account
        save_accounts_to_file(accounts) # Saving updated accounts to file
        print("Success! Your acc has been erased.")
    else:
        print("Could not find acc.")

def change_account_details(account): # Changing either our pin or our acc no
    print("\n1. Change Account Number\n2. Change pin")
    select = input("Please select: ")
    
    if select == '1':
        new_acc_no = input("Enter new account number: ")
        accounts = load_accounts()
        if new_acc_no in accounts:
            print("Stated acc no already exists.")
        else:
            old_acc_no = account.acc_no
            account.change_acc_no(new_acc_no) # Account number changed
            save_account(account)
            del accounts[old_acc_no] # Removing previous account
            save_accounts_to_file(accounts) # Saving updated accounts to the file
            print("Success!Acc no converted to a new acc no.")
    elif select == '2':
        new_pin = input("Enter new pin: ")
        account.change_pin(new_pin) # Changing the pin for our account
        save_account(account)
        print("Success!Acc no converted to new pin.")
    else:
        print("select returns error!.")

def main(): # Implementing  main function in order  to run the bank system
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        select = input("Enter select: ")
        
        if select == '1':
            create_account() # A new account to be created
        elif select == '2':
            accounts = load_accounts() # Accounts that stored the existing loads
            account = login(accounts) # Account log in
            if account:
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout")
                    trans_select = input("Please select: ")
                    
                    if trans_select == '1':
                        cash = float(input("How much you would like to cash in: "))
                        account.deposit(cash) # Cash in our required amount to our account number
                        save_account(account) # Saving the state of the account
                    elif trans_select == '2':
                        cash = float(input("How much would you like to cash out: "))
                        account.withdraw(cash) # Cash out required amount from our balance account
                        save_account(account) # Saving the state of the account
                    elif trans_select == '3':
                        print(f"Acc_balance: Nu {account.check_balance()}") # Check your acc_balance
                    elif trans_select == '4':
                        recipient_number = input("Input recipient account number: ")
                        recipient = accounts.get(recipient_number)
                        if recipient:
                            cash = float(input("How much would you like to send: "))
                            account.transfer(cash, recipient) # Fund/cash transfer 
                            save_account(account) # Saving state of the account
                            save_account(recipient) # Saving the account state of the recipient
                        else:
                            print("Invalid! Recipient account hasn't been created.")
                    elif trans_select == '5':
                        delete_account(account) # Account being deleted or erased
                        break
                    elif trans_select == '6':
                        change_account_details(account) # Account information/details to be changed
                    elif trans_select == '7':
                        save_account(account) # Saving the state of the account
                        print("Log out successful.")
                        break
                    else:
                        print("Invalid select. Try again.")
        elif select == '3':
            break # Exiting/leaving main loop and then ending the program/algorithm
        else:
            print("Invalid select. Try again.")

if __name__ == "__main__":
    main() # Running the main function
