import os
from app.irah.logs import logger

custom_req_config = {
  "question": "",
  "tools": {
    "ContentSearchTool": {
      "query": "string",
      "filters": {},
      "search_type": "hybrid",
      "content_retrieved": os.getenv("ZZ_DEFAULT_CONTENT_RETRIEVED")
    },
    "DatabaseSearchTool": {
      "query": "string",
      "filters": {}
    },
    "FinancialPlannerTool": {
      "query": "string",
      "client_name": "string"
    }
  },
  "restriction": {
    "categories": [
      "1",
      "2",
      "3"
    ]
  }
}


# Define default prompt arguments
## Define default prefix message to add to the prompt for context. This can be changed per endpoint
default_prefix_message = """You are an expert level assistant to financial advisors and analysts that helps them answer questions about their clients and financial services.
Your task is to provide the financial advisors and analysts with detailed and descriptive answers to the question: "{input}" by using the provided tools to retrieve relevant information that will help you answer the question(s).
"""

## Define default final answer format
default_final_answer_format = """The Final Answer format should ALWAYS be as referenced below.
Final Answer: ...

<INFORMATION USED>
Documents used: [content_id1, content_id2, ....]
SQL Query used: [SELECT * FROM table1 where....., SELECT * from table2 where...., ...]
URLs used: [url1, url2, ....]


**NOTE: Irrespective of the tools used the output should contain both "Documents used: [...]" and "SQL Query used: [...]" in the format given above. It should also contain "Final Answer: " and the delimeter "<INFORMATION USED>"**
Documents used should be a list of the content_id of ONLY the documents in where you found the answer from the ContentSearchTool.
SQL Query used should be a list of the SQL queries used to get the response from the DatabaseSearchTool.
URLs used should be a list of ONLY the urls used to get the response from the GoogleSearchTool.
"""

# Examples for the main agent prompt template
default_examples = """
Example 1:
Question: What are the top 3 priorities for company X in 2023?
Thought: To answer this question, I need to use the ContentSearchTool to retrieve the relevant information.
Action: ContentSearchTool
Action Input: company X 2023 priorities
Observation: The tool returned a list of documents that contain the top 3 priorities for company X in 2023.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: The top 3 priorities for company X in 2023 are...

<INFORMATION USED>
Documents used: [content_id1, content_id2]
SQL Query used: []
URLs used: []


Example 2:
Question: Summarise the notes from the last meeting with Paul Benson
Thought: To answer this question, I need to use the DatabaseSearchTool to retrieve the relevant information.
Action: DatabaseSearchTool
Action Input: last meeting notes with Paul Benson
Observation: The tool returned a list of structured data that contain information on the notes from the last meeting with Paul Benson.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: Summary of the notes from the last meeting with Paul Benson...

<INFORMATION USED>
Documents used: []
SQL Query used: [SELECT * FROM table1 where....., SELECT * from table2 where....]
URLs used: []


Example 3:
Question: What recent climate change controversies is the Eastman Kodak facing?
Thought: To answer this question, I need to use the GoogleSearchTool to retrieve the relevant information.
Action: GoogleSearchTool
Action Input: Eastman Kodak climate change controversies
Observation: The tool returned a list of content that contain information on the recent climate change controversies Eastman Kodak is facing.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: Eastman Kodak is facing the following recent climate change controversies...

<INFORMATION USED>
Documents used: []
SQL Query used: []
URLs used: [url1, url2]


Example 4:
Question: Have any clients added beneficiaries and what is the process for opening a trust with our firm?
Thought: To answer the first part of the question, I need to use the DatabaseSearchTool to retrieve the relevant information. For the second part of the question, I need to use the ContentSearchTool.
Action: DatabaseSearchTool
Action Input: clients who recently added beneficiaries
Observation: The tool returned a list of structured data that contain information on clients who recently added beneficiaries.
Thought: I have the information needed to answer the first part of the question. Now, I need to use the ContentSearchTool to answer the second part of the question.
Action: ContentSearchTool
Action Input: process for opening a trust with our firm
Observation: The tool returned a list of documents that contain the process for opening a trust with our firm.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: The clients who recently added beneficiaries are...

<INFORMATION USED>
Documents used: [content_id1, content_id2]
SQL Query used: [SELECT * FROM table1 where....., SELECT * from table2 where....]
URLs used: []


Example 5:
Question: Who is the CFO of Boeing and what recent controversies is the company facing?
Thought: To answer the first part of the question, I need to use the ContentSearchTool to retrieve the relevant information. For the second part of the question, I need to use the GoogleSearchTool.
Action: ContentSearchTool
Action Input: CFO of Boeing
Observation: The tool returned a list of documents that contain information on the CFo of Boeing.
Thought: I have the information needed to answer the first part of the question. Now, I need to use the GoogleSearchTool to answer the second part of the question.
Action: GoogleSearchTool
Action Input: Boeing recent controversies
Observation: The tool returned a list of content that contain the Boeing's recent controversies.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: The CFO of Boeing is...

<INFORMATION USED>
Documents used: [content_id1, content_id2]
SQL Query used: []
URLs used: [url1, url2]


Example 6:
Question: Compare the Q1 2023 earnings call results from American Airlines, Delta Airlines and JetBlue Airlines. 
Thought: To answer this question, I need to use the ContentSearchTool to retrieve the relevant information for all companies.
Action: ContentSearchTool
Action Input: American Airline's Q1 2023 earnings call results
Observation: The tool returned a list of documents that contain the American Airline's Q1 2023 earnings call results.
Thought: I have the information needed for American Airlines. Now, I need to use the ContentSearchTool to retrieve the relevant information for Delta Airlines and JetBlue Airlines.
Action: ContentSearchTool
Action Input: Delta Airline's Q1 2023 earnings call results
Observation: The tool returned a list of documents that contain Delta Airline's Q1 2023 earnings call results.
Thought: I have the information needed for Delta Airlines. Now, I need to use the ContentSearchTool to retrieve the relevant information for JetBlue Airlines.
Action: ContentSearchTool
Action Input: JetBlue Airline's Q1 2023 earnings call results
Observation: The tool returned a list of documents that contain JetBlue Airline's Q1 2023 earnings call results.
Final Thought: I now have the required information to derive a Final Answer
Final Answer: Comparing the Q1 2023 earnings call results from American Airlines, Delta Airlines, and JetBlue Airlines, the results are as follows...

<INFORMATION USED>
Documents used: [content_id1, content_id2]
SQL Query used: []
URLs used: []

"""

