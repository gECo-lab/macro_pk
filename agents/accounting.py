# -*- coding: utf-8 -*-
from .goods import Good, ConsumptionGood, Cash
import random

class Bookkeeper:
    """
    Represents a balance sheet for an agent in an economic simulation.

    Attributes:
        owner (an Agent): The owner of the balance sheet.
        assets (dictionary): dictionary of assets owned by the agent.
        liabilities (dictionary): dictionary of liabilities owed by the agent.
        cash_flow (dictionary): dictionary of cash flows associated with the agent.
        cash (Cash): The amount of cash owned by the agent.

    Methods:
        __init__(self, owner, assets=None, liabilities=None, cash_flow=None, cash=None): 
            Initializes a new instance of the Bookkeeper class.
        include_asset(self, asset): Includes an asset in the balance sheet.
        exclude_asset(self, asset): Excludes an asset from the balance sheet.
        include_liability(self, liability): Includes a liability in the balance sheet.
        exclude_liability(self, liability): Excludes a liability from the balance sheet.
        include_cash_flow(self, cash_flow): Includes a cash flow in the balance sheet.
        exclude_cash_flow(self, cash_flow): Excludes a cash flow from the balance sheet.
        have_money(self, quantity): Checks if the agent has enough money.
        pay(self, an_agent_balance_sheet, quantity): Pays a specified amount to another agent.
        receive(self, quantity): Receives a specified amount of money.
    """


    def __init__(self, owner, assets=None, liabilities=None, cash=None):
        self.owner = owner
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

        self.offer = None
        self.loans={}
            

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
            self.liabilitys[liability.c_name] = liability

    def exclude_liability(self, liability):
        """
        Excludes a liability from the balance sheet.

        Args:
            liability (Loan): The liability to be excluded.
        """
        if liability.c_name in self.assets:
            del self.assets[liability.c_name]
        else:
            raise ValueError("Liability not found in balance sheet.")


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
            an_agent.bookkeeper.receive(quantity)
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


    def got_good(self, a_good):
            # TODO: Este métodoo precisa de revisão
            # É ncessário lidar com ativo e passivo para os bens.

            self.include_asset(a_good)

      
    def set_offer(self, space, offer):
        self.offer = offer
        space.set_offer(self.owner, self.offer)


    def offer_accepted(self, 
                       buyer, 
                       ):
        
        buyer.bookkeeper.pay(self.owner, self.offer.ammount())
        self.offer.c_owner = buyer
        buyer.bookkeeper.got_good(self.offer)
        self.owner.release_offer(self.offer)

    def offer_partially_accepted(self, 
                                 buyer,
                                 an_offer 
                       ):
        
        buyer.bookkeeper.pay(self.owner, an_offer.ammount())
        an_offer.c_owner = buyer
        buyer.bookkeeper.got_good(an_offer)
        self.offer.c_quantity -= an_offer.c_quantity


    def get_accepted_offers(self, accepted_offers):

        first_offer = next(iter(accepted_offers.values()))
        if first_offer.c_category == "kg":
            self.add_to_capital_stock(accepted_offers)
        elif first_offer.c_category == "w":
            self.add_to_workforce(accepted_offers)
        # elif first_offer.c_category == "l":
        #     self.add_to_loans(accepted_offers)


class FirmBookkeeper(Bookkeeper):
    """Bookkeeper for the firms"""


    def __init__(self, owner, assets=None, liabilities=None, cash=None):
            super().__init__(owner, assets, liabilities, cash)

            self.workforce = {}
            self.capital_stock = {}
                

    def add_to_capital_stock(self, accepted_offers):

        last_k_eq = list(self.capital_stock.values())[-1]
        id = last_k_eq.c_id

        for k_good in accepted_offers.values():
            id = id+1
            k_good.c_id = id
            k_good.c_owner = self.owner
            self.capital_stock[id] = k_good

    def add_to_workforce(self, accepted_offers):
 
        for labor in accepted_offers.values():
            labor.c_owner = self.owner
            worker = labor.c_producer
            self.workforce[worker] = labor
            worker.is_employed()

    def lay_off(self, N_ct):
        N_ct = int(N_ct)
        for _ in range(N_ct):
            if len(self.workforce) > 0:
                worker = random.choice(list(self.workforce.keys()))
                labor = self.workforce.pop(worker)
                self.assets["labor"].c_quantity -= labor.c_quantity
                worker.is_unemployed()
        

    def lay_off_from_turnover(self, upsilon):
        lay_offs = int(len(self.workforce) * upsilon)
        lay_offs = int(lay_offs)
        for _ in range(lay_offs):
            worker = random.choice(list(self.workforce.keys()))
            labor = self.workforce.pop(worker)
            self.assets["labor"].c_quantity -= labor.c_quantity
            worker.is_unemployed()

    
    def pay_wages(self):
        # NOTE: Salários negativos ou zero e muito grandes. Checar.

        for worker, labor in self.workforce.items():
            wage = labor.ammount()
            self.pay(worker, wage)
     
    def labor_costs(self):
        """Calculate labor costs"""
        W_ct = 0
        for worker, labor in self.workforce.items():
            W_ct += labor.ammount()
            
        return W_ct
    
    def workforce_size(self):
        """Size of the workforce in the firm"""

        return len(self.workforce)

        

  
class HHBookkeeper(Bookkeeper):

    def __init__(self, owner, assets=None, liabilities=None, 
                 cash=None, consumption=None):
        super().__init__(owner, assets, liabilities, cash)

        if consumption is not None:
            if isinstance(consumption, dict):
                self.consumption = consumption
            else:
                raise ValueError("consumption must be a dictionary.")
        else:
            self.consumption = ConsumptionGood(c_name=owner.name,
                                               c_owner=self.owner)
        

    def got_good(self, a_good):

        if a_good.c_category == "l":
            self.include_liability(a_good)
        elif a_good.c_category == "cg":
            self.add_consumption_goods(a_good)
        elif a_good.c_category == "w":
            self.add_labor(a_good)
        elif a_good.c_category == "k":
            self.include_asset(a_good)
        else: 
            raise ValueError("Asset must be a Good")
    

    def add_consumption_goods(self, consumption):
        
        self.consumption.c_quantity = consumption.c_quantity
        self.consumption.c_price = (self.consumption.c_price +
                                    consumption.c_price)/2


    def create_labor_capacity(self, labor):

        if labor.c_category == "w":
            self.assets['labor'] = labor
        else:
            raise ValueError("object needs to be from Labor class")
        

    def add_labor(self, labor):

        if labor.c_name in self.assets:
            contracted_labor = self.assets[labor.c_name]
            contracted_labor.c_quantity += labor.c_quantity
            contracted_labor.c_price = (contracted_labor.c_price + labor._c_price)/2
            self.workforce[labor.c_producer] = labor


    def is_unemployed(self):

        self.assets["labor"].c_quantity = 0.0


    def calculate_income(self):

        yd_h = self.assets["labor"].ammount()

        return yd_h
