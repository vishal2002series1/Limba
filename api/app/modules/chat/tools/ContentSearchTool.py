# Imports
from datetime import datetime
from ast import literal_eval
from typing import Optional
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

from .. import schema
from app.irah.connections import VECTOR_STORE
from app.irah.logs import logger

class ContentSearchTool(BaseTool):
    name = "ContentSearchTool"
    description = ("This tool is useful for searching a knowledge base for content. " 
                   "Content is usually excerpts from documents (e.g., earnings call transcripts, financial reports, news articles, internal policies & procedures, etc.).\n"
                   "Earnings call transcripts: A company's earnings call transcript contains a comprehensive overview of its financial performance, strategic initiatives, "
                   "industry trends, and future guidance. It includes details about revenue, net income, and other financial metrics, along with analysis of business segments and "
                   "operational challenges. The transcript often features a Q&A session with analysts and investors. Key topics covered are capital allocation, shareholder returns, "
                   "risks, and corporate governance. These transcripts are essential for investors and analysts to gain insights into a company's financial health and future prospects.\n"
                   "Financial documents: Companies' financial documents, such as Form 8-K, Form 10-Q, Form 4, Form 13F, and Form 144, are filed with the U.S. SEC to provide important "
                   "information to investors and ensure regulatory compliance. Form 8-K reports significant events, Form 10-Q presents quarterly financial updates, Form 4 discloses "
                   "insider transactions, Form 13F lists institutional investment managers' holdings, and Form 144 notifies the SEC of planned sales of restricted securities. "
                   "These documents offer transparency into a company's financial condition, management changes, insider activity, and investment positions.\n"
                   "News articles: Company news articles contain information about a company's financial performance, business developments, product launches, leadership changes, "
                   "legal matters, industry analysis, CSR initiatives, and stock market performance. They provide insights into a company's operations, strategy, and market standing. "
                   "Readers should verify information from reliable sources and official filings for accuracy and objectivity. These articles are useful for investors, analysts, and "
                   "stakeholders to stay informed about a company's activities and financial health.\n\n"
                   "Input should be a search query (string). Output should be a list of documents that match the query."
                   "Below are some examples of questions that this tool should be used to retrieve information for:\n"
                   "* What are the key takeaways from Delta Airline's earnings call?\n"
                   "* What is the news saying about Marriot's latest annual report?\n"
                   "* What are the key takeaways from American Airline's 2023 8-K report?")
    args_schema = schema.SearchInput
    
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> list:
        """
        Run the tool to search for content.
        """
        try:
            logger.info(f"[{datetime.now()}] ContentSearchTool - retrieval initiated")
            
            # Generate filters for the search
            filters = self.generate_azure_search_filter(self.args_schema.filters)
            
            # Perform the search
            docs = VECTOR_STORE.similarity_search(
                query=query, 
                filters=filters, 
                k=self.args_schema.content_retrieved, 
                search_type=self.args_schema.search_type
            )
            
            if not docs:
                return "No matching Documents found, try changing the filters"
            
            # Parse the retrieved documents
            relevant_docs = [
                {
                    'page_content': doc.page_content,
                    'content_id': doc.metadata['content_id'],
                    'doc_name': doc.metadata['doc_name'],
                    'content_doc_pages': doc.metadata['content_doc_pages'],
                    'content_tokens': doc.metadata['content_tokens'],
                    'doc_words': doc.metadata['doc_words'],
                    'doc_url': doc.metadata['doc_url'],
                    'doc_path': doc.metadata['doc_path'],
                    'doc_details': doc.metadata['doc_details'],
                    'doc_id': doc.metadata['doc_id'],
                    'doc_tags': doc.metadata['doc_tags'],
                    'score': doc.metadata['@search.score']
                } for doc in docs
            ]
            
            # Sort documents by score, log completion and return the results
            relevant_docs.sort(key=lambda x: x['score'], reverse=True)
            logger.info(f"[{datetime.now()}] ContentSearchTool - Content retrieval complete")

            return f"{relevant_docs}"
        except Exception as e:
            logger.error(f"[{datetime.now()}] ContentSearchTool - Error in run function: {e}")
            raise Exception("ContentSearchTool - Document Retrieval Failed")

    def configure_tool_schema(self, config=None):
        """
        This method is used to instantiate and set up the schema parameters for the tool.
        """
        try:
            logger.info(f"[{datetime.now()}]  ContentSearchTool - configuring schema")
            self.args_schema = schema.SearchInput()
            # print("CONFIG:", config)
            
            if config:
                if 'filters' in config.keys():
                    self.args_schema.filters = config['filters']
                if 'search_type' in config.keys():
                    self.args_schema.search_type = config['search_type']
                if 'content_retrieved' in config.keys():
                    self.args_schema.content_retrieved = int(config['content_retrieved'])
        except Exception as e:
            logger.error(f"[{datetime.now()}]  ContentSearchTool - Error in config schema: {e}")
            raise Exception(" ContentSearchTool - Schema Configuration of ContentSearchTool Failed")


    def get_tool_config_for_response(self):
        """
        This method is used to get the default configurations used for the tool.
        """
        return self.args_schema.model_dump()
    
    def get_tool_intermediate_steps(self, item, intermediate_steps_dict, step_index):
        """
        This method is used to get the tool's portion of the intermediate steps from the agent.
        """
        # Construct the output from the AgentAction class in the agent reasoning steps tuple
        output = f"Tool: {item[0].tool}\nTool Input: {item[0].tool_input}\nLog: {item[0].log}\nAction Output:\n{item[1]}"
        return output

    def get_tool_intermediate_content(self, item):
        """
        This method is used to get the contents retrieved from the agent.
        """
        try:
            return literal_eval(item[1])
        except Exception as e:
            logger.error(f"[{datetime.now()}] ContentSearchTool - Error in get_tool_intermediate_content: {e}")
            return []

    def generate_azure_search_filter(self, filters):
        """
        This method is used to generate azure search filters for the tool.
        """
        try:
            if filters:
                logger.info(f"[{datetime.now()}]  ContentSearchTool - Generate Filter for Azure Search")
                filter_str = ""
                if 'join_operator' in filters.keys():

                    join_operator = filters.pop('join_operator')
                    for logic_operator, conditions in filters.items():
                        if filter_str:
                            filter_str += f" {join_operator} "

                        condition_str = ""
                        for condition in conditions:
                            field = condition['field']
                            parent_field = condition['parent_field']
                            field_type = condition['field_type']
                            operator = condition['operator']
                            value = condition['value']

                            if parent_field:
                                full_field = f"{parent_field}/{field}"
                            else:
                                full_field = field

                            if condition_str:
                                condition_str += f" {logic_operator} "

                            if operator == 'ismatch':
                                condition_str += f"search.ismatch('{value}', '{full_field}')"
                            elif field_type == 'list':
                                condition_str += f"{full_field}/any(t: (t {operator} '{value}'))"
                            else:
                                condition_str += f"{full_field} {operator} '{value}'"

                        filter_str += f"({condition_str})"

                    return filter_str
                else:
                    return None
            else:
                return None
        except Exception as e:
            logger.error(f"[{datetime.now()}]  ContentSearchTool - Error in Generate Azure Filter function: {e}")
            raise Exception(f"ContentSearchTool -  Error in Azure Search Filter generation")