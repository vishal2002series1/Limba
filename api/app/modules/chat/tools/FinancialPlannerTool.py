# Imports
import json
import math
from datetime import datetime

import numpy as np
from scipy.stats import norm
from typing import Optional, Type
from langchain.agents import Tool, load_tools
from langchain.pydantic_v1 import BaseModel
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.callbacks import get_openai_callback  
######## Deprecated Modules ###########
from langchain.chains import LLMChain
from langchain.agents.chat.base import ChatAgent
########################################
from langchain.prompts import PromptTemplate

from ..prompt_templates.financial_planner_prompt_templates import (
    SYSTEM_MESSAGE_PREFIX, SYSTEM_MESSAGE_SUFFIX,
    HUMAN_MESSAGE,  
    SYSTEM_MESSAGE_PREFIX_CHAT_AGENT, SYSTEM_MESSAGE_SUFFIX_CHAT_AGENT, 
    solution_plan_template, scenario_template, financial_planner_template, 
    )
from ..schema import RetirementSimulationInput, MonthlyPaymentCalculatorInput, LoanAmountCalculatorInput, LoanTermCalculatorInput, FinancialPlannerInput, ClientDataReaderInput
from app.irah.connections import financial_planner_llm, math_llm
from app.irah.connections import bing_search
from app.irah.logs import logger
from app.modules.chat.agents import irah_chat_agent

