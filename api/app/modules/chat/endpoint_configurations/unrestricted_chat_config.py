# Define unrestricted chat. This config uses all the configured tools in the chat agent and does not have any restrictions.
unrestricted_req_config = {
    "question": "",
    "tools": {
        "ContentSearchTool": {},
        "DatabaseSearchTool": {},
        "FinancialPlannerTool": {},
        "GoogleSearchTool": {}
        }  
}