from app.irah.connections import Data, DataObj
from . import schema

class Log(DataObj):
    def __init__(self):
        self.db = Data(table= "logs", schema = schema.Log)

class LogFinancialPlanner(DataObj):
    def __init__(self):
        self.db = Data(table= "logs_financial_planner", schema = schema.LogFinancialPlanner)
