# Imports
import os
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from . import SearchInput, GoogleSearchInput

# Define schemas
class FinancialPlannerResponseSchema(BaseModel):
    client_name: Optional[str] = Field(default=None, description = "The name of the client asking the question.")


class LlmMetric(BaseModel):
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_cost: float
    successful_requests: int
    llm_model_name: str
    temperature: float


class ContentSearchResponseSchema(BaseModel):
    content_used: List[Dict] = Field(default=[])
    other_relevant_content: List[Dict] = Field(default=[])


class DatabaseSearchResponseSchema(BaseModel):
    sql_query: List[str] = Field(default=[])


class GoogleSearchResponseSchema(BaseModel):
    urls_used: List = Field(description = "List of the URLs used in the final answer.", default = [])
    other_relevant_urls: List = Field(description = "List of the URLs retrieved from the tool.", default = [])


class RestrictionCheckerResponseSchema(BaseModel):
    response_type: Optional[int] = Field(default = None)
    question_category: Optional[str] = Field(default = None)


class AnnotationResponseSchema(BaseModel):
    ContentSearchTool: Optional[ContentSearchResponseSchema] = Field(None)
    DatabaseSearchTool: Optional[DatabaseSearchResponseSchema] = Field(None)
    FinancialPlannerTool: Optional[FinancialPlannerResponseSchema] = Field(None)
    GoogleSearchTool: Optional[GoogleSearchResponseSchema] = Field(None)
    RestrictionChecker: Optional[RestrictionCheckerResponseSchema] = Field(None)


class ContentSearchParamResponseSchema(SearchInput):
    pass   

class DatabaseSearchParamResponseSchema(BaseModel):
    filters: Optional[Dict] = Field(None)
    database_name: Optional[str] = Field(None)


class GoogleSearchParamResponseSchema(GoogleSearchInput):
    pass
class ToolsResponseSchema(BaseModel):
    ContentSearchTool: Optional[ContentSearchParamResponseSchema] = Field(None)
    DatabaseSearchTool: Optional[DatabaseSearchParamResponseSchema] = Field(None)
    FinancialPlannerTool: Optional[FinancialPlannerResponseSchema] = Field(None)
    GoogleSearchTool: Optional[GoogleSearchParamResponseSchema] = Field(None)


class SystemMetricResponseSchema(BaseModel):
    llm_usage_metrics: LlmMetric
    agent_reasoning_steps: List[str]
    agent_response_time: float


class ResponseSchema(BaseModel):
    question: str
    response: str
    annotations: AnnotationResponseSchema = Field(None)
    tools: ToolsResponseSchema
    system_metrics: SystemMetricResponseSchema


class FinancialPlannerResponseSchema(BaseModel):
    question: str
    response: str
    annotations: Optional[dict]
    tools: Optional[dict]
    system_metrics: SystemMetricResponseSchema


class SearchMetric(BaseModel):
    search_type: str


class ColumnSearchInput(BaseModel):
    query: str = Field(description="List of tables")

# Advisor Copilot
#     Helpers:
class RelevantTranscript(BaseModel):
    transcript_id: int
    summary: str
    relevant_sentences: List[str]

class QuestionAnswer(BaseModel):
    question: str
    answer: str
    relevant_transcripts: List[RelevantTranscript]

class TranscriptSelector(BaseModel):
    chain_of_thought: str
    relevant_transcript_ids: List[int]

class RelevantEmail(BaseModel):
    email_id: str
    subject: str
    relevant_sentences: List[str]

class QuestionAnswerEmail(BaseModel):
    question: str
    answer: str
    relevant_emails: List[RelevantEmail]

class EmailSelector(BaseModel):
    chain_of_thought: str
    relevant_email_ids: List[str]

class CombinedSelector(BaseModel):
    chain_of_thought: str
    relevant_transcript_ids: List[int]
    relevant_email_ids: List[str]

#     Actual Response Schemas:
class ProcessNotesResponse(BaseModel):
    summary: str

class CombinedQuestionAnswer(BaseModel):
    question: str
    answer: str
    relevant_transcripts: List[RelevantTranscript]
    relevant_emails: List[RelevantEmail]