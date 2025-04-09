# Imports
import ast
import requests
import warnings
from datetime import datetime 
from typing import Optional
import re
import os

from googlesearch import search
from bs4 import BeautifulSoup 
from langchain_core.prompts import PromptTemplate
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

from app.irah.connections import LLM
from .. import schema
from app.irah.logs import logger
from ..prompt_templates.google_search_prompt_template import default_final_answer_format_top3titles, template_top3titles, default_final_answer_format_summary, template_summary


# Filter warnings
warnings.filterwarnings('ignore')


# Get environment variables
pause_seconds = int(os.getenv("ZZ_Pause_Seconds"))
successful_response_code = int(os.getenv("ZZ_Success_Status_Code"))
minimum_content_length = int(os.getenv("ZZ_Minimum_Content_Length"))
timeout_secs = int(os.getenv("ZZ_Timeout_Secs"))


class GoogleSearchTool(BaseTool):
    name = "GoogleSearchTool"
    description = ("Useful for searching google for current events, news, public concerns, and controversies surrounding a company and its operations. "
                   "The input to the tool should be a fully formed question (string).\n\n"
                   "This tool should be used when the question asks about current, recent, or unfolding events, such as new ESG initiatives, up-to-date controversies, "
                   "social impact projects, governance reforms, or the latest public opinions related to the company's ESG practices. " 
                   "It should also be used to when the question asked is related to public perception, media coverage, or topics that are discussed in real-time media, "
                   "such as legal disputes, social movements affecting the company, or publicized incidents of environmental harm.\n"
                   "Some examples of questions that this tool should be used to retrieve content for are: "
                   "Does Microsoft have ongoing concerns around bribery and fraud?\nWhat concerns are there around Tesla's governance structure?\n"
                   "Tell me about Nestle's water stress controversies.\nHas Delta Airlines faced any recent lawsuits related to environmental damage?\n"
                   "What are the recent developments in Johnson & Johnson's stance on animal testing?\nAre there any unfolding labour disputes or strikes at Nike?\n"
                   "Are there any breaking news on stories about Amazon's data privacy breach?\nWhat are the current market sentiments on Meta's risk management practices?\n\n"
                   "This tool should NOT be used for questions that require quantitative ESG data, such as specific emissions numbers or detailed energy usage, "
                   "as these are typically not available through news search results. "
                   "Do NOT use this tool for inquiries that call for historical financial data or in-depth analysis, as these provide a verified and "
                   "comprehensive record not usually captured by the latest news updates."
                   "DO NOT use this tool for questions unrelated to the description and examples provided above."
                   "DO NOT use this tool for general questions unrelated to the company's current events, news, public concerns, and controversies.")
    args_schema = schema.GoogleSearchInput
    
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> list:
        """
        Run the tool to search google for a query and return websites with relevant information to the query.
        """
        try:
            # Log initiation and process query
            logger.info(f"[{datetime.now()}]  GoogleSearchTool - retrieval initiated")
            search_results = self.process(query)

            # Log completion, and return results
            logger.info(f"[{datetime.now()}]  GoogleSearchTool - retrieval complete")
            return search_results
        except Exception as e:
            logger.error(f"[{datetime.now()}]  GoogleSearchTool - Error in run function: {e}")
            raise Exception("GoogleSearchTool - Retrieval Failed")
    
    def configure_tool_schema(self, config = None):
        """
        This method is used to instantiate and set up the schema parameters for the tool.
        """
        self.args_schema = schema.GoogleSearchInput()

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
        content = ast.literal_eval(item[1])
        #content = {"urls_retrieved": ast.literal_eval(item[1])}
        return content
    
    # Define methods for execution
    def remove_chars(self, input_str):
        """
        Removes specified characters ({, }, and :) from the input string.

        Parameters:
        input_str (str): The input string from which to remove characters.

        Returns:
        str: The input string with specified characters removed.
        """
        # Define the translation table
        translation_table = str.maketrans('', '', '{}:')

        # Use translate to remove specified characters
        result_str = input_str.translate(translation_table)

        return result_str 
    
    def remove_emojis(self,text):
        """
        Removes all emojis from the provided text.

        Emojis are identified by their Unicode character ranges, encompassing various symbols and pictographs,
        including but not limited to emoticons, transport and map symbols, enclosed alphanumeric characters,
        and many other emoji categories.

        Parameters:
        - text (str): The string from which emojis will be removed.

        Returns:
        - str: The text stripped of emojis.
        """
        # Unicode ranges that include emojis and some additional related characters
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)

        return emoji_pattern.sub(r'', text)
    
    def clean_text(self,inputstr):
        """
        Cleans the input text by performing specific substitutions and normalizations.

        This function modifies the input string in three ways:
        1. Removes all single quote characters.
        2. Replaces sequences of one or more whitespace characters (spaces, tabs, newlines, etc.)
        with a single space.
        3. Removes all emojis from the provided input string.

        Parameters:
        - inputstr (str): The string to be cleaned.

        Returns:
        - str: The cleaned version of the input string.
        """
        inputstr = inputstr.replace("'", "") 
        inputstr=re.sub(r'\s+', ' ', inputstr)
        cleaned_text=self.remove_emojis(inputstr)
        return cleaned_text
    

    def get_page_content(self, url):
        """
        Fetches the content of a web page at the specified URL.

        Parameters:
        url (str): The URL of the web page.

        Returns:
        bytes or None: The content of the web page, or None if an error occurs.
        """
        try:
            response = requests.get(url, verify=False, timeout=timeout_secs)
        except Exception as e:
            return None

        if response.status_code == successful_response_code:
            return response.content
        else:
            #print(f"Failed to fetch content. Status code: {response.status_code}")
            return None

    def parse_page_content(self, content):
        """
        Parses the content of a web page and extracts the title and meaningful contents.
        Parameters:
        content (bytes): The content of the web page as bytes.
        Returns:
        tuple: A tuple containing the title (str) and a list of meaningful contents (list of str).
        """
        try:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            # Extract title
            title = soup.title.text
            #remove single quotes from titles to avoid ast.literal_eval exceptions
            title = self.clean_text(title)
        except Exception as e:
            return '',''
        
        # Extract contents
        contents = []
        selected_tags = ['p','li', 'h2']
        for paragraph in soup.find_all(selected_tags):
            contents.append(paragraph.text)
        
        # Remove elements with length less than 20 to keep meaningful sentences, '\n' if it exists, and empty strings
        contents = list(set(item.strip('\n') for item in contents if len(item) >= minimum_content_length and item.strip()))
        contents = [self.remove_chars(item).strip() for item in contents]
        
        # Join content to one string
        contents = "\n".join(contents)
        contents = self.clean_text(contents)

        return title, contents

    def google_search(self, query, num_results):
        """
        Perform a Google search and return the results along with their URLs.

        :param query: The search query.
        :param num_results: Number of results to fetch (default is 5).
        :return: A list of dictionaries containing 'title' and 'url' for each result.
        """
        results = []

        # Using the googlesearch library to perform the search
        for result in search(query, num = num_results, stop = num_results, pause = pause_seconds):
            results.append(result)
        
        return results

    def scrape_titles_and_contents(self, urls):
        """
        Scrapes titles and contents from multiple URLs.
        Parameters:
        urls (list of str): A list of URLs to scrape.
        Returns:
        list of dict: A list of dictionaries, each containing the URL, title, and contents of a scraped page.
        """
        # Create empty list to store data
        try:
            results = []

            # Loop through URLs
            for url in urls:
                # Get the content of the current URL
                page_content = self.get_page_content(url)
                if page_content:
                    # Parse the content to extract title and contents
                    title, contents = self.parse_page_content(page_content)
                    # Append the results to the list
                    results.append({'url': url, 'title': title, 'contents': contents})
            
            return results
        except Exception as e:
            logger.error(f"[{datetime.now()}]  GoogleSearchTool - Error in scrape_titles_and_contents function: {e}")
            raise Exception(f"GoogleSearchTool - Error in scrape_titles_and_contents function")

    def get_most_relevant_titles(self, query, titles, num_results):
        """
        Generates a response for the most relevant titles based on a query and a list of titles.
        Parameters:
        query (str): The query for which most relevant titles are requested.
        titles (list of str): The list of titles to consider for relevance ranking.
        num_results (int): The number of most relevant titles to return. Default is 3.
        Returns:
        str: A response containing the most relevant titles based on the query.
        """
        try:

            # Create prompt and invoke response
            prompt1 = PromptTemplate.from_template(template = template_top3titles)
            multiple_input_prompt = prompt1.format(query = query, num_results = num_results, titles = titles, default_final_answer_format = default_final_answer_format_top3titles)
            response = LLM.invoke(input = multiple_input_prompt).content 

            return response
        except Exception as e:
            logger.error(f"[{datetime.now()}]  GoogleSearchTool - Error in get_most_relevant_titles function: {e}")
            raise Exception(f"GoogleSearchTool - Error in get_most_relevant_titles function")

    def find_urls(self, url_title_dict, top3titles):
        """
        Finds URLs associated with given titles from a dictionary of URL-title pairs.
        Parameters:
        url_title_dict (dict): A dictionary mapping URLs to their corresponding titles.
        top3titles (list of str): A list of titles for which URLs need to be found.
        Returns:
        list of str: A list of URLs associated with the given titles.
        """
        try:

            matching_urls = [url for url, title in url_title_dict.items() if title in top3titles]
            
            return matching_urls
        except Exception as e:
            logger.error(f"[{datetime.now()}]  GoogleSearchTool - Error in find_urls function: {e}")
            raise Exception(f"GoogleSearchTool - Error in find_urls function")


    def generate_summary(self,query, urls_and_titles_and_contents):
        """
        Generates a summary based on the given query and a list of dictionaries containing URLs, titles, and contents.

        Parameters:
        query (str): The query used to generate the summary.
        urls_and_titles_and_contents (list of dict): A list of dictionaries, each containing URL, title, and contents of a webpage.

        Returns:
        tuple: A tuple containing the generated summary (str) and the information used to generate it (str or list of str).
        """
        summary=''
        
        for item in urls_and_titles_and_contents:
            summary += f"{item['url']}   -  {item['title']}  - {item['contents']}\n"
        
        default_final_answer_format=default_final_answer_format_summary
        template1 = template_summary
        prompt_summary = PromptTemplate.from_template(template=template1)
        multiple_input_prompt_summary = prompt_summary.format(query=query, summary=summary,default_final_answer_format=default_final_answer_format)
        response = LLM.invoke(input = multiple_input_prompt_summary).content
        
        if "<INFORMATION USED>" in response:
            final_answer, information_used = response.split("<INFORMATION USED>")
            final_answer = final_answer.strip()
            information_used = information_used.strip()
        elif "Information Used:" in response:
            final_answer, information_used = response.split("URLs used:")
            final_answer = final_answer.replace("Information Used:", "")
            final_answer = final_answer.strip()
            information_used = information_used.strip()
        else:
            final_answer = response.strip()
            if("URLs used:" in final_answer):
                final_answer=response.split("URLs used:")[0]
                information_used = response.split("URLs used:")[1]
            else:
                information_used={"URLs used:":[]}
        
        return final_answer,information_used

    def process(self, query_to_search):
        """
        Processes a query by performing the following steps:
        1. Scraping titles using BeautifulSoup.
        2. Getting the most relevant titles from the given titles.
        3. Scraping titles and contents for the top 3 URLs.
        Moved this one 4. Generating a summary using OpenAI with the contents of the top 3 URLs.

        Parameters:
        query_to_search (str): The query to process.

        Returns:
        list of dict: A list of dictionaries containing the summary and URLs used.
        """
        try:
            search_results = self.google_search(query_to_search, num_results = self.args_schema.total_retrievals)

            # Step 1: Scraping titles using BeautifulSoup
            titles = [self.parse_page_content(self.get_page_content(result))[0] for result in search_results]
            
            titles = [title.strip() for title in titles]
            
            url_title_dict = dict(zip(search_results, titles))

            ## Remove entries with null or empty titles
            url_title_dict = {url: title for url, title in url_title_dict.items() if title is not None and title != ''}

            #Step 2 : Get most relevant titles from given titles.
            top_3_titles = self.get_most_relevant_titles(query_to_search, titles, num_results = self.args_schema.relevant_retrievals)
            top_3_titles = top_3_titles.split('Titles:')[1].strip()  
            top_3_titles = ast.literal_eval(top_3_titles)

            # corresponding urls of top3titles
            top_3_urls = self.find_urls(url_title_dict, top_3_titles)

            # Step 3: Scraping titles and contents using BeautifulSoup for the top 3 URLs
            top_3_results = self.scrape_titles_and_contents(top_3_urls)

            # # Step 4: Generate a summary using OpenAI with the contents of the top 3 URLs
            # summary,URLs_used = self.generate_summary(query_to_search, top_3_results)
            # doc = {}
            # doc['Summary']=summary
            # doc['URLs_used']=URLs_used
            # relevent_docs.append(doc)
            # resultDict={"content_retrieved":top_3_results}
            
            return f"{top_3_results}"
        except Exception as e:
            logger.error(f"[{datetime.now()}]  GoogleSearchTool - Error in Process function: {e}")
            raise Exception(f"GoogleSearchTool - Error in Process function")