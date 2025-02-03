
from .goods import CapitalGood, Cash, Loan, Labor

class BalanceSheet:
    def __init__(self, bookkeeper,  assets=None, liabilities=None, cash=None):
        """
        Initialize a BalanceSheet instance.
        Parameters:
        bookkeeper (Bookkeeper): The bookkeeper associated with this balance sheet.
        assets (dict, optional): A dictionary of assets. Defaults to None.
        liabilities (dict, optional): A dictionary of liabilities. Defaults to None.
        cash (float, optional): The initial amount of cash. Defaults to None.
        Raises:
        ValueError: If assets or liabilities are provided and are not dictionaries.
        """
        self.bk = bookkeeper
        
        self.capital_stock = {}
        self.loans = {}
        self.transactions = {}

        if assets is not None:
            if isinstance(assets, dict):
                self.assets = assets
            else:
                raise ValueError("Assets must be a dictionary.")
        else:
            self.assets = {}
        if liabilities is not None:
            if isinstance(liabilities, dict):
                self.liabilities = liabilities
            else:
                raise ValueError("Liabilities must be a dictionary.")
        else:
            self.liabilities = {}

        if cash is not None:
           my_cash = Cash(c_quantity=cash)
        else:
           my_cash = Cash(c_quantity=0.0)
        self.assets[my_cash.c_name] = my_cash


   

    ################################
    ### Assets
    ###############################

    def include_asset(self, asset):
        """
        Includes an asset in the balance sheet.

        Args:
            asset (Good): The asset to be included.

        Raises:
            ValueError: If the asset is not an instance of the Good class.
        """
        
        if asset.c_name in self.assets:
            existing_asset = self.assets[asset.c_name]
            existing_asset.c_quantity += asset.c_quantity
            existing_asset.c_price = (existing_asset.c_price + asset.c_price) / 2
        else:
            self.assets[asset.c_name] = asset

    def exclude_asset(self, asset):
        """
        Excludes an asset from the balance sheet.

        Args:
            asset (Good): The asset to be excluded.
        """
        if asset.c_name in self.assets:
            del self.assets[asset.c_name]
        else:
            raise ValueError("Asset not found in balance sheet.")


    #################################
    ### Labor
    #################################

    def add_labor(self, labor):
        """
        Add labor to the balance sheet.

        If labor already exists in the assets, update the quantity and average the price.
        If labor does not exist in the assets, create a new labor asset and include it.

        Args:
            labor (Labor): The labor asset to be added or updated.

        Returns:
            None
        """
        if "labor" in self.assets:
            my_labor = self.assets["labor"]
            my_labor.c_quantity += labor.c_quantity
            my_labor.c_price += (my_labor.c_price + labor.c_price)/2
        else:
            my_labor = Labor()
            my_labor.c_price = labor.c_price
            my_labor.c_quantity = labor.c_quantity
            self.include_asset(my_labor)


    def reduce_labor(self, labor):
        """
        Reduces the quantity of labor in the assets by the specified amount.

        Args:
            labor (object): An object representing the labor to be reduced. 
                            It should have an attribute `c_quantity` which indicates the quantity of labor.

        Modifies:
            self.assets["labor"].c_quantity: Decreases by the amount specified in `labor.c_quantity`. 
                                             If the resulting quantity is less than 0, it is set to 0.
        """
        self.assets["labor"].c_quantity -= labor.c_quantity
        if self.assets["labor"].c_quantity < 0.0:
            self.assets["labor"].c_quantity = 0.0


    def set_labor_to_zero(self):

        self.assets["labor"].c_quantity = 0.0

    def create_labor_capacity(self, labor):

        if labor.c_category == "w":
            self.assets['labor'] = labor
        else:
            raise ValueError("object needs to be from Labor class")

    def calculate_income_from_labor(self):

        yd_h = self.assets["labor"].ammount()

        return yd_h





    

    #################################
    ### Liabilities
    #################################
    
    def include_liability(self, liability):
        """
        Includes a liability in the balance sheet.

        Args:
            liability (Loan): The liability to be included.

        Raises:
            ValueError: If the liability is not an instance of the Loan class.
        """

        if liability.c_name in self.liabilities:
            existing_liability = self.liabilities[liability.c_name]
            existing_liability.c_quantity += liability.c_quantity
            existing_liability.c_price = (existing_liability.c_price + liability.c_price) / 2
        else:
            self.liabilities[liability.c_name] = liability

    def exclude_liability(self, liability):
        """
        Excludes a liability from the balance sheet.

        Args:
            liability (Loan): The liability to be excluded.
        """
        if liability.c_name in self.assets:
            del self.liabilities[liability.c_name]
        else:
            raise ValueError("Liability not found in balance sheet.")


    #################################
    ### Cash
    #################################

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


    def have_money(self, quantity):
        """
        Returns True if the agent has enough money, False otherwise.

        Args:
            quantity (float): The amount of money to check.

        Returns:
            bool: True if the agent has enough money, False otherwise.
        """
        if "cash" in self.assets:
            my_cash = self.assets["cash"].c_quantity
            return my_cash >= quantity
        else:
            raise ValueError("Cash not found in Balance Sheet")

    def pay(self, an_agent, quantity):
        """
        Pays a specified amount to another agent.

        Args:
            an_agent_balance_sheet (Bookkeeper): The balance sheet of the agent to pay.
            quantity: The amount of money to pay.

        Returns:
            bool: True if the payment was successful, False otherwise.
        """
        if self.have_money(quantity):
            self.assets["cash"].c_quantity -= quantity
            return True
        else:
            return False        

    def receive(self, quantity):
        """
        Receives a specified amount of money.

        Args:
            quantity: The amount of money to receive.
        """
        self.assets["cash"].c_quantity += quantity
        # TODO: If the agent is a firm, needs to update sales.



    #################################
    ### Loans
    #################################

    def include_loan(self, loan):
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
        
        if loan.date_contract in self.loans:
            raise NameError("This loan is already in the loans dict")
        else:
            self.loans[loan.date_contract] = loan


        if "loan" in self.liabilities:
            self.liabilities["loan"].l_quantity += loan
        else:
            self.liabilities["loan"] = Loan(l_quantity=loan)


    def exclude_loan(self, loan):
        """
        Excludes a loan from the balance sheet.
        Parameters:
        loan (Loan): The loan to be excluded. Must be an instance of the Loan class.
        Raises:
        TypeError: If the loan is not an instance of the Loan class.
        NameError: If the loan is not present in the loans dictionary.
        Updates:
        - Removes the loan from the loans dictionary using the loan's c_name as the key.
        - Updates the liabilities dictionary by subtracting the loan amount from the existing 
        "loan" liability or removing the "loan" liability if the amount becomes zero.
        """
        
        if not isinstance(loan, Loan):
            raise TypeError("loan must be an instance of the Loan class")
        
        if loan.c_name not in self.loans:
            raise NameError("This loan is not in the loans dict")
        else:
            del self.loans[loan.c_name]

        if "loan" in self.liabilities:
            self.liabilities["loan"].l_quantity -= loan.l_quantity
            if self.liabilities["loan"].l_quantity <= 0:
                self.liabilities["loan"].l_quantity = 0 ### check consistency of this


    def loan_costs(self, eta):
        """Return the total loan costs

        Returns:
            float: The sum of the loan costs by period.
        """
        Lp_ct = 0.0

        for loan in self.loans:
            Lp_ct += loan.one_term_ammount()

        return Lp_ct        


    ##############################
    ### Capital
    ##############################

    def add_equipment(self, equipment):
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

        if not isinstance(equipment, CapitalGood):
            raise TypeError("Equipment must be an instance of the CapitalGood class")
        
        if equipment.c_name in self.capital_stock:
            raise NameError("This equipment is already in the capital_stock")
        else:
            self.capital_stock[equipment.id] = equipment

        if "capital" in self.assets:
            self.assets["capital"].l_quantity += equipment
        else:
            self.assets["capital"] = CapitalGood(l_quantity=equipment)


    def last_id(self):
        """
        Retrieve the c_id of the last item in the capital_stock dictionary.

        Returns:
            int: The c_id of the last item in the capital_stock dictionary.
        """
        if self.capital_stock:
            return list(self.capital_stock.values())[-1].c_id
        else:
            return 0


    def capital_costs(self, kappa):
        """
        Calculate the total capital costs.
        This method iterates over the capital stock and calculates the total cost
        by summing the product of the quantity and price of each capital good.
        Returns:
            float: The total capital costs.
        """
        return sum(
                    (capital_good.c_quantity * capital_good.c_price) / kappa 
                     for capital_good in self.capital_stock.values()
                     ) 





 
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