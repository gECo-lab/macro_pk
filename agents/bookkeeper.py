# -*- coding: utf-8 -*-
from .goods import ConsumptionGood, Cash
from .balance_sheet import BalanceSheet
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
        self.balance_sheet = BalanceSheet(self, assets=None, liabilities=None, cash=None)

        
        self.offer = None
        
            

    def include_asset(self, asset):
        """
        Includes an asset in the balance sheet.

        """

        self.balance_sheet.include_asset(asset)
        

    def exclude_asset(self, asset):
        """
        Excludes an asset from the balance sheet.

        Args:
            asset (Good): The asset to be excluded.
        """
        self.balance_sheet.exclude_asset(asset)
 

    def include_liability(self, liability):
        """
        Includes a liability in the balance sheet.
        """

        self.balance_sheet.include_liability(liability)


    def exclude_liability(self, liability):
        """
        Excludes a liability from the balance sheet.
        """
        self.balance_sheet.exclude_liability(liability)


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
        if self.balance_sheet.pay(an_agent, quantity):
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
        self.balance_sheet.receive(quantity)
        # TODO: If the agent is a firm, needs to update sales.


    def got_good(self, a_good):
            # TODO: Este métodoo precisa de revisão
            # É ncessário lidar com ativo e passivo para os bens.

            self.include_asset(a_good)

      
    def set_offer(self, space, offer):
        self.offer = offer
        space.set_offer(self.owner, self.offer)


    def offer_accepted(self,
                       market, 
                       buyer, 
                       ):
        
        buyer.bookkeeper.pay(self.owner, self.offer.ammount())
        self.offer.c_owner = buyer
        buyer.bookkeeper.got_good(self.offer)
        self.owner.got_contract(market, self.offer, buyer)
        self.owner.release_offer(market, self.offer)

    def offer_partially_accepted(self,
                                 market,  
                                 buyer,
                                 an_offer 
                       ):
        
        buyer.bookkeeper.pay(self.owner, an_offer.ammount())
        an_offer.c_owner = buyer
        buyer.bookkeeper.got_good(an_offer)
        self.offer.c_quantity -= an_offer.c_quantity
        self.owner.got_partial_contract(market, self.offer, buyer)




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

        id = self.balance_sheet.last_id()

        for k_good in accepted_offers.values():
            id = id+1
            k_good.c_id = id
            k_good.c_owner = self.owner
            self.balance_sheet.add_equipment(k_good)

    def add_to_workforce(self, accepted_offers):
 
        for labor in accepted_offers.values():
            labor.c_owner = self.owner
            worker = labor.c_producer
            self.workforce[worker] = labor
            self.balance_sheet.add_labor(labor)
            worker.is_employed()

    def lay_off(self, N_ct):
        N_ct = int(N_ct)
        for _ in range(N_ct):
            if len(self.workforce) > 0:
                worker = random.choice(list(self.workforce.keys()))
                labor = self.workforce.pop(worker)
                self.balance_sheet.reduce_labor(labor)
                worker.is_unemployed()
        

    def lay_off_from_turnover(self, upsilon):
        lay_offs = int(len(self.workforce) * upsilon)
        lay_offs = int(lay_offs)
        for _ in range(lay_offs):
            worker = random.choice(list(self.workforce.keys()))
            labor = self.workforce.pop(worker)
            self.balance_sheet.reduce_labor(labor)
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


class CGFirmBookkeeper(FirmBookkeeper):


    ### Here 17-01-2025
    def __init__(self, owner, assets=None, liabilities=None, 
                 cash=None, consumption=None):
        super().__init__(owner, assets, liabilities, cash)


    def add_loan(self, a_loan):

        self.balance_sheet.include_loan(a_loan)


    def loan_costs(self, eta):
        """Return the total loan cost

        Returns:
            float: The sum of the loan costs by period.
        """
        return self.balance_sheet.loan_costs(eta)


    def capital_costs(self, kappa):
        """
        Calculate the total capital costs.
     
        """
        return self.balance_sheet.capital_costs(kappa)

  
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

        self.balance_sheet.create_labor_capacity(labor)
        

    def add_labor(self, labor):

        ## Precisa revisar todo o protocolo da classe

        self.balance_sheet.add_labor(labor)
        self.owner.update_labor_quantity(labor)


    def is_unemployed(self):

        self.balance_sheet.set_labor_to_zero()


    def calculate_income(self):

        return self.balance_sheet.calculate_income_from_labor()