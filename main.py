# The entry point of you application
from assets import art
from data import data
import re

print(art.logo)


class AutomatedPrinter:
    def __init__(self):

        # Printer Mode
        self.mode = "ON"

        # Resources
        self.ink = data.resources['ink']
        self.paper = data.resources['paper']
        self.profit = data.resources['profit']

        # Format (coloured or greyscale)
        # Coloured
        self.price_coloured = data.FORMAT['coloured']['price']
        self.coloured_ink_unit = data.FORMAT['coloured']["materials"]['ink']
        self.coloured_paper_unit = data.FORMAT['coloured']["materials"]['paper']
        # Greyscale
        self.price_greyscale = data.FORMAT['greyscale']['price']
        self.greyscale_ink_unit = data.FORMAT['greyscale']["materials"]['ink']
        self.greyscale_paper_unit = data.FORMAT['greyscale']["materials"]['paper']

        # Currency Denomination
        self.biyar = 5
        self.faiba = 10
        self.muri = 20
        self.wazobia = 50

        # Transaction Success
        self.is_successful = False

        # working variables
        self.page_number = 0
        self.user_choice = ''
        self.required_ink = 0
        self.required_paper = 0
        self.cost = 0
        self.payment = 0
        self.mother_function()

    def user_start_prompt(self):
        while True:
            try:
                self.user_choice = input("""
WELCOME TO DECAGON AUTOMATED PRINTER
>> What format would you like? (coloured or grayscale )
>> Please enter 'report' to generate current resource values
>> Turn off the printing machine by entering 'off'\n
""")
                if self.user_choice.lower() in ['coloured', 'grayscale', 'report', 'off']:
                    return self.user_choice.lower()
                else:
                    raise Exception("Invalid option")
            except Exception as err:
                print(str(err))

    def user_page_prompt(self):
        while True:
            try:
                self.page_number = input("Please enter the number of pages\n")
                if self.page_number.isdecimal():
                    return self.page_number
                else:
                    raise Exception('Pages must be a number')
            except Exception as err:
                print(str(err))

    def maintenance(self):
        if self.user_choice.lower() == 'off':
            self.mode= "off"
            exit()

    def cost_of_printing(self):     # Perfect
        if self.user_choice.lower() == "coloured":
            self.cost = int(self.page_number) * self.price_coloured
            print(f"Your price is #{self.cost}")
        elif self.user_choice.lower() == "greyscale":
            self.cost = int(self.page_number) * self.price_greyscale
            print(f"Your price is #{self.cost}")

    def currency_validation_errorhandling(self):
        while True:
            try:
                my_arr = []
                biyar = input("Enter the number of Biyar(#5) notes or '0' if none ")
                my_arr.append(biyar)
                faiba = input("Enter the number of Faiba(#10) notes or '0' if none ")
                my_arr.append(faiba)
                muri = input("Enter the number of Muri(#20) notes or '0' if none ")
                my_arr.append(muri)
                wazobia = input("Enter the number of Wazobia(#50) notes or '0' if none ")
                my_arr.append(wazobia)
                currency = ','.join(my_arr)
                pattern = re.compile("[\s]*[0-9]{1,}[\s]*,[\s]*[0-9]{1,}[\s]*,[\s]*[0-9]{1,}[\s]*")
                if bool(pattern.match(currency)):
                    split_list = currency.split(',')
                    arr = []
                    for digit in split_list:
                        arr.append(digit.strip())
                    return arr
                else:
                    raise Exception("Invalid input")
            except Exception as err:
                print(str(err))

    def transaction_value_error_check(self):
        while True:
            try:
                splitted_arr = self.currency_validation_errorhandling()
                self.payment = (int(splitted_arr[0]) * self.biyar) + (int(splitted_arr[1]) * self.faiba) + \
                      (int(splitted_arr[2]) * self.muri) + (int(splitted_arr[3]) * self.wazobia)
                if self.payment:
                    return self.payment
                else:
                    raise ValueError
            except ValueError:
                print("Your input for quantity of notes is invalid")

    def transaction(self):
        self.transaction_value_error_check()
        print(f"You paid in {self.payment}")
        if self.payment < self.cost:
            print("Sorry that's not enough money. Money refunded")
            self.is_successful = False

        elif self.payment > self.cost:
            change = self.payment - self.cost
            self.profit = self.profit + self.cost
            self.ink = self.ink - self.required_ink
            self.paper = self.paper - self.required_paper
            self.is_successful = True
            print(f"Here is your #{change} change")
        elif self.payment == self.cost:
            self.profit = self.profit + self.cost
            self.ink = self.ink - self.required_ink
            self.paper = self.paper - self.required_paper
            self.is_successful = True

    def resource_report(self):
        report = {
            'ink': self.ink,
            'paper': self.paper,
            'profit': self.profit
        }
        print(report)

    def resource_check(self):
        self.required_ink = int(self.page_number) * self.coloured_ink_unit
        self.required_paper = int(self.page_number) * self.coloured_paper_unit
        condition = self.paper > self.required_paper and self.ink > self.required_ink
        if condition:
            print("There are enough resources for this demand")
        else:
            if self.paper < self.required_paper and self.ink < self.required_ink:
                print("Sorry there is not enough paper and ink")
                proceed = input('Enter "quit" to end or "proceed" to make another demand?\n') # to be worked on

            elif self.paper < self.required_paper:
                print("Sorry there is not enough paper")
            elif self.ink > self.required_ink:
                print("Sorry there is not enough ink.")

    def user_project(self):
        if self.is_successful:
            print("Transaction successful!")
            print("Here is your Project and Thank you for using our services")
        else:
            print("Transaction is unsuccessful!")

    def end_or_continue(self):
        while True:
            try:
                proceed = input("Enter 'yes' to continue or 'no' to terminate process ")
                if proceed.lower() == 'yes' or proceed.lower() == 'no':
                    if proceed.lower() == 'yes':
                        return self.mother_function()
                    elif proceed.lower() == 'no':
                        return self.maintenance()
                else:
                    raise Exception("Invalid option! Enter 'yes' or 'no'")
            except Exception as err:
                print(str(err))

    def mother_function(self):
        self.user_start_prompt()
        if self.user_choice.lower() == "off":
            self.maintenance()
        elif self.user_choice.lower() == "report":
            self.resource_report()
            self.end_or_continue()
        elif self.user_choice.lower() == 'coloured' or self.user_choice.lower() == 'grayscale':
            self.user_page_prompt()
            self.resource_check()
            self.cost_of_printing()
            self.transaction()
            self.user_project()
            self.end_or_continue()


AutomatedPrinter()