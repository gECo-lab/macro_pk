 # -*- coding: utf-8 -*-
from examples.benchmark.agents.accounting import HHBookkeeper
from .agents import EconomicAgent
from .goods import Labor
from .equations import HHEquations
import numpy as np



class Household(EconomicAgent):
    """ Household Agents from the basic macroeconomic model 


    This module implements the Household agent

    Example:

    The agents are created by the AgentCreator class 
    in the AgentCreation module

        "agents_init": {
            "EconomicAgent": [
            {
                "var_name": "income",
                "var_type": "stochastic",
                "var_dist": "np.random.lognormal(6.0,1.0)",
                "var_value": 0.0
            }
            ]
            }

    Todo:
        * Organize equations cals
    """

    def __init__(self, simulation, model, agent_number, agent_def):
        super().__init__(simulation, model, agent_number, agent_def)
       
        self.bookkeeper = HHBookkeeper(self)
        self.eq = HHEquations(self.active_scenario)

        self.labor_mkt_name = "Labor_Market"
        self.cg_mkt_name = "CG_Market"

        self.first_step = True

   



    def step(self):
        """Household Agent Step method
        """
        if self.first_step:
            self.create_initial_values()
            self.first_step = False
        self.create_expectations()
        self.compute_reservation_wages()
        if self.unemployed:
            self.u_ht_n += 1
            self.offer_labor()
            self.receive_dole()
        self.calculate_income()
        self.demand_goods()
        self.consume()
        self.pay_taxes()


    def create_expectations(self):
        """Agent Creates Expectations
        """
        self.pe_ht_1 = self.consumption_good.c_price
        self.pe_ht = self.eq.zet(self.pe_ht,
                               self.pe_ht_1)
    

    def compute_reservation_wages(self):
        """ Workers Compute their reservation wages

        """

        self.wd_ht_1 = self.wd_ht
        self.wd_ht = self.eq.wd_ht(self.wd_ht_1, self.u_ht_n)

        return self.wd_ht


    def offer_labor(self):
        """ Worker offer labor in labor market

        # Todo: Rewrite 
        """
        self.offered_labor.c_quantity = np.random.lognormal(1.0, 0.03)
        self.offered_labor.c_price = self.compute_reservation_wages()
        self.has_offer = True
        space = self.get_a_space(self.labor_mkt_name)
        self.bookkeeper.set_offer(space, self.offered_labor)

    def receive_dole(self):
        """ Unemployed worker receive dole from government

        Todo: Rewrite
        """
    
    def calculate_income(self):

        self.income = self.bookkeeper.calculate_income()


    def demand_goods(self):
        """ Household demand goods 
        """
        self.calculate_consumer_demand()
        self.update_consumer_demand()

        ## Make good offer
        self.get_a_space(self.cg_mkt_name).set_demand(self, self.consumption_good)
                     

    def consume(self):
        """ Household consumes 
        """

        # include payment
        self.w_ht = self.income
        self.consumption_good.c_quantity = 0


  
    def create_consumer_demand(self, expected_price, demand_qnt):
        """Household creates ConsumerGood object

        Args:
            demand_qnt (number): the quantity of demand 

        Returns:
            Consumption (Good): returns a ConsumerGood object
        """

        ## Transfer to Balance Sheet?
            
        return self.bookkeeper.consumption
    

    def update_consumer_demand(self):  
        self.consumption_good.c_quantity = self.demand_qnt


    def calculate_consumer_demand(self):

        self.demand_qnt = 1 + np.random.lognormal(1.0, 0.03)
        return self.demand_qnt



    def create_labor_offer(self, labor_qnt, hourly_wage):
        """Household creates labor offer

        Args:
            labor_qnt (number): quantity of available labor
            hourly_wage (number): the minimum hourly wage

        Returns:
            Labor (Good): returns a Labor object
        """
        
        return Labor(c_quantity=labor_qnt, 
                     c_price=hourly_wage, 
                     c_owner=self, 
                     c_producer=self)
    
    def got_job(self, a_market, an_offer):

        if a_market.name == self.labor_mkt_name:
            self.unemployed = False
            self.offered_labor.c_quantity -= an_offer.c_quantity
            self.offered_labor.c_price = (self.offered_labor.c_price + an_offer.c_price)/2
            self.hourly_wage = an_offer.c_price



    def is_unemployed(self):
        self.unemployed = True
        self.bookkeeper.is_unemployed()

    def is_employed(self):
        self.unemployed = False
  
    
    def create_initial_values(self):

        ## Household Variables: NOTE: Incluidas no cenario
        ## self.demand_qnt = np.random.lognormal(1.0, 0.03)
        ### self.demand_expected_price = np.random.lognormal(1.0, 0.03)
   

        ## Create Initial consumer demand
        ## Transfer to Balance Sheet??
        self.consumption_good = self.create_consumer_demand(self.demand_expected_price,
                                                            self.demand_qnt)
        
        ## Expected prices
        ## NOTE: Incluidas no cenario
        # self.pe_ht = np.random.lognormal(1.0, 0.03)
        # self.pe_ht_1 = np.random.lognormal(1.0, 0.03)
      
        ## Create Labor Offer
        ## Transfer to Balance Sheet??
        # self.unemployed = np.random.choice([True,False], size = 1, p = [.2,.8])[0]
        ## self.labor_qnt = np.random.lognormal(1.0, 0.03)
        ## self.wd_ht =  np.random.lognormal(1.0, 0.03)


        self.offered_labor = self.create_labor_offer(self.labor_qnt, 
                                             self.wd_ht)
        self.bookkeeper.create_labor_capacity(self.offered_labor)
        if self.unemployed:
            self.is_unemployed()
        
        # time unemployed
        # self.u_ht_n = 0

        # self.unemployed = True
  
 


            




        

    



    

