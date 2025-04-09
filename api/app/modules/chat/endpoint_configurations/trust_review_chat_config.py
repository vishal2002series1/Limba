# Define esg prefix message to add to the prompt for context
trust_prefix_message = """You are a trust review specialist that assists analysts in answering questions related to the trust document. When given a question, you must use the ContentSearchTool to find the relevant document and answer the question based on the information in the document."""

# Define esg chat request configuration
trust_doc_req_config = {
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
                        'value': 'irah-storage-2/wealth/demos/trust_review_demo',
                    },
                ],
                'join_operator':'and'
            },
          "search_type": "hybrid",
          "content_retrieved": 3
        }
      },
    "restriction": {
        "categories": ["1", "2", "3"]
    }   
}