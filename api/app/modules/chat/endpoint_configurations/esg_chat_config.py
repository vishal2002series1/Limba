# Define esg prefix message to add to the prompt for context
esg_prefix_message = """You are an ESG (environmental, social, and governance) specialist that assists ESG analysts in answering questions related to ESG reporting."""

# Define esg chat request configuration
esg_doc_req_config = {
    "question": "",
    "tools": {
        "ContentSearchTool": {
            "filters": {
                'or': [
                    {
                        'field': 'doc_path',
                        'parent_field': None,
                        'field_type': 'str',
                        'operator': 'eq',
                        'value': 'irah-storage-2/wealth/demos/esg_demo',
                    },
                ],
                'join_operator': 'and'
            },
            "search_type": "hybrid",
            "content_retrieved": 3
        }
    },
    "restriction": {
        "categories": ["1", "2", "3"]
    }
}