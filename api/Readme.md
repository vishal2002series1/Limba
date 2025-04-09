# IRAH

IRAH is an LLM-powered platform for content aggregation, information search/synthesis, and content generation that assists professionals in the Wealth & Asset Management industry perform their jobs more efficiently.

IRAH includes a user interface (UI), an application programming interface (API), and a file-processing module for processing documents. It uses Python for backend operations and Angular for frontend operations.

## Project Structure

The project is structured into three main folders: `api`, `ui`, and `file-processing`.

### API

The `api` folder contains all the backend code for the application. This includes the communication with the LLMs & other data systems. It includes several utility scripts for data processing, fetching, and management. The main entry point of the application is `main.py`.

### UI

The `ui` folder contains the frontend code for the application. It includes all the Angular components, services, models, and styles. It also includes the `angular.json` configuration file, `package.json` and `package-lock.json` for managing npm packages, and `tsconfig.json` for TypeScript configuration.

### File-Processing

The `file-processing` folder includes scripts for processing and managing files & documents. It includes preprocessing scripts, summary templates, embedding scripts, and more. The file-processing module is designed to run as a function using Azure Functions. This allows for automated processing of documents as they are loaded to a file store.

## Installation
1. Clone the repo
```sh
git clone -b IRAH-Fastapi git@github.com:ey-org/irah.git
```
2. Install Python packages
```sh
cd api
pip install -r requirements.txt
```
3. Install NPM packages
```sh
cd ../ui
npm install
```

## Running the Project

To run the project locally:

1. Start the API server
```sh
cd api
uvicorn main:app --reload
```

2. Start the Angular server
```sh
cd ../ui
ng serve
```

The API server will start on `localhost:5000` and the Angular server will start on `localhost:4200`.

Note: In order to successfully connect to the various data sources & API endpoints required by IRAH, you will need to include a `devConfig.yml` file in your project directory. This file contains the API keys and other secrets for connecting to these services. Please reach out to Matt O'Neill (matt.oneill@ey.com) for access.

## Overview of Project Files
- **API Folder**  
  - `api`: Folder that has the complete backend code  
    - `app`: This is the main code folder
        - `archive`: This folder has old legacy code
        - `irah`: This folder has code that is used by all the application modules
            - `connections`: This is the folder where all the connections are defined
                - `__init__.py`
                - `azure_ai_search.py`: Azure AI search connections defined here.
                - `azure_blob.py`: Azure Blob Storage connection defined here.
                - `azure_openai.py`: Azure OpenAI and LLM connections are defined here.
                - `bing.py`: Bing connection is defined here.
                - `json_pandas.py`: This file has a custom engine to use JSON files as a database.
                - `snowflake.py`: Snowflake connections are defined here.
            - `__init__.py`
            - `object.py`: This file has a generic engine for CRUD operations to any database.
            - `router.py`: This file has the custom router that is used by all modules.
        - `modules`: This folder contains all the application modules
            - `auth`
                - `__init__.py`
                - `actions.py`: Main logic for authentication is found here.
                - `api.py`: This file has all the APIs related to authentication.
                - `schema.py`: This file contains the authentication schema.
            - `chat`
                - `agents`: This has the custom Langchain agent classes 
                    - `__init__.py`
                    - `irah_chat_agent.py`: This contains the main chat agent class.
                - `endpoint_configurations`
                    - `default_config.py`: This file has all the default configs of the chat agent.
                    - `wealth_chat_config.py`: This file has wealth endpoint related configs.
                - `prompt_templates`
                    - `__init__.py`
                    - `agent_prompt_templates.py`: Contains the agent prompt templates.
                    - `database_search_prompt_template.py`: Contains database prompt templates.
                    - `financial_planner_prompt_templates.py`: Contains the financial planner prompt templates.
                - `schema`
                    - `__init__.py`
                    - `request_schema.py`: Contains all the request schemas related to the chat module.
                    - `response_schema.py`: Contains all the response schemas related to the chat module.
                    - `tools_schema.py`: Contains all the tools schemas related to the tools.
                - `tools`
                    - __init__.py
                    - available_tools_repo.py: this all the list of all available tools
                    - ContentSearchTool.py: this has the custom search tool
                    - DatabaseSearchTool.py: this has a database search tool
                    - FinancialPlannerTool.py: this has a finnancial Planner tool
                    - RestrictionChecker.py: this has the restriction checker
                - `__init__.py`
                - `actions.py`: Logic for all endpoints for the chat module.
                - `api.py`: File with all the chat API endpoints.
            - `logs`
                - `__init__.py`
                - `actions.py`: Logic related to logs.
                - `data.py`: Logic for data class connection.
                - `schema.py`: Schemas for logs.
            - `__init__.py`
        - `store`
            - `data`
                - `logs.json`: Stores the logs of every successful call.
            - `files`
            - `metadata`
                - `financial_planner_user_profile.json`: User data for the financial planner.
                - `snowflake_metadata.json`: Details for the database schema.
        - `__init__.py`
    - `main.py`: Entry point to run the server.
    - `requirements.txt`: Lists the Python dependencies for the project.  
  - `.env`: File with all the API credentials.

