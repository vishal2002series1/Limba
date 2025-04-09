from . import schema, data

def create_log(log) -> schema.LogResponse:
    temp = schema.LogRequest(**log.dict())
    created = data.Log().create(item=temp).get()
    return schema.LogResponse(**created.dict())

def get_log(key) -> schema.LogResponse:
    item = data.Log().load(key=key).get()
    return schema.LogResponse(**item.dict())

# Create log for financial planner
def create_log_financial_planner(log) -> schema.LogFinancialPlannerResponse:
    temp = schema.LogFinancialPlannerRequest(**log.dict())
    created = data.LogFinancialPlanner().create(item=temp).get()
    return schema.LogFinancialPlannerResponse(**created.dict())

def get_log_financial_planner(key) -> schema.LogFinancialPlannerResponse:
    item = data.LogFinancialPlanner().load(key=key).get()
    return schema.LogFinancialPlannerResponse(**item.dict())