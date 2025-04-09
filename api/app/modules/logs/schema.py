# Imports
import uuid
from datetime import datetime

from app.modules.chat.schema.response_schema import ResponseSchema, FinancialPlannerResponseSchema


# Create log schema
class LogRequest(ResponseSchema):
    pass


class Log(LogRequest):
    key: str = uuid.uuid4().hex.upper()
    created: datetime = datetime.utcnow()
    modified: datetime = datetime.utcnow()


class LogResponse(Log):
    pass


# Create log schema for financial planner
class LogFinancialPlannerRequest(FinancialPlannerResponseSchema):
    pass


class LogFinancialPlanner(LogFinancialPlannerRequest):
    key: str = uuid.uuid4().hex.upper()
    created: datetime = datetime.utcnow()
    modified: datetime = datetime.utcnow()


class LogFinancialPlannerResponse(LogFinancialPlanner):
    pass