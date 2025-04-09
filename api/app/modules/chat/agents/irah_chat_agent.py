# Imports
import time
from datetime import datetime

from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate

from .. import schema
from app.modules.logs.actions import create_log
from app.modules.logs.schema import LogRequest
from app.modules.chat.tools.available_tools_repo import all_available_tools
from app.modules.chat.prompt_templates.agent_prompt_templates import template
from app.modules.chat.tools.RestrictionChecker import RestrictionChecker
from ..endpoint_configurations.default_config import default_examples, default_prefix_message, default_final_answer_format, default_annotations_cleaner, default_unable_to_answer, default_final_answer_parser
from app.irah.logs import logger


# Main chat agent class for IRAH
class IRAHChatAgent:
    # Initialise response and set all available tools
    res = {
        "question": "", "response": "", "annotations": {},
        "tools": {}, "system_metrics": {}
    }
    all_available_tools = all_available_tools
    tool_intermediate_steps_dict = {}

    def __init__(self, llm, req, final_answer_parser_func=default_final_answer_parser, final_annotations_cleaner=default_annotations_cleaner, prompt=None):
        """
        Initialise the variables for the class.

        Arg(s):
            llm = Large language model to use for the agent.
            req = Request parameters to use for the instance. Should follow the request schema.
            prompt = Prompt to use for the agent. Default is None in which case it uses the default template to create the prompt.
        """
        try:
            # Initialise final answer parser
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - Inside Constructor")
            self.final_answer_parser = final_answer_parser_func
            self.final_annotations_cleaner = final_annotations_cleaner
            self.request = req

            # If LLM is given, initialise LLM, set up the tools with the request parameter and set prompt
            if llm is not None:
                self.llm = llm
                self.__setup_tools(req)
                self.__setup_prompt(prompt)
            else:
                raise ValueError('Model Not provided')
        except Exception as e:
            logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error in __init__: {e}")
            raise ValueError('IRAHChatAgent not properly called !!!')

    def __setup_prompt(self, prompt):
        """
        This method sets up the prompt. If prompt is not passed during initialization, we use the default one.
        """
        try:
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - Setting up prompt Started")
            if prompt is not None:
                self.prompt = prompt
            else:
                # Set prompt
                prompt = PromptTemplate(
                    input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools', 'examples', 'custom_prefix_message', 'final_answer_format', 'unable_to_answer'],
                    template=template
                )
                self.prompt = prompt
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - Setting up prompt Completed")
        except Exception as e:
            logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error Setup prompt: {e}")
            raise Exception(f"IRAHChatAgent Error in setting up prompt")


    def __setup_tools(self, req):
        """
        This method sets up the tools to use for a particular instance. If no particular tools are given in the response, we use all available tools.
        """
        # Set container for tools
        try:
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - setting up tools Started")
            tools = []

            # If tools are given in the request, use the parameters to configure the tools
            if req.tools is not None:
                # Get the tools to use dictionary from the request
                tools_to_use = req.tools.model_dump(exclude_none=True)

                # Loop through the tools keys and use them to get the tool instances from the available tools
                for tool_key in tools_to_use.keys():
                    if tool_key in self.all_available_tools.keys():
                        # Get tool instance, configure and append
                        current_tool_instance = self.all_available_tools[f'{tool_key}']
                        current_tool_instance.configure_tool_schema(req.tools.model_dump()[f"{tool_key}"])
                        tools.append(current_tool_instance)

                        # Get tool configuration for response output
                        self.res["tools"][tool_key] = current_tool_instance.get_tool_config_for_response()
                    else:
                        raise Exception("Tool being called is not available in the tool inventory. Please check to make sure tool is available and/or spelled correctly.")

            # if no tools are given, use all available tools
            else:
                for tool_key, current_tool_instance in self.all_available_tools.items():
                    # Configure schema and then append
                    current_tool_instance.configure_tool_schema()
                    tools.append(current_tool_instance)

                    # Get tool configuration for response output
                    self.res["tools"][tool_key] = current_tool_instance.get_tool_config_for_response()

            # Add tools list to class attributes
            self.tools = tools
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - tools being set up for use: {tools}")
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - setting up tools completed")
        except Exception as e:
            logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error in Setting up Tools: {e}")
            raise Exception(f"IRAHChatAgent Error in setting up tools")

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
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - Started Building response")
            # Get response question
            self.res['question'] = item['input']

            # Build response using output parser
            self.res['response'], self.res["annotations"] = self.final_answer_parser(item['output'])

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
            ## Create empty dictionary to store index per tool used in the main agent
            tools_idx = {}

            ## Loop through intermediate steps
            for intermediate_steps in item['intermediate_steps']:
                if (tool_name := intermediate_steps[0].tool) in self.all_available_tools.keys():
                    current_tool = self.all_available_tools[tool_name]
                    # self.res["tools"][tool_name] = current_tool.get_tool_config_for_response()
                    # print(f"Tool config:", {tool_name: self.res["tools"][tool_name]})

                    ## Get counter for tool and append to tools index dictionary
                    if tool_name in tools_idx:
                        tools_idx[tool_name] = tools_idx[tool_name] + 1
                    else:
                        tools_idx[tool_name] = 0
                    
                    ## Append to reasoning steps for the main agent
                    step_to_append = str(current_tool.get_tool_intermediate_steps(intermediate_steps, self.tool_intermediate_steps_dict, tools_idx[tool_name]))
                    self.res['system_metrics']['agent_reasoning_steps'].append(step_to_append)
                    
                    ## Edge case of getting retrieved contents from intermediate response for ContentSearchTool and GoogleSearchTool
                    if tool_name.strip() in ["ContentSearchTool", "GoogleSearchTool"]:
                        self.res['annotations'][tool_name]['content_retrieved'].extend(current_tool.get_tool_intermediate_content(intermediate_steps))
                        
            # Clean annotations and log
            self.res["annotations"] = self.final_annotations_cleaner(self.res["annotations"].copy())
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - Completed Building Response")

            return schema.ResponseSchema(**self.res, exclude_unset=True, exclude_none=True)
        except Exception as e:
            logger.error(f"[{datetime.now()}]  IRAHChatAgent - error Build Response: {e}")
            raise Exception(f"IRAHChatAgent Error in building Response")
        
    

    def execute_chat(self, custom_prefix_message: str = default_prefix_message, examples: str = default_examples,
                     unable_to_answer: str = default_unable_to_answer, final_answer_format: str = default_final_answer_format):
        """
        This method is used to execute the agent and get the response.

        Arg(s):
            restriction_flag: bool = Indicator for adding restriction checks to the execution. Default is True.
            custom_prefix_message: str = Customisable message to give context to the prompt. This can be changed per endpoint.
            unable_to_answer: str = Custom response to use when the agent is unable to answer a question. This can be changed per endpoint.
            final_answer_format: str = Custom final answer format that can also be changed per endpoint.

        Output:
            Agent response as in the response schema.
        """
        try:
            # Log invocation and get query from request
            logger.info(f"[{datetime.now()}]  IRAHChatAgent - execute_chat function invoked")
            query = self.request.question

            # If query needs to be checked for restrictions based on flag
            if self.request.restriction is not None:
                try:
                    logger.info(f"[{datetime.now()}]  IRAHChatAgent - Calling Restriction checker")
                    restriction_response = RestrictionChecker(categories_to_include=self.request.model_dump()['restriction']['categories']).execute_restriction_checker(question=query)

                    # If query is restricted, set result as response and log response using dictionary
                    if (restriction_response_dict := restriction_response.model_dump())["annotations"]["RestrictionChecker"]["response_type"] == 1:
                        # Log result using response dictionary and return response schema object
                        logger.info(f"[{datetime.now()}]  IRAHChatAgent - Restricted Query Detected")
                        log_res = create_log(LogRequest(**restriction_response_dict))
                        return restriction_response
                    else:
                        logger.info(f"[{datetime.now()}]  IRAHChatAgent - Query is not restricted")
                except Exception as e:
                    logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error in Restriction Checker: {e}")
                    raise Exception(f"IRAHChatAgent Error in Restriction Checker")

            try:
                # Create react agent and executor
                agent = create_react_agent(self.llm, self.tools, self.prompt)
                executor = AgentExecutor(agent=agent, tools=self.tools, return_intermediate_steps=True, verbose=True,
                                         handle_parsing_errors=True, debug=True, return_source_documents=True, max_iterations=5)

                # Set timers and invoke response
                start_time = time.time()
                with get_openai_callback() as cb:
                    logger.info(f"[{datetime.now()}]  IRAHChatAgent - Main Agent Execution Started")
                    response = executor.invoke({"input": query, "examples": examples, "custom_prefix_message": custom_prefix_message,
                                                "unable_to_answer": unable_to_answer, "final_answer_format": final_answer_format})
                    logger.info(f"[{datetime.now()}]  IRAHChatAgent - Main Agent Execution Completed")
                end_time = time.time()
                agent_response_time = round(end_time - start_time)

                # Build response and dump into the log
                result = self.build_response(response, cb, agent_response_time, self.llm)
                item = result.model_dump()

                log_res = create_log(LogRequest(**item))
                logger.info(f"[{datetime.now()}]  IRAHChatAgent - execute_chat function completed")
                return result
            except Exception as e:
                logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error in Execute Chat Main Agent: {e}")
                raise Exception(f"Error in Execute Chat Function")
        except Exception as e:
            logger.error(f"[{datetime.now()}]  IRAHChatAgent - Error in execute_chat: {e}")
            raise Exception(f"Error in execute_chat")