# Client data reader tool
class ClientDataReaderTool(BaseTool):
    name = "ClientDataReaderTool"
    description = ("Useful for getting client financial data. The input is the client name: first name and last name. For example, 'Jane Smith'.\n"
                   "The output data includes information about clients portfolio, trust fund accounts, retirement accounts, age, retirement monetary goal, "
                   "time frame, deposit rate, total savings, return rate, savings, savings growth, volatility, property details, and location.\n"
                   "This information can be used to model financial outcomes and make better financial planning decisions.")
    args_schema: Type[BaseModel] = ClientDataReaderInput

    def _run(self, client_name: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Use the tool by inputting the client name.
        """
        try:
            # Load data
            with open('app/store/metadata/financial_planner_user_profile.json', 'r') as f:
                all_clients = json.load(f)
            
            # Clean / strip input and get data
            client_name = str(client_name.strip())
            client_data = [client for client in all_clients if client['client_data']['name']==client_name][0]

            # Calculate initial annual savings from retirement accounts
            annual_savings = sum(account['contribution'] for account in client_data['client_data']['retirement_accounts'])

            # Calculate annual savings growth as average of growth rates in retirement accounts
            annual_savings_growth = sum(account['annual_growth'] for account in client_data['client_data']['retirement_accounts']) / len(client_data['client_data']['retirement_accounts'])

            # Get output data: all the underlying data and intermediate data calculations
            output_data = json.dumps({
                'client_data': client_data['client_data'],
                'annual_savings': annual_savings,
                'annual_savings_growth': annual_savings_growth
            })

            return f"{output_data}"
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error in ClientDataReaderTool run: {e}")
            raise ValueError(f"Error in ClientDataReaderTool run: {e}")


# Bing search tool
search_tool = Tool(
    name = "Search",
    func = bing_search.run,
    description = "A search engine. Useful for when you need to answer questions about current events. Input should be a search query."
    )


# Retirement simulation tool
def safe_exp(x):
    """
    Arg(s):
        x: float = integer or float value

    Output:
        Returns exponential value of the input argument or the integer value if it's greater than 700
    """
    if x > 700:  #number 700 is used because math.exp(710) is too large for python, causes error
        return x
    else:
        return math.exp(x)

class RetirementSimulationTool(BaseTool):
    name = "RetirementSimulationTool"
    description = ("Useful for simulating retirement savings and expenses by calculating the likelihood of achieving the specified retirement monetary goal at the specified retirement age goal. "
                   "It also calculates the most likely age of retirement."
                   "To use the tool, you must provide the following input parameters:\n"
                   "['current_age', 'retirement_age_goal', 'total_savings', 'annual_savings', 'annual_savings_growth_rate'].\n"
                   "The following parameters below are optional, if you don't know the value, don't make up a number:\n"
                   "['retirement_monetary_goal', 'cost_of_living', 'return_rate', 'volatility'].")
    args_schema: Type[BaseModel] = RetirementSimulationInput

    def _run(self, current_age: int, retirement_age_goal: int, total_savings: float, annual_savings: float, 
             annual_savings_growth_rate: float, cost_of_living: Optional[float] = None, retirement_monetary_goal: Optional[float] = None, 
             return_rate: Optional[float] = None, volatility: Optional[float] = None, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Use the tool.The output is a string containing all the assumptions made and likelihood of retiring at the desired age.
        """
        try:
            # Check if total savings or annual savings is less than 0
            if (total_savings < 0) or (annual_savings < 0):
                output_message = f"The client can't afford to retire at the specified age because of a negative savings balance. {total_savings = } and {annual_savings = }"
                return output_message
            
            # Set up schema
            self.args_schema = RetirementSimulationInput(current_age = current_age, retirement_age_goal = retirement_age_goal, total_savings = total_savings, 
                                                        annual_savings = annual_savings, annual_savings_growth_rate = annual_savings_growth_rate)

            # Assumptions
            max_age = 95
            yes_vol = True
            sims = 50

            # Set default parameters if none given
            ## Cost of living
            if cost_of_living is None:
                cost_of_living = self.args_schema.cost_of_living
            ## Retirement monetary goal
            if not retirement_monetary_goal:
                retirement_monetary_goal = float(cost_of_living * 12.0 * (max_age - retirement_age_goal))
            # Return rate
            if return_rate is None:
                return_rate = self.args_schema.return_rate
            # Volatility
            if volatility is None:
                volatility = self.args_schema.volatility

            # Get annual cost of living
            annual_COL = cost_of_living * 12

            # Create counters / storage container
            achieved_goal_sims = 0
            achieved_age_goal_sims = 0
            achieved_goal_age = []

            # Initialize savings percentiles as a dictionary where the keys are ages
            savings_at_age = {age: [] for age in range(current_age, max_age)}

            for s in range(sims):
                savings = total_savings
                current_annual_savings = annual_savings
                goal_achieved_in_sim = False

                for age in range(current_age, max_age):
                    if yes_vol:
                        np.random.seed(97)
                        Z = norm.ppf(np.random.uniform(0, 1))
                    else:
                        Z = 0
                    current_annual_savings = current_annual_savings * (1 + annual_savings_growth_rate)
                    savings = savings * safe_exp(return_rate + volatility * Z) + current_annual_savings

                    # Save the savings amount for this age in this simulation
                    savings_at_age[age].append(savings)

                    if savings >= retirement_monetary_goal and not goal_achieved_in_sim:
                        achieved_goal_sims += 1
                        achieved_goal_age.append(age)
                        goal_achieved_in_sim = True
                        if age <= retirement_age_goal:
                            achieved_age_goal_sims += 1

                    if goal_achieved_in_sim:
                        savings = savings * safe_exp(return_rate + volatility * Z) - annual_COL

            likelihood_of_achieving_age_goal = achieved_age_goal_sims / sims
            most_likely_age_of_achieving_goal = max(set(achieved_goal_age), key = achieved_goal_age.count)

            # Define output as a string
            output_string = (f"Assuming a {annual_savings_growth_rate:.2%} annual savings growth, "
                            f"a {return_rate:.2%} rate of return on investments after retirement, "
                            f"market volatility of {volatility:.2%}, and "
                            f"a monthly retirement cost of living of ${cost_of_living:,.2f} for {max_age - retirement_age_goal} years after retirement: "
                            f"the likelihood of the client retiring by {retirement_age_goal} years old is {likelihood_of_achieving_age_goal:.2%}.\n" 
                            f"Given the assumptions, the most likely age for the client to retire with a calculated retirement monetary goal of ${retirement_monetary_goal:,.2f} "
                            f"is at the age of {most_likely_age_of_achieving_goal}.")

            return output_string
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error in LoanAmountCalculatorTool run: {e}")
            raise ValueError(f"Error in RetirmentSimulatorTool run: {e}")


# Create loan tools
## Monthly Payment Calculator 
class MonthlyPaymentCalculatorTool(BaseTool):
    name = "MonthlyPaymentTool"
    description = ("Useful for calculating monthly payments on loans. Use this tool for mortgage loans, student loans, auto loans and any general loans.\n"
                   "To use the tool, you must provide the following input: "
                   "['price', 'interest_rate', 'loan_term'].\nThe parameter: ['down_payment'] is OPTIONAL, if you don't know the value, don't make up a number. If you know the value, use it."
                   "\nUse the descriptions below as a guide for identifying the input parameters:\n"
                   "price = The price of the item (home, car, tuition) to get a loan for. It should be a float value.\n"
                   "interest_rate = The interest rate for the loan to calculate a monthly payment for. It should be a float representation of a percentage value, for example 0.06. "
                   "Unless otherwise specified, search the internet for current interest rates.\n"
                   "loan_term = Number of years for the loan. It should be an integer.\n"
                   "down_payment = Down payment amount on the price. It should be a dollar amount represented as a float. This is optional and should only be provided if you know the value.")
    args_schema: Type[BaseModel] = MonthlyPaymentCalculatorInput

    def _run(self, price: float, interest_rate: float, loan_term: int, down_payment: Optional[float] = None):
        """
        Use the tool. This method is used to calculate the monthly payment for a given loan price.

        Arg(s):
            price: float = price of the loan item / purpose (home, car, education, personal, etc.)
            interest_rate: float = interest rate for the loan
            loan_term: int = number of years for the loan
            down_payment: float = down payment amount on the loan

        Output:
            a dictionary or string containing the input arguments and the calculated monthly payment.
        """
        try:
            # Get down payment amount. Default will be 20% of the home value.
            if down_payment is None:
                down_payment = 0.20 * price

            # Get down payment percentage
            percent_down_payment = down_payment / price

            # Get loan amount, monthly interest rate (r), and number of payments (n) in months
            loan_amount = price - down_payment
            r = interest_rate / 12
            n = loan_term * 12

            # Calculate monthly payment and get output dictionary
            monthly_payment = (loan_amount * r * (1 + r) ** n) / (((1 + r) ** n) - 1)
            output_dict = {"price": price, "interest_rate": interest_rate, "loan_term": loan_term, "down_payment": down_payment, 
                        "percent_down_payment": percent_down_payment, "loan_amount": loan_amount, "monthly_payment": monthly_payment}
            output_string = (f"Price: {price:,.2f}. Interest Rate: {interest_rate:.2%}. Loan Term: {loan_term:,.2f}. Down Payment: {down_payment:,.2f}. "
                            f"Down Payment Percentage: {percent_down_payment:.2%}. Loan Amount: {loan_amount:,.2f}. Monthly Payment: {monthly_payment:,.2f}")
            
            return output_string
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error in MonthlyPaymentCalculatorTool run: {e}")
            raise ValueError(f"Error in MonthlyPaymentCalculatorTool run: {e}")

# Loan Amount Tool
class LoanAmountCalculatorTool(BaseTool):
    name = "LoanAmountTool"
    description = ("Useful for calculating loan amounts when the expected monthly payment is known. Use this tool for mortgage loans, student loans, auto loans and any general loans.\n"
                   "To use the tool, you must provide the following input: "
                   "['monthly_payment', 'interest_rate', 'loan_term'].\nThe parameter: ['down_payment'] is OPTIONAL, if you don't know the value, don't make up a number. If you know the value, use it.\n"
                   "Use the descriptions below as a guide for identifying the input parameters:\n"
                   "monthly_payment = The expected monthly payment for the loan amount to be calculated.\n"
                   "interest_rate = The interest rate for the loan to calculate a monthly payment for. Unless otherwise specified, search the internet for the current interest rates.\n"
                   "loan_term = Number of years for the loan. It should be an integer.\n"
                   "down_payment = Down payment amount on the price. This is optional and should only be provided if you know the value.")
    args_schema: Type[BaseModel] = LoanAmountCalculatorInput

    def _run(self, monthly_payment: float, interest_rate: float, loan_term: int, down_payment: Optional[float] = None):
        """
        This method is used to calculate the loan amount and price of an item.

        Arg(s):
            monthly_payment: float = expected monthly payment on item to be purchased 
            interest_rate: float = interest rate for the loan
            loan_term: int = number of years for the loan
            down_payment: float = down payment amount on the loan

        Output:
            a dictionary or string containing the calculated price, loan amount and down payment.
        """
        try:
            # Get monthly interest rate (r), and number of payments (n) in months
            r = interest_rate / 12
            n = loan_term * 12

            # Calculate loan amount
            loan_amount = (monthly_payment * (((1 + r) ** n) - 1)) / (r * (1 + r) ** n)

            # Calculate item price. If no down payment is given, assume 20%
            if down_payment is None:
                price = loan_amount / 0.8
                down_payment = 0.2 * price
            # If a down payment is entered, price is loan amount + down payment
            else:
                price = loan_amount + down_payment
            
            # Get output as dictionary
            output_dict = {"price": price, "loan_amount": loan_amount, "down_payment": down_payment}
            output_string = f"Price: {price:,.2f}. Loan Amount: {loan_amount:,.2f}. Down Payment: {down_payment:,.2f}"

            return output_string
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error in LoanAmountCalculatorTool run: {e}")
            raise Exception("FinancialPlannerTool - Error in LoanAmountCalculatoe Tool")

# Loan Term Tool
class LoanTermCalculatorTool(BaseTool):
    name = "LoanTermTool"
    description = ("Useful for calculating loan terms to help understand loan repayments. Use this tool if you want to find out a new loan term / duration for a loan when a client wants to make "
                   "additional monthly payments and/or make a lump sum on a loan.\n"
                   "To use the tool, you must provide the following input: "
                   "['expected_monthly_payment', 'expected_loan_balance', 'current_interest_rate'].\n"
                   "If a client wants to make additional payments to their original monthly payment, the expected monthly payment will be the original payment plus the additional payment. "
                   "For example if a client's current monthly payment is $3000 and they want to make an additional monthly payment of $200, the expected monthly payment will be 3200.\n"
                   "If a client wants to make a lump sum payment to their current loan, this expected loan balance will be the current loan minus the lump sum. For example "
                   "if a client's current loan balance is $300,000 and they want to make a lump sum payment of $50,000, the expected_loan_balance will be 250000 which is 300000-50000.\n")
    args_schema: Type[BaseModel] = LoanTermCalculatorInput

    def _run(self, expected_monthly_payment: float, expected_loan_balance: float, current_interest_rate: float):
        """
        Use the tool.
        """
        try:
            # Get monthly interest rate (r) and other variables
            r = current_interest_rate / 12
            m = expected_monthly_payment
            p = expected_loan_balance

            # Get new loan term in months
            ## Account for domain of log (no negative numbers)
            if (domain := (m - (p * r))) <= 0:
                return f"Monthly payment of ${m:,.2f} is insufficient for paying off a loan of ${p:,.2f} at an interest rate of {current_interest_rate:.2%} over any period of time."
            else:
                loan_term = math.log(m / domain, 1 + r)

            # Calulate loan term in years / months and get output dictionary
            years, months = divmod(round(loan_term), 12)
            output_dict = {"new_loan_term_in_months": round(loan_term), "new_loan_term_string": f"{years} years and {months} months."}
            output_string = f"New loan term in months: {round(loan_term)}. New loan term in years and months: {years} years and {months} months."

            return output_string
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error in LoanTermCalculatorTool run: {e}")
            raise Exception("FinancialPlannerTool - Error in LoanTermCalculatoe Tool")


# Create a solution plan for the agent
def create_plan(scenario, tools, planning_template: str = solution_plan_template, scenario_template: str = scenario_template):
        """
        This function is used to create a solution plan of action for the main financial planner agent.
        """
        try:
            # Create templates (system and human) and chat prompt
            system_message_prompt = SystemMessagePromptTemplate.from_template(planning_template)
            human_message_prompt = HumanMessagePromptTemplate.from_template(scenario_template)
            chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

            # Get tool name and description as a string and create chat message
            tool_strings = "\n- ".join([f"{tool.name}: {tool.description}" for tool in tools])
            chat_msgs = chat_prompt.format_prompt(scenario=scenario, tool_list=tool_strings).to_messages()

            return chat_msgs
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTools - Error in create Plan: {e}")
            raise Exception("FinancialPlannerTool - Error in Create Plan")


# Define planner tools
## Set calculator LLM description, get tool and edit description
calculator_description_suffix = "The input should be a fully formed instruction on the calculation to execute."
planner_tools = load_tools(["llm-math"], llm = math_llm)
calculator_tool = planner_tools[0]
calculator_tool.description = f"{calculator_tool.description} {calculator_description_suffix}"

## Set financial planner tools
planner_tools = [ClientDataReaderTool(), RetirementSimulationTool(), MonthlyPaymentCalculatorTool(), 
                 LoanAmountCalculatorTool(), LoanTermCalculatorTool(), calculator_tool, search_tool]

## Create Financial Planner tool
class FinancialPlannerTool(BaseTool):
    name = "FinancialPlannerTool"
    description = ("""if client name is not available in input then do not use this tool. Useful for advising clients on their financial goals (retirement, mortgages, loans, etc).
                   When a question related to financial planning, retirement, mortgages, or loans is asked, use this tool first.
                   To use the tool, you must provide a fully formed question that contains a client's name.
                   Example question:
                    1. Jane Smith's son was just accepted to Yale and she wants to support him. What are the all included costs for 4 years and how will that affect her financial goals? Will she need to get a loan to retire in time?
                    """)
    args_schema= FinancialPlannerInput

    def _run(self, scenario: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        """
        Use the tool. The output is a dictionary containing the response and generated solution plan.
        """
        try:
            logger.info(f"[{datetime.now()}]  FinancialPlannerTool - Planner initiated")
            # Check client name
            self.args_schema = FinancialPlannerInput()
            # if not client_name:
            #     client_name = self.args_schema.client_name
            
            # Create prompt, chain and financial planner agent
            prompt = ChatAgent.create_prompt(
                planner_tools,
                system_message_prefix = SYSTEM_MESSAGE_PREFIX,
                system_message_suffix = SYSTEM_MESSAGE_SUFFIX,
                human_message = HUMAN_MESSAGE,
                input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
                )
            llm_chain = LLMChain(llm = financial_planner_llm, prompt = prompt)
            agent = ChatAgent(llm_chain = llm_chain, tools = planner_tools)
            planner_agent = AgentExecutor(agent = agent, tools = planner_tools, verbose = True, 
                                        return_intermediate_steps = True, handle_parsing_errors = True, debug = True, return_source_documents = True)
            # prompt = PromptTemplate(
            #             input_variables = ["input", "agent_scratchpad", "tools", "tool_names", "client_name"],
            #             template = financial_planner_template
            #             )
            # agent = create_openai_functions_agent(llm = financial_planner_llm, tools=planner_tools, prompt=prompt)
            # planner_agent = AgentExecutor(agent=agent, tools=planner_tools, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True, debug=True, return_source_documents=True)

            # Create solution plan
            solution_plan = create_plan(scenario, planner_tools)
            solution_plan = financial_planner_llm.invoke(solution_plan).content

            # Get response
            # response = planner_agent.invoke({"input": scenario, "solution_plan": solution_plan, "tools":planner_tools, "tool_names":tool_names})
            response = planner_agent.invoke({"input": scenario, "solution_plan": solution_plan})

            # Get intermediate steps for main agent
            ## If tool already exists in 
            if self.name in irah_chat_agent.IRAHChatAgent.tool_intermediate_steps_dict:
                irah_chat_agent.IRAHChatAgent.tool_intermediate_steps_dict[self.name].append(response["intermediate_steps"])
            else:
                irah_chat_agent.IRAHChatAgent.tool_intermediate_steps_dict[self.name] = [response["intermediate_steps"]]
            
            # Log end of tool use
            logger.info(f"[{datetime.now()}]  FinancialPlannerTool - Planning Complete")

            return response['output']
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerTool - Error run function: {e}")
            raise Exception("FinancialPlannerTool - Error in FinancialPlannerTool run")

    def configure_tool_schema(self, config = None):
        """
        This method is used to instantiate and set up the schema parameters for the tool.
        """
        # Setup schema with default values
        self.args_schema = FinancialPlannerInput()

        # If values are specified in the request, use them
        # if config:
            # Get tool portion of request
            # self.args_schema.client_name = config['client_name']
        # pass

    def get_tool_config_for_response(self):
        """
        This method is used to get the default configurations used for the tool.
        """
        return self.args_schema.model_dump()

    def get_tool_intermediate_steps(self, item, intermediate_steps_dict, step_index):
        """
        This method is used to get the tool's portion of the intermediate steps from the agent.
        """
        # Construct the main agent steps from the AgentAction class in the agent reasoning steps tuple
        main_agent_steps = f"Tool: {item[0].tool}\nTool Input: {item[0].tool_input}\nLog: {item[0].log}\nAction Output:\n{item[1]}"

        # Concatenate intermediate steps from main agent and the tool
        steps = intermediate_steps_dict[self.name][step_index]
        tool_agent_steps = [f"Tool: {step[0].tool}\nTool Input: {step[0].tool_input}\nLog: {step[0].log}\nAction Output:\n{step[1]}" for step in steps]
        tool_agent_steps = "\n\n".join(tool_agent_steps)

        # Construct output string
        output = f"Main Agent Intermediate Step For {self.name}:\n{main_agent_steps}\n\n{self.name} Agent Intermediate steps:\n{tool_agent_steps}"
        return output
    

# Define function for financial planner standalone endpoint
def financial_planner_chat_agent(llm, req, agent_planner_tools = planner_tools[1:], 
                                 system_message_prefix = SYSTEM_MESSAGE_PREFIX_CHAT_AGENT, system_message_suffix = SYSTEM_MESSAGE_SUFFIX_CHAT_AGENT, human_message = HUMAN_MESSAGE):
    """
    This function is used for the financial planner endpoint. Unlike the financial planner tool that uses only the question, the prompt uses the client name and question.
    """
    try:
        # Create prompt
        prompt = ChatAgent.create_prompt(
            agent_planner_tools,
            system_message_prefix = system_message_prefix,
            system_message_suffix = system_message_suffix,
            human_message = human_message,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names", "client_name", "client_data"]
            )
        
        # Create chain and agent
        llm_chain = LLMChain(llm = llm, prompt = prompt)
        agent = ChatAgent(llm_chain = llm_chain, tools = agent_planner_tools)
        # prompt = PromptTemplate(
        #                 input_variables = ["input", "agent_scratchpad", "tools", "tool_names", "client_name"],
        #                 template = financial_planner_template
        #                 )
        # agent = create_openai_functions_agent(llm = financial_planner_llm, tools=agent_planner_tools, prompt=prompt)
        # tool_names = [tool.name for tool in agent_planner_tools]

        # Get client data
        client_data = ClientDataReaderTool().run(req.client_name)

        # Create solution plan
        create_solution_plan = create_plan(req.question, agent_planner_tools)
        solution_plan = llm.invoke(create_solution_plan).content

        # Create planner agent and invoke
        # planner_agent = AgentExecutor(agent=agent, tools=agent_planner_tools, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True, debug=True, return_source_documents=True)
        planner_agent = AgentExecutor(agent = agent, tools = agent_planner_tools, verbose = True, 
                                    return_intermediate_steps = True, handle_parsing_errors = True, debug = True, return_source_documents = True)
        with get_openai_callback() as cb:
            # answer = planner_agent.invoke({"input": req.question, "client_name": req.client_name, "solution_plan": solution_plan, "tools":agent_planner_tools, "tool_names":tool_names})
            answer = planner_agent.invoke({"input": req.question, "client_name": req.client_name, "client_data": client_data, "solution_plan": solution_plan})

        total_tokens = cb.total_tokens
        prompt_tokens = cb.prompt_tokens
        completion_tokens = cb.completion_tokens
        total_cost = cb.total_cost
        # print(f"{total_tokens = }\n{prompt_tokens = }\n{completion_tokens = }\n{total_cost = }")

        return answer
    except Exception as e:
        logger.error(f"[{datetime.now()}]  FinancialPlannerFunction - Error in financial_planner_agent_chat: {e}")
        raise Exception("FinancialPlannerFunction - error in financial_planner_agent_chat")

