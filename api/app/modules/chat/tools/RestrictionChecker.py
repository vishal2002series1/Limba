# Imports
import time
from datetime import datetime

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback

from app.irah.connections import restriction_checker_llm
from app.modules.chat.schema import response_schema
from ..prompt_templates.restriction_checker_prompt_template import restriction_dictionary, restriction_checker_template
from app.irah.logs import logger

# Create restriction checker class
class RestrictionChecker:
    name = "Restriction Checker"
    description = "Check if any query is restricted. Restrictions can be based on category to which query belongs (e.g. Personal Identifiable Information, Investment recommendation, etc.)"

    def __init__(self, llm=restriction_checker_llm, categories_to_include=None, 
                 restriction_checker_template: str = restriction_checker_template, restriction_dictionary: dict = restriction_dictionary):
        """
        This method sets up defining LLM.
        
        Arg(s):
            llm: large language model to use.
            categories_to_include: a list of categories to include in the checker. For example ["1", "2"]. The default is None which uses all categories.
            restriction_checker_template: template for the restriction checker.
            restriction_dictionary: a dictionary containing information on all the restrictions we have.
        """
        self.template = restriction_checker_template
        self.restriction_dictionary = restriction_dictionary
        self.restrictions_string = self.__build_restrictions_string(categories_to_include)

        # Set LLM
        try:
            self.llm = llm
        except Exception as e:
            raise ValueError('RestrictionChecker not properly called !!!')

    def __build_restrictions_string(self, categories_to_include=None):
        """
        This method is used to build the restriction string to be passed into the LLM chain.

        Arg(s):
            categories_to_include: list = a list of categories to consider. Default is None in which case we use all categories.
        
        Output:
            a string containing the restrictions for the prompt to check.
        """
        # Get categories to use
        if categories_to_include:
            dictionary_to_use = {key: self.restriction_dictionary[key] for key in categories_to_include}
        else:
            dictionary_to_use = self.restriction_dictionary

        # Set counter string
        output_string = ""

        # Loop through dictionary to build string
        for number, dictionary in dictionary_to_use.items():
            output_string += f'{number}. {dictionary["Category"].strip()}: {dictionary["Description"].strip()}. For example, "{dictionary["Example"]}".\n'
        
        return output_string

    def build_response(self, item, cb, agent_response_time, llm):
        """
        Modifying result to fit response schema.
        """
        try:
            logger.info(f"[{datetime.now()}]  RestrictionCheckerTool - Build Response Started")
            # Define response schema
            res = {
                "question": "", "response": "", "annotations": {}, 
                "tools": {}, "system_metrics": {"llm_metric": {}}
            }

            # Get question for response
            res['question'] = str(item['input'])

            # Set storage
            answer_list = []
            category_list = []

            # Get LLM answer as a list of categories and loop through
            for category_number in [answer.strip() for answer in item["text"].strip().split(",")]:
                # If the category number is in the dictionary append answers and categories to storage
                if category_number in self.restriction_dictionary:
                    answer_list.append(self.restriction_dictionary[category_number]["Response"])
                    category_list.append(self.restriction_dictionary[category_number]["Category"])
            
            # If storage containers are not empty, get the restriction response, category, and response type for annotations
            if answer_list:
                res['response'] = "\n".join(answer_list)
                question_category = "\n".join(category_list)
                response_type = 1
            # Else, there is no restriction
            else:
                res['response'] = "No restrictions identified, proceed to the next step."
                question_category = "No Restrictions"
                response_type = 0

            # Add annotations
            res['annotations']['RestrictionChecker'] = {'response_type': response_type, 'question_category': question_category}

            # Build response for system metrics
            llm_usage_metrics = {
                'total_tokens': cb.total_tokens,
                'prompt_tokens': cb.prompt_tokens,
                'completion_tokens': cb.completion_tokens,
                'total_cost': cb.total_cost,
                'successful_requests': cb.successful_requests,
                'llm_model_name': llm.deployment_name,
                'temperature': llm.temperature
            }
            res['system_metrics']['llm_usage_metrics'] = llm_usage_metrics
            res['system_metrics']['agent_response_time'] = agent_response_time
            res['system_metrics']['agent_reasoning_steps'] = []

            logger.info(f"[{datetime.now()}]  RestrictionCheckerTool - Build Response Complete")

            return response_schema.ResponseSchema(**res, exclude_unset=True, exclude_none=True)
        except Exception as e:
            logger.error(f"[{datetime.now()}]  RestrictionCheckerTool - Error in RestrictionCheckerTool build_response: {e}")
            raise Exception("RestrictionCheckerTool - error in RestrictionCheckerTool build_response")
    
    def execute_restriction_checker(self, question):
        """
        This method is used to prompt for checking negative cases and get the response.

        Arg(s):
            question: str = The question asked by an end user.
        
        Output:
            Response as in the checker response schema.
        """
        try:
            logger.info(f"[{datetime.now()}]  RestrictionCheckerTool - Check Start")
            # Building chain for executing prompt
            prompt = PromptTemplate.from_template(template=self.template)
            chain = LLMChain(llm=self.llm, prompt=prompt)

            # Set timers and invoke response
            start_time = time.time()
            with get_openai_callback() as cb:
                response = chain.invoke({"input": question, "restrictions_string": self.restrictions_string})
            end_time = time.time()
            agent_response_time = round(end_time - start_time)

            # Build response
            result = self.build_response(response, cb, agent_response_time, self.llm)

            logger.info(f"[{datetime.now()}]  RestrictionCheckerTool - Check Complete")

            return result
        except Exception as e:
            logger.error(f"[{datetime.now()}]  RestrictionCheckerTool - Error in RestrictionCheckerTool: {e}")
            raise Exception("RestrictionCheckerTool - error in RestrictionCheckerTool")

