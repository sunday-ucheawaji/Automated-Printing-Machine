# The entry point of you application
from assets import art
from data import data

print(art.logo)


class AutomatedPrinter:

    def __init__(self):

        # Printer Mode
        self.mode = "ON"

        # Resources from database
        self.ink = data.resources['ink']
        self.paper = data.resources['paper']
        self.profit = data.resources['profit']

        # Format (coloured or greyscale) from database
        # Coloured
        self.price_coloured = data.FORMAT['coloured']['price']
        self.coloured_ink_unit = data.FORMAT['coloured']["materials"]['ink']
        self.coloured_paper_unit = data.FORMAT['coloured']["materials"]['paper']
        # Greyscale
        self.price_greyscale = data.FORMAT['greyscale']['price']
        self.greyscale_ink_unit = data.FORMAT['greyscale']["materials"]['ink']
        self.greyscale_paper_unit = data.FORMAT['greyscale']["materials"]['paper']

        # Currency Denomination worth or value
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
        self.biya_notes = 0
        self.faiba_notes = 0
        self.muri_notes = 0
        self.wazobia_notes = 0
        self.colour_type = ''
        self.count = 0

        # called method
        self.chained_function()

    def user_start_prompt(self):
        """ Ask the user for the operation they want to perform """
        while True:
            try:
                self.user_choice = input("""
WELCOME TO DECAGON AUTOMATED PRINTER
>> Please enter 'print' to print.
>> Please enter 'report' to generate current resource values
>> Turn off the printing machine by entering 'off'\n
""")
                if self.user_choice.lower() in ['print', 'report', 'off']:
                    return self.user_choice.lower()
                else:
                    raise Exception("Invalid option")
            except Exception as err:
                print(str(err))

    def coloured_greyscale(self):
        """ Ask the user for the print colour, coloured or greyscale """
        if self.user_choice.lower() == 'print':
            while True:
                try:
                    self.colour_type = input("coloured or greyscale? ")
                    if self.colour_type.lower() == 'coloured' or self.colour_type.lower() == 'greyscale':
                        return self.colour_type
                    else:
                        raise Exception("Invalid Colour type")
                except Exception as err:
                    print(str(err))

    def user_page_prompt(self):
        """The user enters the page number which must be a number greater than 0 """
        while True:
            try:
                print("---------------Only Numbers---------------------------")
                self.page_number = input("Please enter the number of pages\n")
                if self.page_number.isdecimal() and int(self.page_number) > 0:
                    return self.page_number
                else:
                    if not self.page_number.isdecimal():
                        raise Exception('Pages must be a number')
                    elif int(self.page_number) <= 0:
                        raise Exception("Page number must be greater than 0")
            except ValueError:
                print("Please enter a Number")
            except Exception as err:
                print(str(err))

    def maintenance(self):
        """ The user can switch off the printer"""
        if self.user_choice.lower() == 'off':
            self.mode = "off"
            exit()

    def cost_of_printing(self):
        """The cost of printing whether coloured or greyscale is determined"""
        if self.colour_type == "coloured":
            self.cost = int(self.page_number) * self.price_coloured
            print(f"Your price is #{self.cost}")
            print("------------------------------------------------------------")
            print("Please choose the currency denomination you want to pay with")
        elif self.colour_type == "greyscale":
            self.cost = int(self.page_number) * self.price_greyscale
            print(f"Your price is #{self.cost}")
            print("------------------------------------------------------------")
            print("Please choose the currency denomination you want to pay with")

    def currency_validation_errorhandling(self):
        """ The user can pay with any currency he chooses and the payment is computed"""
        while True:
            try:
                currency_choice = input(""" 
>>Enter 1 for Biya (#5)
>>Enter 2 for Faiba (#10)
>>Enter 3 for Muri (#20) 
>>Enter 4 for Wazobia (#50)
>>Enter 5 when you are Done 
""").strip()

                if currency_choice in ['1', '2', '3', '4', '5']:
                    if currency_choice == '5':
                        if self.count == 0:
                            print("You have not made payment. Please select at least one currency")
                            self.currency_validation_errorhandling()
                        else:
                            break
                    elif currency_choice == '1':
                        one = input("Enter the number of Biyar(#5) notes ")
                        self.biya_notes += int(one)
                        self.count += 1
                        self.currency_validation_errorhandling()
                    elif currency_choice == '2':
                        two = input(f"Enter the number of Faiba(#10) notes ")
                        self.faiba_notes += int(two)
                        self.count += 1
                        self.currency_validation_errorhandling()
                    elif currency_choice == '3':
                        three = input("Enter the number of Muri(#20) notes ")
                        self.muri_notes += int(three)
                        self.count += 1
                        self.currency_validation_errorhandling()
                    elif currency_choice == '4':
                        four = input("Enter the number of Wazobia(#50) notes ")
                        self.wazobia_notes += int(four)
                        self.count += 1
                        self.currency_validation_errorhandling()

                else:
                    raise Exception("Invalid option")
            except ValueError:
                print("Input must be a number")
                self.currency_validation_errorhandling()
            except Exception as err:
                print(str(err))
                self.currency_validation_errorhandling()

            self.payment = (self.biya_notes * self.biyar) + (self.faiba_notes * self.faiba) + \
                           (self.muri_notes * self.muri) + (self.wazobia_notes * self.wazobia)

            return self.payment

    def transaction(self):
        """ The cost of printing is compared with the amount paid.
        Where the amount paid is equal or greater the transaction becomes successful"""
        print('------------------------------------')
        print(f"You paid in #{self.payment}")
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
        """ The current resources available is displayed when called
        as well as the current profit"""
        report = {
            'ink': str(self.ink) + "ml",
            'paper': str(self.paper) + "pc",
            'profit': "#" + str(self.profit)
        }
        print(report)

    def resource_check(self):
        """The user demand is compared with the available resources. If
        there are available resources, the operation moves on"""
        # Coloured
        if self.colour_type.lower() == 'coloured':
            self.required_ink = int(self.page_number) * self.coloured_ink_unit
            self.required_paper = int(self.page_number) * self.coloured_paper_unit

            # The condition where both papers and ink are available
            if self.paper >= self.required_paper and self.ink >= self.required_ink:
                print("There are enough resources for this demand")
            # The condition where both papers and ink are exhausted
            elif self.paper < self.required_paper and self.ink < self.required_ink:
                print("Sorry there is not enough paper and ink")
                self.end_or_continue()
            # The condition where only paper is not enough
            elif self.paper < self.required_paper:
                print("Sorry there is not enough paper")
                self.end_or_continue()
            # The condition where only ink is not enough
            elif self.ink < self.required_ink:
                print("Sorry there is not enough ink.")
                self.end_or_continue()

        # Greyscale
        elif self.colour_type.lower() == 'greyscale':
            self.required_ink = int(self.page_number) * self.greyscale_ink_unit
            self.required_paper = int(self.page_number) * self.greyscale_paper_unit

            # The condition where both papers and ink are available
            if self.paper >= self.required_paper and self.ink >= self.required_ink:
                print("There are enough resources for this demand")
            # The condition where both papers and ink are exhausted
            elif self.paper < self.required_paper and self.ink < self.required_ink:
                print("Sorry there is not enough paper and ink")
                self.end_or_continue()
            # The condition where only paper is not enough
            elif self.paper < self.required_paper:
                print("Sorry there is not enough paper")
                self.end_or_continue()

            # The condition where only ink is not enough
            elif self.ink < self.required_ink:
                print("Sorry there is not enough ink.")
                self.end_or_continue()

    def user_project(self):
        """ The appropriate message is displayed if the operation is successful or otherwise"""
        if self.is_successful:
            print("Transaction successful!")
            print("Here is your Project and Thank you for using our services")
        else:
            print("Transaction is unsuccessful!")

    def end_or_continue(self):
        """ The user is given an option to either proceed or end the process"""
        self.biya_notes = 0
        self.faiba_notes = 0
        self.muri_notes = 0
        self.wazobia_notes = 0
        while True:
            try:
                proceed = input("Enter 'yes' to continue or 'no' to terminate process ")
                if proceed.lower() == 'yes' or proceed.lower() == 'no':
                    if proceed.lower() == 'yes':
                        return self.chained_function()
                    elif proceed.lower() == 'no':
                        return self.maintenance()
                else:
                    raise Exception("Invalid option! Enter 'yes' or 'no'")
            except Exception as err:
                print(str(err))

    def chained_function(self):
        """ This determines the order in which the functions or task would be executed"""
        self.user_start_prompt()
        if self.user_choice.lower() == "off":
            self.maintenance()
        elif self.user_choice.lower() == "report":
            self.resource_report()
            self.end_or_continue()
        elif self.user_choice.lower() == 'print':
            self.coloured_greyscale()
            self.user_page_prompt()
            self.resource_check()
            self.cost_of_printing()
            self.currency_validation_errorhandling()
            self.transaction()
            self.user_project()
            self.end_or_continue()


printer = AutomatedPrinter()
# printer = AutomatedPrinter().chained_function()

