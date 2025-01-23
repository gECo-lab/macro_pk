
from .goods import CapitalGood, Cash, Loan

class BalanceSheet:
    def __init__(self, bookkeeper):
        self.bk = bookkeeper
        self.assets = {}
        self.liabilities = {}
        self.capital_stock = {}
        self.loans = {}
        self.transactions = {}


    def add_cash(self, cash):
        """
        Add cash to the balance sheet.

        Parameters:
        cash (Cash): The cash amount to be added. Must be an instance of the Cash class.

        Raises:
        TypeError: If the provided cash is not an instance of the Cash class.

        Updates:
        If "cash" is already in assets, increments the c_quantity of the existing Cash instance.
        Otherwise, creates a new Cash instance with the provided cash amount and adds it to assets.
        """

        if not isinstance(cash, Cash):
            raise TypeError("cash must be an instance of the Cash class")

        if "cash" in self.assets:
            self.assets["cash"].c_quantity += cash
        else:
            self.assets["cash"] = Cash(c_quantity=cash)


    def add_loan(self, loan):
        """
        Adds a loan to the balance sheet.
        Parameters:
        loan (Loan): The loan to be added. Must be an instance of the Loan class.
        Raises:
        TypeError: If the loan is not an instance of the Loan class.
        NameError: If the loan is already present in the loans dictionary.
        Updates:
        - Adds the loan to the loans dictionary using the loan's c_name as the key.
        - Updates the liabilities dictionary by adding the loan amount to the existing 
        "loan" liability or creating a new "loan" liability if it does not exist.
        """


        if not isinstance(loan, Loan):
            raise TypeError("loan must be an instance of the Loan class")
        
        if loan.c_name in self.loans:
            raise NameError("This loan is already in the loans dict")
        else:
            self.loans[loan.c_name] = loan

        if "loan" in self.liabilities:
            self.liabilities["loan"].l_quantity += loan
        else:
            self.liabilities["loan"] = Loan(l_quantity=loan)

    def add_equipment(self, capital):
        """
        Adds a piece of equipment to the balance sheet.
        Parameters:
        capital (CapitalGood): The equipment to be added, which must be
        an instance of the CapitalGood class.
        Raises:
        TypeError: If the provided capital is not an instance of the CapitalGood class.
        NameError: If the equipment is already present in the capital_stock.
        Updates:
        - Adds the equipment to the capital_stock dictionary using the equipment's name as the key.
        - Updates the liabilities under "capital" by increasing the quantity if a loan exists in assets,
          otherwise, it creates a new CapitalGood entry in liabilities with the provided capital.
        """

        if not isinstance(capital, CapitalGood):
            raise TypeError("Equipment must be an instance of the CapitalGood class")
        
        if capital.c_name in self.capital_stock:
            raise NameError("This equipment is already in the capital_stock")
        else:
            self.capital_stock[capital.c_name] = capital

        if "loan" in self.assets:
            self.liabilities["capital"].l_quantity += capital
        else:
            self.liabilities["capital"] = CapitalGood(l_quantity=capital)
        

 
###### GPT generated

    def add_asset(self, name, value):
        self.assets[name] = value

    def add_liability(self, name, value):
        self.liabilities[name] = value

    def add_capital_stock(self, name, value):
        self.capital_stock[name] = value

    def generate_report(self):
        report = "Balance Sheet Report\n"
        report += "====================\n\n"
        
        report += "Assets:\n"
        for name, value in self.assets.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        report += "Liabilities:\n"
        for name, value in self.liabilities.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        report += "Capital Stock:\n"
        for name, value in self.capital_stock.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        total_assets = sum(self.assets.values())
        total_liabilities = sum(self.liabilities.values())
        total_capital_stock = sum(self.capital_stock.values())
        
        report += f"Total Assets: ${total_assets}\n"
        report += f"Total Liabilities: ${total_liabilities}\n"
        report += f"Total Capital Stock: ${total_capital_stock}\n"
        report += f"Net Worth: ${total_assets - total_liabilities}\n"

        return report

# Example usage:
# balance_sheet = BalanceSheet()
# balance_sheet.add_asset("Cash", 10000)
# balance_sheet.add_liability("Loan", 5000)
# balance_sheet.add_capital_stock("Common Stock", 2000)
# print(balance_sheet.generate_report())