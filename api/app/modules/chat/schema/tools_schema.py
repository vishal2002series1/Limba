# Imports
import os

from pydantic import BaseModel, Field
from typing import Optional, Dict


# Define schemas
## Financial Planner Tool schems
class ClientDataReaderInput(BaseModel):
    client_name: str = Field(description = "Name of the client to get data for.", default = "Jane Smith")

class RetirementSimulationInput(BaseModel):
    current_age: int = Field(description = "Current age of the client")
    retirement_age_goal: int = Field(description = "Desired retirement age (goal) of the client")
    total_savings: float = Field(description = "The client's total savings")
    annual_savings: float = Field(description = "The client's annual savings")
    annual_savings_growth_rate: float = Field(description = "The client's average annual savings growth rate")
    cost_of_living: Optional[float] = Field(description = "Cost (expense) of living during retirement", default = 5000.00)
    retirement_monetary_goal: Optional[float] = Field(description = "Retirement monetary goal", default = None)
    return_rate: Optional[float] = Field(description = "Expected rate of return", default = 0.04)
    volatility: Optional[float] = Field(description = "Market volatility", default = 0.03)

class MonthlyPaymentCalculatorInput(BaseModel):
    price: float = Field(description = "The price of the item to calculate a monthly payment for.")
    interest_rate: float = Field(description = "Interest rate for the loan.")
    loan_term: int = Field(description = "Number of years for the loan")
    down_payment: Optional[float] = Field(description = "Down payment amount on the loan", default = None)

class LoanAmountCalculatorInput(BaseModel):
    monthly_payment: float = Field(description = "The expected monthly payment for the loan amount to be calculated.")
    interest_rate: float = Field(description = "Interest rate for the loan.")
    loan_term: int = Field(description = "Number of years for the loan")
    down_payment: Optional[float] = Field(description = "Down payment amount on the loan", default = None)

class LoanTermCalculatorInput(BaseModel):
    expected_monthly_payment: float = Field(description = "The current or expected monthly payment for the loan amount to be calculated.")
    expected_loan_balance: float = Field(description = "The current or expected balance / principal on the loan.")
    current_interest_rate: float = Field(description = "Interest rate for the loan.")

class FinancialPlannerInput(BaseModel):
    # scenario: Optional[str] = Field(default = None, description = "The query. It should be a fully formed question")
    client_name: Optional[str] = Field(default = None, description = "The name of the client asking the question.")

class FinancialPlannerChatRequest(BaseModel):
    query: Optional[str] = Field(default = None, description = "The query. It should be a fully formed question")
    client_name: Optional[str] = Field(default = None, description = "The name of the client asking the question.")


## Content Search Tool schema
class SearchInput(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input. It should be a fully formed search query.")
    filters: Optional[dict] = Field(default = None)
    search_type: str = Field(default='hybrid',description="type of search to be performed")
    content_retrieved: Optional[int] = Field(default = int(os.getenv("ZZ_DEFAULT_CONTENT_RETRIEVED")))

class AgentParams(BaseModel):
    content_search: SearchInput = Field(default={'search_type': 'hybrid','filters': None})


## Database Search Tool Schema
class DataBaseSearchInput(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input to the tool. It should be a fully formed question.")
    filters: Optional[Dict] = Field(default=None)

class ColumnSearchInput(BaseModel):
    query: str = Field(description="List of tables")

## Google API Schema
class GoogleSearchInput(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input to the tool. It should be a fully formed search query.")
    total_retrievals: Optional[int] = Field(default = int(os.getenv("ZZ_Google_Num_Results")))
    relevant_retrievals: Optional[int] = Field(default = int(os.getenv("ZZ_Num_Relevant_Titles")))
