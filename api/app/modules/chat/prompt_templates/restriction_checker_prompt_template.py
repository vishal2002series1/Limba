# Set restriction dictionary. It should always follow the format below
restriction_dictionary = {"1": {"Category": "Personal Identifiable Information (PII)", 
                                "Description": "Questions related to social security numbers, home addresses, credit card information, passport information, and medical records", 
                                "Example": "What is John Smith's social security number?", 
                                "Response": "I am sorry, but I cannot provide or access any personal identifiable information, such as social security numbers, home addresses, credit card information, passport information, and medical records."}, 
                          "2": {"Category": "Personalized Investment Recommendation", 
                                "Description": "Questions related to what investments someone should buy or sell", 
                                "Example": "Should Jane Doe buy Amazon stock?", 
                                "Response": "I am sorry, but I cannot provide specific investment recommendations tailored to individual profiles or situations. Please consult a financial advisor for more information on individual investment recommendations."}, 
                          "3": {"Category": "Market Activity", 
                                "Description": "Questions related to predict future market activity", 
                                "Example": "Will the S&P 500 close at an all time high today?",
                                "Response": "I am sorry, but I am not able to predict future market activity. Predicting market movements is highly uncertain as they are influenced by a multitude of unpredictable factors."}
                        }

# Define template
restriction_checker_template = """
You are a financial services professional specialised in identifying question categories. Given a question {input}, identify the category of the question from the options below and return ONLY the category number:
{restrictions_string}

If the question falls under more than one category, return all the categories seperated by a comma.
If the question does not fall under any of the categories above or if you do not know the category, return "0".
"""