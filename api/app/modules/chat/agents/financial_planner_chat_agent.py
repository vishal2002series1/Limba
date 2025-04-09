# Imports
import json
import time
from datetime import datetime

from langchain.agents import AgentExecutor
from langchain_community.callbacks import get_openai_callback  
######## Deprecated Modules ###########
from langchain.chains import LLMChain
from langchain.agents.chat.base import ChatAgent
########################################

from .. import schema
from ..tools.FinancialPlannerTool import planner_tools, create_plan
from ..prompt_templates.financial_planner_prompt_templates import HUMAN_MESSAGE, SYSTEM_MESSAGE_PREFIX_CHAT_AGENT, SYSTEM_MESSAGE_SUFFIX_CHAT_AGENT
from app.irah.logs import logger
from app.modules.logs.actions import create_log_financial_planner
from app.modules.logs.schema import LogFinancialPlannerRequest


# Define Financial Planner Chat Agent class
class FinancialPlannerChatAgent:
    # Initialise response and set all available tools
    res = {
        "question": "", "response": "", "annotations": {},
        "tools": {}, "system_metrics": {}
    }
    # For the financial planner chat agent, get all the planner tools except the first one (the client data reader tool)
    financial_planner_tools = planner_tools[1:]
    financial_planner_tools_dict = {tool_instance.name: tool_instance for tool_instance in planner_tools[1:]}


    def __init__(self, llm, req, prompt = None):
        """
        Initialise the variables for the class.

        Arg(s):
            llm = Large language model to use for the agent.
            req = Request parameters to use for the instance. Should follow the request schema.
            prompt = Prompt to use for the agent. Default is None in which case it uses the default template to create the prompt.
        """
        try:
            # Initialise request variables
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Inside Constructor")
            self.request = req
            self.query = req.question
            self.client_name = req.client_name
            self.client_data = self.get_client_data(self.client_name)

            # If LLM is given, initialise LLM, set up the prompt
            if llm is not None:
                self.llm = llm
                self.__setup_prompt(prompt)
            else:
                raise ValueError('Model Not provided')
            
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in __init__: {e}")
            raise ValueError('FinancialPlannerChatAgent not properly called !!!')
        

    def get_client_data(self, client_name: str) -> str:
        """
        Get the client data for the given client name.

        Arg(s):
            client_name = Name of the client for which the data is needed.

        Returns:
            JSON string of the client data.
        """
        try:
            # Log start
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Retrieving client data for {client_name}")

            # # Load data
            # with open('app/store/metadata/financial_planner_user_profile.json', 'r') as f:
            #     all_clients = json.load(f)
            
            # # Clean / strip input and get data
            # client_name = str(client_name.strip())
            # client_data = [client for client in all_clients if client['client_data']['name']==client_name][0]

            # Get initial client data from request
            client_data = self.request.client_data

            # Calculate initial annual savings from retirement accounts
            annual_savings = sum(account['contribution'] for account in client_data['client_data']['retirement_accounts'])

            # Calculate annual savings growth as average of growth rates in retirement accounts
            annual_savings_growth = sum(account['annual_growth'] for account in client_data['client_data']['retirement_accounts']) / len(client_data['client_data']['retirement_accounts'])

            # Get output data: all the underlying data and intermediate data calculations
            output_data = json.dumps({
                'client_data': client_data['client_data'],
                'annual_savings': annual_savings,
                'annual_savings_growth': annual_savings_growth
            })

            # Log end
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Client data retrieved successfully")

            return f"{output_data}"
        
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in reading client data: {e}")
            raise ValueError(f"Error in reading client run: {e}")  
    

    def __setup_prompt(self, prompt):
        """
        Set up the prompt for the agent.

        Arg(s):
            prompt = Prompt to use for the instance. Default is None in which case it uses the default template to create the prompt.
        """
        try:
            # If prompt is not given, create the default prompt
            if prompt is None:
                logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Inside __setup_prompt")
                self.prompt = ChatAgent.create_prompt(
                    self.financial_planner_tools,
                    system_message_prefix = SYSTEM_MESSAGE_PREFIX_CHAT_AGENT,
                    system_message_suffix = SYSTEM_MESSAGE_SUFFIX_CHAT_AGENT,
                    human_message = HUMAN_MESSAGE,
                    input_variables=["input", "agent_scratchpad", "tools", "tool_names", "client_name", "client_data"]
                    )
            else:
                self.prompt = prompt
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in __setup_prompt: {e}")
            raise ValueError('FinancialPlannerChatAgent - Error in __setup_prompt')
        
    
    def get_tool_intermediate_steps(self, item):
        """
        This method is used to get the tool's portion of the intermediate steps from the agent.
        """
        try:
            # Construct the output from the AgentAction class in the agent reasoning steps tuple for the system metric agent reasoning steps
            x = f"Tool: {item[0].tool}\nTool Input: {item[0].tool_input}\nLog: {item[0].log}\nAction Output:\n{item[1]}"

            # Contruct the output from the AgentAction class in the agent reasoning steps tuple for the annotations
            y = f"**Tool:** {item[0].tool}\n**Input:** {item[0].tool_input}\n**Output:** {item[1].strip()}"

            # Get final output as tuple
            output = (x, y)

        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in get_tool_intermediate_steps: {e}")
            raise ValueError(f"FinancialPlannerChatAgent - Error in get_tool_intermediate_steps\n{e}")
        
        return output  
    

    def build_solution_plan(self):
        """
        Build the solution plan for the agent.

        Returns:
            The solution plan for the agent.
        """
        try:
            # Log start
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Building solution plan")

            # Create solution plan
            create_solution_plan = create_plan(self.query, self.financial_planner_tools)
            solution_plan = self.llm.invoke(create_solution_plan).content

            # Log end
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Solution plan built successfully")
            return solution_plan
        
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in build_solution_plan: {e}")
            raise ValueError('FinancialPlannerChatAgent - Error in build_solution_plan')
        
    
    def build_response(self, item, cb, agent_response_time, llm):
        """
        This method is used to build the response for the agent results.

        Arg(s):
            item = Result of the agent execution.
            cb = OpenAI callback data for the execution.
            agent_response_time = Time taken for the execution.
            llm = Large language model used for the execution.
        """
        try:
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Started Building response")
            # Get response question
            self.res['question'] = item['input']

            # Get final answer and annotations
            self.res['response'] = item['output']
            self.res["annotations"] = {"solution_plan": item['solution_plan']}

            # If response was due to agent timeout, set response as unable to answer
            if self.res['response'] == "Agent stopped due to iteration limit or time limit.":
                self.res['response'] = "I do not have the capacity to answer your question. Could you please try rephrasing the question?"

            # Build response for system metrics
            llm_usage_metrics = {}
            llm_usage_metrics['total_tokens'] = cb.total_tokens
            llm_usage_metrics['prompt_tokens'] = cb.prompt_tokens
            llm_usage_metrics['completion_tokens'] = cb.completion_tokens
            llm_usage_metrics['total_cost'] = cb.total_cost
            llm_usage_metrics['successful_requests'] = cb.successful_requests
            llm_usage_metrics['llm_model_name'] = llm.deployment_name
            llm_usage_metrics['temperature'] = llm.temperature
            self.res['system_metrics']['llm_usage_metrics'] = llm_usage_metrics
            self.res['system_metrics']['agent_response_time'] = agent_response_time
            self.res['system_metrics']['agent_reasoning_steps'] = []

            # Build response for intermediate steps
            annotation_reasoning_steps = []

            ## Loop through intermediate steps
            for intermediate_steps in item['intermediate_steps']:
                if (tool_name := intermediate_steps[0].tool) in self.financial_planner_tools_dict.keys():
                    ## Get intermediate steps for the tool
                    step_to_append = self.get_tool_intermediate_steps(intermediate_steps)

                    ## Append to agent reasoning steps for the main agent and to the annotations
                    self.res['system_metrics']['agent_reasoning_steps'].append(step_to_append[0])
                    annotation_reasoning_steps.append(step_to_append[1])

                if self.res["tools"]:
                    if tool_name in self.res["tools"].keys():
                        self.res["tools"][tool_name].append({"input": intermediate_steps[0].tool_input, "output": intermediate_steps[1]})

                    else:
                        self.res["tools"][tool_name] = [{"input": intermediate_steps[0].tool_input, "output": intermediate_steps[1]}]

                else:
                    self.res["tools"][tool_name] = [{"input": intermediate_steps[0].tool_input, "output": intermediate_steps[1]}]

            ## Add extra information to annotations
            self.res['annotations']['reasoning_steps'] = "\n\n".join(annotation_reasoning_steps)
            
            # Log end and return response
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Completed Building Response")

            return schema.FinancialPlannerResponseSchema(**self.res, exclude_unset=True, exclude_none=True)
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - error Build Response: {e}")
            raise Exception(f"FinancialPlannerChatAgent Error in building Response")
        

    def execute_chat(self):
        """
        Execute the chat agent.

        Returns:
            The response from the chat agent.
        """
        try:
            # Log start and start time
            start_time = time.time()
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Executing chat agent")

            # Create chain and agent
            llm_chain = LLMChain(llm = self.llm, prompt = self.prompt)
            agent = ChatAgent(llm_chain = llm_chain, tools = self.financial_planner_tools)

            # Create solution plan
            solution_plan = self.build_solution_plan()

            # Create planner agent and invoke
            planner_agent = AgentExecutor(agent = agent, tools = self.financial_planner_tools, verbose = True, return_intermediate_steps = True, 
                                          handle_parsing_errors = True, debug = True, return_source_documents = True)
            with get_openai_callback() as cb:
                response = planner_agent.invoke({"input": self.query, "client_name": self.client_name, "client_data": self.client_data, "solution_plan": solution_plan})

            # Get end time and agent response time
            end_time = time.time()
            agent_response_time = round(end_time - start_time)

            # Build response and dump to log
            result = self.build_response(response, cb, agent_response_time, self.llm)
            item = result.model_dump()

            ## Log the response
            log_res = create_log_financial_planner(LogFinancialPlannerRequest(**item))
            logger.info(f"[{datetime.now()}]  FinancialPlannerChatAgent - Chat agent executed successfully")

            return result
        
        except Exception as e:
            logger.error(f"[{datetime.now()}]  FinancialPlannerChatAgent - Error in execute_chat: {e}")
            raise ValueError('FinancialPlannerChatAgent - Error in execute_chat')