## Overview of the Backend Endpoints:

### AUTH:
- **POST**: `/irah/auth/login`

### CHAT:
- **POST**: `/irah/chat/`
    - **Description**: This endpoint is a custom chat endpoint, through which you can access all the available tools to the agent in its fullest potential.
    - **Request Body**: Example requests:
        1. Mentioning all the tools along with filters and configs:
            ```json
            {
              "question": "",
              "tools": {
                "ContentSearchTool": {
                  "filters":{
                    "or": [
                      {
                        "field": "doc_tags",
                        "parent_field": null,
                        "field_type": "list",
                        "operator": "eq",
                        "value": "wealth"
                      },
                      {
                        "field": "doc_tags",
                        "parent_field": null,
                        "field_type": "list",
                        "operator": "eq",
                        "value": "portfolio"
                      }
                    ],
                    "and": [
                      {
                        "field": "company_name",
                        "parent_field": "doc_details",
                        "field_type": "str",
                        "operator": "ismatch",
                        "value": "EY"
                      },
                      {
                        "field": "industry_name",
                        "parent_field": "doc_details",
                        "field_type": "str",
                        "operator": "eq",
                        "value": "Business"
                      }
                    ],
                    "join_operator":"and"
                  },
                  "search_type": "hybrid",
                  "content_retrieved": 4
                },
                "DatabaseSearchTool": {
                  "filters": {}
                },
                "FinancialPlannerTool": {
                  "client_name": "string"
                }
              }
            }
            ```
        2. Mentioning specific tools you want the agent to use (in this case, ContentSearchTool and DatabaseSearchTool only):
            ```json
            {
              "question": "",
              "tools": {
                "ContentSearchTool": {
                  "filters": {},
                  "search_type": "hybrid",
                  "content_retrieved": 4
                },
                "DatabaseSearchTool": {
                  "filters": {}
                }
              }
            }
            ```
        3. Mentioning only the question:
            ```json
            {
              "question": ""
            }
            ```
    - **Response Body**: Example response:
        ```json
        {
          "question": "Who is the CFO of American Airlines?",
          "response": "Derek J. Kerr is the CFO of American Airlines.",
          "

```json
          "annotations": {
            "ContentSearchTool": {
              "content_used": [
                "79e9ec4f-1652-4080-af5a-ef7c3a22682a"
              ],
              "content_retrieved": [
                [
                  {
                    "page_content": "...",
                    "content_id": "412411aa-e63a-4edc-bbe5-375c4a721405",
                    "doc_name": "AAL Q4 2021 Earnings Call Summary.pdf",
                    "content_doc_pages": [1,2,3,4],
                    "content_tokens": 977,
                    "doc_words": 13816,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202021%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "20_01_2022",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Aviation"
                    },
                    "doc_id": "985754Z-1dcd7b13-29ba-4506-a42b-b84779f6e50c",
                    "doc_tags": [
                      "wealth"
                    ]
                  },
                  {
                    "page_content": "...",
                    "content_id": "6cc91c02-47be-4afb-b8d6-7a77b8c04fd3",
                    "doc_name": "AAL Q1 2023 Earnings Call Summary.pdf",
                    "content_doc_pages": [20,21],
                    "content_tokens": 993,
                    "doc_words": 12732,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q1%202023%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "27_04_2023",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Airline"
                    },
                    "doc_id": "813067Z-be57ada5-ae35-4a56-89b8-7f3b1dffe5d9",
                    "doc_tags": [
                      "wealth"
                    ]
                  },
                  {
                    "page_content": "...",
                    "content_id": "79e9ec4f-1652-4080-af5a-ef7c3a22682a",
                    "doc_name": "AAL Q4 2020 Earnings Call Summary.pdf",
                    "content_doc_pages": [17,18,19],
                    "content_tokens": 992,
                    "doc_words": 12840,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202020%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "NA",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Airline"
                    },
                    "doc_id": "939486Z-d7304eee-3107-40a6-94a0-6aecc3e8c0be",
                    "doc_tags": [
                      "wealth"
                    ]
                  }
                ]
              ]
            }
          },
          "tools": {
            "ContentSearchTool": {
              "search_type": "hybrid",
              "content_retrieved": 3
            },
            "DatabaseSearchTool": {},
            "FinancialPlannerTool": {}
          },
          "system_metrics": {
            "llm_usage_metrics": {
              "total_tokens": 5133,
              "prompt_tokens": 4950,
              "completion_tokens": 183,
              "total_cost": 0.15948,
              "successful_requests": 2,
              "llm_model_name": "gpt-4-1106-preview",
              "temperature": 0
            },
            "agent_reasoning_steps": [
            "tool='ContentSearchTool' tool_input='Who is the current CFO of American Airlines?' log='To find out who the current CFO of American Airlines is, I will use the ContentSearchTool to search for recent documents that might mention the current CFO of the company.\\n\\nAction: ContentSearchTool\\nAction Input: Who is the current CFO of American Airlines?'"
            ],
            "agent_response_time": 30
          }
        }
        ```

- **POST**: `/irah/chat/wealth`
    - **Description**: This endpoint is a Wealth chat endpoint, where the Content Search tool is restricted to retrieve content from the wealth folder. This endpoint has access to two tools: ContentSearchTool and DatabaseSearchTool.
    - **Request Body**: Example request:
        ```json
        {
          "question": ""
        }
        ```
    - **Response Body**: Example response:
        ```json
        {
          "question": "Who is the CFO of American Airlines?",
          "response": "Derek J. Kerr is the CFO of American Airlines.",
          "annotations": {
            "ContentSearchTool": {
              "content_used": [
                "79e9ec4f-1652-4080-af5a-ef7c3a22682a"
              ],
              "content_retrieved": [
                [
                  {
                    "page_content": "...",
                    "content_id": "412411aa-e63a-4edc-bbe5-375c4a721405",
                    "doc_name": "AAL Q4 2021 Earnings Call Summary.pdf",
                    "content_doc_pages": [1,2,3,4],
                    "content_tokens": 977,
                    "doc_words": 13816,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202021%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "20_01_2022",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Aviation"
                    },
                    "doc_id": "985754Z-1dcd7b13-29ba-4506-a42b-b84779f6e50c",
                    "doc_tags": [
                      "wealth"
                    ]
                  },
                  {
                    "page_content": "...",
                    "content_id": "6cc91c02-47be-4afb-b8d6-7a77b8c04fd3",
                    "doc_name": "AAL Q1 2023 Earnings Call Summary.pdf",
                    "content_doc_pages": [20,21],
                    "content_tokens": 993,
                    "doc_words": 12732,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q1%202023%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "27_04_2023",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Airline"
                    },
                    "doc_id": "813067Z-be57ada5-ae35-4a56-89b8-7f3b1dffe5d9",
                    "doc_tags": [
                      "wealth"
                    ]
                  },
                  {
                    "page_content": "...",
                    "content_id": "79e9ec4f-1652-4080-af5a-ef7c3a22682a",
                    "doc_name": "AAL Q4 2020 Earnings Call Summary.pdf",
                    "content_doc_pages": [17,18,19],
                    "content_tokens": 992,
                    "doc_words": 12840,
                    "doc_url": "https://wamllmpocstorage.blob.core.windows.net/irah-storage-2/testing/wealth/AAL%20Q4%202020%20Earnings%20Call%20Summary.pdf",
                    "doc_path": "irah-storage-2/testing/wealth",
                    "doc_details": {
                      "publication_date": "NA",
                      "company_name": "American Airlines Group, Inc. (AAL)",
                      "industry_name": "Airline"
                    },
                    "doc_id": "939486Z-d7304eee-3107-40a6-94a0-6aecc3e8c0be",
                    "doc_tags": [
                      "wealth"
                    ]
                  }
                ]
              ]
            }
          },
          "tools": {
            "ContentSearchTool": {
              "search_type": "hybrid",
              "content_retrieved": 3
            },
            "DatabaseSearchTool": {},
            "FinancialPlannerTool": {}
          },
          "system_metrics": {
            "llm_usage_metrics": {
              "total_tokens": 5133,
              "prompt_tokens": 4950,
              "completion_tokens": 183,
              "total_cost": 0.15948,
              "successful_requests": 2,
              "

llm_model_name": "gpt-4-1106-preview",
              "temperature": 0
            },
            "agent_reasoning_steps": [
            "tool='ContentSearchTool' tool_input='Who is the current CFO of American Airlines?' log='To find out who the current CFO of American Airlines is, I will use the ContentSearchTool to search for recent documents that might mention the current CFO of the company.\\n\\nAction: ContentSearchTool\\nAction Input: Who is the current CFO of American Airlines?'"
            ],
            "agent_response_time": 30
          }
        }
        ```

- **POST**: `/irah/chat/financial_planner`
    - **Description**: This endpoint gives you access to the Financial Planner tool only.
    - **Request Body**: 
        ```json
        {
          "question": "string",
          "client_name": "string"
        }
        ```
    - **Response Body**:
        ```json
        {
          "input": "Will my client be able to retire by 65?",
          "client_name": "Jane Smith",
          "solution_plan": "To answer the question 'Will my client be able to retire by 65?', I would need to know the client's current financial status, their savings, and their retirement goals. Here's how I would go about it:\n\n1. Use the `ClientDataReaderTool` to get the client's financial data. This will provide me with the client's current age, total savings, annual savings, and annual savings growth rate.\n\n2. Use the `RetirementSimulationTool` to simulate the client's retirement savings and expenses. The input parameters for this tool would be the client's current age, retirement age goal (which is 65 in this case), total savings, annual savings, and annual savings growth rate.\n\n3. The `RetirementSimulationTool` will calculate the likelihood of the client achieving their retirement monetary goal by the age of 65. If the likelihood is high, then the client will be able to retire by 65. If the likelihood is low, then the client may need to adjust their retirement plans.\n\n4. If the likelihood is low, I would suggest the client to either increase their annual savings, extend their retirement age, or adjust their retirement monetary goal. I would then use the `RetirementSimulationTool` again with the adjusted parameters to see if the likelihood of retirement by 65 has improved.\n\n5. Repeat steps 3 and 4 until the client is satisfied with their retirement plan.\n\nThis process will help the client understand their current financial status and what adjustments they need to make in order to retire by 65.",
          "output": "Yes, Jane Smith will be able to retire by 65 based on her current financial status and retirement plans. In fact, she could potentially retire as early as 58 years old. However, these are just estimates and actual results may vary. It's recommended that Jane continues to monitor her financial situation and adjust her retirement plans as necessary.",
          "intermediate_steps": [
            [
              {
                "tool": "ClientDataReaderTool",
                "tool_input": "Jane Smith",
                "log": "Thought: I need to use the ClientDataReaderTool to get the client's financial data.\nAction:\n```\n{\n  \"action\": \"ClientDataReaderTool\",\n  \"action_input\": \"Jane Smith\"\n}\n```",
                "type": "AgentAction"
              },
              "{\"client_data\": {\"name\": \"Jane Smith\", \"age\": 45, \"retirement_age\": 65, \"total_savings\": 350000, \"monthly_income\": 12000, \"deposit_rate\": 0.05, \"location\": {\"city\": \"New York\", \"state\": \"New York\"}, \"retirement_accounts\": [{\"type\": \"401k\", \"balance\": 200000, \"contribution\": 19500, \"annual_growth\": 0.07}, {\"type\": \"IRA\", \"balance\": 100000, \"contribution\": 6000, \"annual_growth\": 0.06}], \"trust_fund_accounts\": [{\"beneficiary\": \"Child\", \"balance\": 50000, \"contribution\": 10000, \"annual_growth\": 0.05}, {\"beneficiary\": \"Grandchild\", \"balance\": 0, \"contribution\": 5000, \"annual_growth\": 0.04}], \"house\": {\"value\": 800000, \"mortgage_balance\": 400000, \"monthly_payment\": 3000, \"interest_rate\": 0.03, \"years_left\": 15}, \"other_investments\": [{\"type\": \"Stocks\", \"balance\": 25000, \"annual_growth\": 0.08}, {\"type\": \"Bonds\", \"balance\": 15000, \"annual_growth\": 0.03}]}, \"annual_savings\": 25500, \"annual_savings_growth\": 0.065}"
            ],
            [
              {
                "tool": "RetirementSimulationTool",
                "tool_input": {
                  "current_age": 45,
                  "retirement_age_goal": 65,
                  "total_savings": 350000,
                  "annual_savings": 25500,
                  "annual_savings_growth_rate": 0.065
                },
                "log": "The client's current age is 45 and she wants to retire at 65. Her total savings are $350,000 and she saves $25,500 annually. The annual growth rate of her savings is 6.5%. Now, I will use the RetirementSimulationTool to determine if she will be able to retire by 65.\nAction:\n```\n{\n  \"action\": \"RetirementSimulationTool\",\n  \"action_input\": {\n    \"current_age\": 45,\n    \"retirement_age_goal\": 65,\n    \"total_savings\": 350000,\n    \"annual_savings\": 25500,\n    \"annual_savings_growth_rate\": 0.065\n  }\n}\n```",
                "type": "AgentAction"
              },
              "Assuming a 6.50% annual savings growth, a 4.00% rate of return on investments after retirement, market volatility of 3.00%, and a monthly retirement cost of living of $5,000.00 for 30 years after retirement: the likelihood of the client retiring by 65 years old is 100.00%.\nGiven the assumptions, the most likely age for the client to retire with a calculated retirement monetary goal of $1,800,000.00 is at the age of 58."
            ]
          ]
        }
        ```

### FILES:
- **POST**: `/irah/files/get_documents`
    - **Description**: This endpoint is used to retrieve the documents.
    - **Request Body**:
        ```json
        {
          "path": "../../../",
          "filename": "....pdf"
        }
        ```
    - **Response**: 
        - File Blob

---

