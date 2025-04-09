# Imports
import os

from typing import Optional, Dict, List
from pydantic import BaseModel, Field


# Define schemas
class FinancialPlannerRequest(BaseModel):
    query: Optional[str] = Field(default = None, description = "The query. It should be a fully formed question")
    client_name: str = Field(default = None, description = "The name of the client asking the question.")


class FinancialPlannerAgentRequest(BaseModel):
    question: Optional[str] = Field(default = None, description = "The query. It should be a fully formed question")
    client_name: str = Field(default = None, description = "The name of the client asking the question.")
    client_data: dict = Field(description = "The client data as sent from the front end request.")


class ContentSearchRequest(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input. It should be a fully formed search query.")
    filters: Optional[Dict] = Field(default = None)
    search_type: Optional[str] = Field(default = os.getenv("ZZ_DEFAULT_SEARCH_TYPE"))
    content_retrieved: Optional[int] = Field(default = int(os.getenv("ZZ_DEFAULT_CONTENT_RETRIEVED")))


class DatabaseSearchRequest(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input to the tool. It should be a fully formed question.")
    filters: Optional[Dict] = Field(None)


class GoogleSearchRequest(BaseModel):
    query: Optional[str] = Field(default = None, description = "The action input to the tool. It should be a fully formed search query.")
    total_retrievals: Optional[int] = Field(default = int(os.getenv("ZZ_Google_Num_Results")))
    relevant_retrievals: Optional[int] = Field(default = int(os.getenv("ZZ_Num_Relevant_Titles")))


class Tools(BaseModel):
    ContentSearchTool: Optional[ContentSearchRequest] = Field(None)
    DatabaseSearchTool: Optional[DatabaseSearchRequest] = Field(None)
    FinancialPlannerTool: Optional[FinancialPlannerRequest] = Field(None)
    GoogleSearchTool: Optional[GoogleSearchRequest] = Field(None)

  
class RestrictionChecker(BaseModel):
    categories: Optional[List[str]] = Field(default=["1","2","3"])

class ChatRequest(BaseModel):
    question: str
    tools: Optional[Tools] = Field(None)
    restriction: Optional[RestrictionChecker] = Field(None)

class CustomChatRequest(BaseModel):
    question: str

class WealthChatRequest(BaseModel):
    question: str

class GetDocsSchema(BaseModel):
    path: str
    filename: str

# Advisor Copilot Schemas
class CallSummary(BaseModel):
    id: int
    summary: str

class Email(BaseModel):
    id: str
    subject: str
    body: str

class Transcript(BaseModel):
    id: int
    transcript: str

class CombinedQuestionRequest(BaseModel):
    question: str = Field(description="The question to be processed.")
    summaries: List[CallSummary] = Field(description="List of call summaries.")
    emails: List[Email] = Field(description="List of emails.")
    transcripts: List[Transcript] = Field(description="List of transcripts.")

class PinnedItem(BaseModel):
    id: str
    content: str
    type: str
    source: str
    title: Optional[str] = None
    group: Optional[str] = None

class ProcessNotesRequest(BaseModel):
    pinnedItems: List[PinnedItem] = Field(description="List of pinned items.")
    notes: str = Field(description="Notes provided by the user.")
    promptInstructions: str = Field(description="Instructions for generating the summary.")