## Default response to use when the system is unable to answer
default_unable_to_answer = """I do not have the required information to answer your question. Could you please try rephrasing the question?"""

# Define default final answer parser
def default_final_answer_parser(final_answer_string: str):
    """
    This function is used to parse the final answer for the response.

    Arg(s):
        final_answer_string: str = Final answer string from the agent.

    Output:
        Returns a tuple with the actual final answer and the information used.
    """
    # Set default info used dictionary output
    info_used_output = {"ContentSearchTool": {"content_used": [], "content_retrieved": []}, 
                        "DatabaseSearchTool": {"sql_query": []}, "GoogleSearchTool": {"urls_used": [], "content_retrieved": []}}

    try:
        # Check if information used exists in answer
        if (info_used_flag := "<INFORMATION USED>") in final_answer_string:
            # Split final answer into response and information used then strip
            final_answer, information_used = final_answer_string.split(info_used_flag)
            final_answer = final_answer.strip()
            information_used = information_used.strip()

            # Check if information used is empty
            if not information_used:
                if (docs_used_flag := "Documents used:") in final_answer_string:
                    final_answer, information_used = final_answer.split(docs_used_flag)
                    final_answer = final_answer.strip()
                    information_used = docs_used_flag + information_used
                    
                elif (sql_query_used_flag := "SQL Query used:") in final_answer_string:
                    final_answer, information_used = final_answer.split(sql_query_used_flag)
                    final_answer = final_answer.strip()
                    information_used = sql_query_used_flag + information_used

                elif (urls_used_flag := "URLs used:") in final_answer:
                    final_answer, information_used = final_answer.split(urls_used_flag)
                    final_answer = final_answer.strip()
                    information_used = urls_used_flag + information_used

        elif (docs_used_flag := "Documents used:") in final_answer_string:
            # Split on info_used
            final_answer, information_used = final_answer_string.split(docs_used_flag)
            final_answer = final_answer.strip()
            information_used = docs_used_flag + information_used

        elif (sql_query_used_flag := "SQL Query used:") in final_answer_string:
            # Split on info_used
            final_answer, information_used = final_answer_string.split(sql_query_used_flag)
            final_answer = final_answer.strip()
            information_used = sql_query_used_flag + information_used

        elif (urls_used_flag := "URLs used:") in final_answer_string:
          # Split on info_used
          final_answer, information_used = final_answer_string.split(urls_used_flag)
          final_answer = final_answer.strip()
          information_used = urls_used_flag + information_used
     
        else:
            # Strip final answer string and return
            final_answer = final_answer_string.strip()
            return final_answer, info_used_output

        # Parse through information used
        if "Documents used:" in information_used:
            # Get content used and sql query used
            content_used = information_used.split("Documents used:")[1].strip().split("SQL Query used:")[0].strip().replace("[","").replace("]","").replace(" ", "").replace("'","").replace('"',"")
            if (not content_used.strip()) or (content_used.strip().lower() == "none"):
                content_used = []
            else:
                content_used = list(content_used.split(','))
            info_used_output['ContentSearchTool']['content_used'] = content_used

        if "SQL Query used:" in information_used:     
            sql_query_used = information_used.split("SQL Query used:")[1].strip().split("URLs used:")[0].replace("[","").replace("]","").strip()
            if (not sql_query_used.strip()) or (sql_query_used.strip().lower() == "none"):
                sql_query_used = []
            else:
                sql_query_used = list(sql_query_used.split(';'))
                sql_query_used = [sql.strip() for sql in sql_query_used]
            info_used_output['DatabaseSearchTool']['sql_query'] = sql_query_used

        if "URLs used:" in information_used:
          # Get URLs used and assign to dictionary
          urls_used = information_used.split("URLs used:")[1].strip().replace("[","").replace("]","").replace(" ", "").strip().replace("'","").replace('"',"")
          if (not urls_used.strip()) or (urls_used.strip().lower() == "none"): 
               urls_used = []
          else:
               urls_used = list(urls_used.split(","))
          info_used_output['GoogleSearchTool']['urls_used'] = urls_used
               
    except Exception as e:
        # Handle any unexpected errors during parsing
        logger.error(f"Error parsing final answer: {e}")
        final_answer = final_answer_string.strip()

    return final_answer, info_used_output

