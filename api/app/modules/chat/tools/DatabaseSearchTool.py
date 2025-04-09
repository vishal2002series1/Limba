# Imports
import json,time
from datetime import datetime
import re

from typing import Optional
from langchain.chains import LLMChain
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

from .. import schema
from app.irah.connections import database_search_llm
from app.irah.connections import SQL_DB
from ..prompt_templates.database_search_prompt_template import get_tables_template, get_sql_query_template,get_tables_examples,get_sql_query_examples, DatabaseSearchTool_description 
from app.irah.logs import logger
from app.modules.chat.agents import irah_chat_agent

# Load mock data
with open("app/store/metadata/snowflake_metadata.json", "r") as f:
    table_json = json.load(f)
 
def get_tables_list(db_name, schema):
    try:
        table_list = []
        if table_json["database"]==db_name:
            for n_schema in table_json["schemas"]:
                if n_schema["schema"]==schema:
                    for n_table in n_schema["tables"]:
                        keys_to_extract = ['table_name', 'table_description']
                        res = dict(filter(lambda item: item[0] in keys_to_extract, n_table.items()))
                        table_list.append(res)      
        return table_list
    except Exception as e:
        logger.error(f"[{datetime.now()}]  DatabaseSearchTool - Error in getting Table list: {e}")
        raise Exception(f"DatabaseSearchTool - Error in getting Table list")
 
 
tables = get_tables_list(db_name = "IRAH_WEALTH_DB", schema = "dbo")


def get_columns_list(db_name,schema, table_list):
    try:
        column_list = []
        if table_json["database"]==db_name:
            for n_schema in table_json["schemas"]:
                if n_schema["schema"]==schema:
                    for n_table in n_schema["tables"]:
                        for table in table_list:
                            if n_table['table_name']==table:
                                keys_to_extract = ['table_name', 'columns']
                                res = dict(filter(lambda item: item[0] in keys_to_extract, n_table.items()))
                                column_list.append(res)      
        return column_list
    except Exception as e:
        logger.error(f"[{datetime.now()}]  DatabaseSearchTool - Error in get column list: {e}")
        raise Exception(f"DatabaseSearchTool - Error in get column list")
 
 
class DatabaseSearchTool(BaseTool):
    name = "DatabaseSearchTool"
    description = (DatabaseSearchTool_description )
    args_schema = schema.DataBaseSearchInput

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Search for data in a SQL database.
        """
        try:
            # Log initiation
            logger.info(f"[{datetime.now()}]  DatabaseSearchTool - retrieval initiated")

            # Get the tables and columns list
            tables = self.get_tables(query)
            table_list = [table.strip() for table in tables.split(',')]
            columns_list = get_columns_list(db_name="IRAH_WEALTH_DB",schema="dbo",table_list=table_list)

            # Get the SQL query and final response
            sql_query = self.get_sql_query(query=query,columns_list=columns_list)
            response = SQL_DB.run_no_throw(sql_query)

            # Log completion and return the response
            logger.info(f"[{datetime.now()}]  DatabaseSearchTool - retrieval Complete")
            return f"sql_query: {sql_query} response: {response}"
        
        except Exception as e:
            logger.error(f"[{datetime.now()}]  DatabaseSearchTool - Error in run Function: {e}")
            raise Exception(f"DatabaseSearchTool - Error in run Function")
    
    def configure_tool_schema(self, config = None):
        """
        This method is used to instantiate and set up the schema parameters for the tool.
        """
        self.args_schema = schema.DataBaseSearchInput()

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

        # # Concatenate intermediate steps from main agent and the tool (For old version of the tool where the tool was an agent)
        # steps = intermediate_steps_dict[self.name][step_index]
        # output = f"Main Agent Intermediate Step For {self.name}:\n{item}\n\n{self.name} Agent Intermediate steps\n:{steps}"

        # # Old version of the tool where the tool was an agent (updated)
        # # Construct the main agent steps from the AgentAction class in the agent reasoning steps tuple
        # main_agent_steps = f"Tool: {item[0].tool}\nTool Input: {item[0].tool_input}\nLog: {item[0].log}\nAction Output:\n{item[1]}"

        # # Concatenate intermediate steps from main agent and the tool
        # steps = intermediate_steps_dict[self.name][step_index]
        # tool_agent_steps = [f"Tool: {step[0].tool}\nTool Input: {step[0].tool_input}\nLog: {step[0].log}\nAction Output:\n{step[1]}" for step in steps]
        # tool_agent_steps = "\n\n".join(tool_agent_steps)

        # # Construct output string
        # output = f"Main Agent Intermediate Step For {self.name}:\n{main_agent_steps}\n\n{self.name} Agent Intermediate steps:\n{tool_agent_steps}"

        return output
    
    def generate_sql_database_filter(self, filter):
        """
        This method is used to generate filters for the tool.
        """
        return None
    
    def get_tables(self, query):
        """
        This method is used to get the tables used in the query.

        Args:
            query (str): The query to be executed.

        Returns:
            str: The tables used in the query.
        """
        # Get the template for the tables and set the prompt
        template = get_tables_template
        prompt = PromptTemplate(input_variables = ["input", "tables", "examples"], template = template)

        # Create the chain and invoke it
        chain = LLMChain(llm=database_search_llm, prompt=prompt)
        required_tables = chain.invoke({"input":query,"tables":tables,"examples":get_tables_examples})['text']

        # Set the delimiter and split the string to get the part after the delimiter
        delimiter = "Tables Used:"
        table_part = required_tables.split(delimiter)[1]
        table_part = table_part.strip()

        return table_part
    
    def get_sql_query(self, query, columns_list):
        """
        This method is used to get the SQL query for the given query and columns list.

        Args:
            query (str): The query to be executed.
            columns_list (list): The list of columns.

        Returns:
            str: The SQL query.
        """
        # Get the template for the SQL query and set the prompt
        template = get_sql_query_template
        prompt = PromptTemplate(input_variables = ["input", "data_structure", "examples"], template = template)

        # Create the chain and invoke it
        chain = LLMChain(llm=database_search_llm, prompt=prompt)
        sql_query_text = chain.invoke({"input":query,"data_structure":columns_list,"examples":get_sql_query_examples})['text']

        # Set the delimiter and split the string to get the part after the delimiter
        delimiter = "Final Answer:"
        sql_query = sql_query_text.split(delimiter)[1]
        sql_query = sql_query.strip()

        return sql_query