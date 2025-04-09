# Define req config for hoopp demo chat
hoopp_demo_req_config = {
    "question": "",
    "tools": {
        "ContentSearchTool": {
            "filters":{
                'or': [
                    {
                        'field': 'doc_path',
                        'parent_field': None,
                        'field_type': 'str',
                        'operator': 'eq',
                        'value': 'irah-storage-2/wealth/demos/pe_pension_demo',
                    },
                ],
                'join_operator':'and'
            }
        },
        "DatabaseSearchTool": {},
        "GoogleSearchTool": {}
        },
    "restriction": {
        "categories": ["1"]
    }  
}