def default_annotations_cleaner(item):
    """
    This function is used to clean the annotations section of the response.
    """
    try:
        # Remove tools if they're empty
        if item['ContentSearchTool']['content_used'] in (["..."], [""], [], [" "]) and item['ContentSearchTool']['content_retrieved'] in ([{}], [""], [], [" "]):
          item.pop('ContentSearchTool')
        if item['DatabaseSearchTool']['sql_query'] in (["..."], [""], [], [" "]):
            item.pop('DatabaseSearchTool')
        if item['GoogleSearchTool']['urls_used'] in (["..."], [" "], []) and item['GoogleSearchTool']['content_retrieved'] in ([{}], [""], [], [" "]):
          item.pop('GoogleSearchTool')
     
        # Rebuild content search
        if "ContentSearchTool" in item:
            ## Get content search dictionary
            content_search_dict =  item["ContentSearchTool"]

            ## Get the content used and content retrieved. Get unique list for both
            all_content_id_used = list(set(content_search_dict["content_used"]))
            all_content_retrieved_dict = {dictionary["content_id"]: dictionary for dictionary in content_search_dict['content_retrieved']}
            unique_content_id_keys = list(set(all_content_retrieved_dict.keys()))
            all_content_retrieved_dict = {key: all_content_retrieved_dict[key] for key in unique_content_id_keys}
            unique_content_retrieved = list(all_content_retrieved_dict.values())

            ## Create storage for content used and other relevant content
            content_used = []
            other_relevant_content = []

            for content in unique_content_retrieved:
                if content["content_id"] in all_content_id_used:
                    content_used.append(content)
                else:
                    other_relevant_content.append(content)
          
            ## Finally replace in annotations
            item["ContentSearchTool"] = {"content_used": content_used, "other_relevant_content": other_relevant_content}

        if "GoogleSearchTool" in item:
          ## Get content search dictionary
          google_search_dict =  item["GoogleSearchTool"]

          ## Get the content used and content retrieved. Get unique list for both
          all_urls_used = list(set(google_search_dict["urls_used"]))
          all_urls_retrieved_dict = {dictionary["url"]: dictionary for dictionary in google_search_dict['content_retrieved']}
          unique_url_keys = list(set(all_urls_retrieved_dict.keys()))
          all_urls_retrieved_dict = {key: all_urls_retrieved_dict[key] for key in unique_url_keys}
          unique_urls_retrieved = list(all_urls_retrieved_dict.values())

          ## Create storage for content used and other relevant content
          urls_used = []
          other_relevant_urls = []

          # Loop through URL dictionary
          for url in unique_urls_retrieved:
               if url["url"] in all_urls_used:
                    urls_used.append(url)
               else:
                    other_relevant_urls.append(url)
          
          ## Finally replace in annotations
          item["GoogleSearchTool"] = {"urls_used": urls_used, "other_relevant_urls": other_relevant_urls}

        return item

    except Exception as e:
        # Handle any unexpected errors during cleaning
        logger.error(f"Error cleaning annotations: {e}")