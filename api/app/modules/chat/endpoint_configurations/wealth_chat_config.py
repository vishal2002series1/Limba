# Define wealth chat request configuration
wealth_req_config = {
    "question": "",
    "tools": {
        "ContentSearchTool": {
            "filters": None
        },
        "DatabaseSearchTool": {
                "filters":{}
            },
        "FinancialPlannerTool":{
            "client_name": "str"
        }
        },
    "restriction": {
        "categories": ["1"]
    }

}

# Define wealth chat request configuration
wealth_doc_req_config = {
    "question": "",
    "tools": {
        "ContentSearchTool": {
            "filters":{
                'or': [
                    {
                        'field': 'doc_tags',
                        'parent_field': None,
                        'field_type': 'list',
                        'operator': 'eq',
                        'value': 'wealth',
                    },
                ],
                'join_operator':'and'
            }
        },
        "DatabaseSearchTool": {
                "filters":{}
            }
        },
    "restriction": {
        "categories": ["1"]
    }   
}