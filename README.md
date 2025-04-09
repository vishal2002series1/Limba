# IRAH

IRAH is an LLM-powered platform for content aggregation, information search/synthesis, and content generation that assists professionals in the Wealth & Asset Management industry perform their jobs more efficiently.

IRAH includes a user interface (UI), an application programming interface (API), and a file-processing module for processing documents. It uses Python for backend operations and Angular for frontend operations.

![image](https://github.com/ey-org/irah/assets/99744961/03dfbca5-f229-48dd-b06e-4f508100fff6)

## Project Structure

The project is structured into three main folders: `api`, `ui`, and `file-processing`,

### API

The `api` folder contains all the backend code for the application. This includes the communication with the LLMs & other data systems. It includes several utility scripts for data processing, fetching, and management. The main entry point of the application is `run.py`.

## UI

The `ui` folder contains the frontend code for the application. It includes all the Angular components, services, models, and styles. It also includes the `angular.json` configuration file, `package.json` and `package-lock.json` for managing npm packages, and `tsconfig.json` for TypeScript configuration.

### File-Processing

The `file-processing` folder includes scripts for processing and managing files & documents. It includes preprocessing scripts, summary templates, embedding scripts, and more. The file-processing module is designed to run as a function using Azure Functions. This allows for automated processing of documents as their are loaded to a file store.

## Installation

1. Clone the repo
```sh
git clone git@github.com:ey-org/irah.git
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
python run.py --debug
```

2. Start the Angular server
```sh
cd ../ui
ng serve
```

The API server will start on localhost:5000 and the Angular server will start on localhost:4200.

Note: In order to successfully connect to the various data sources & API endpoints required by IRAH, you will need to include a devConfig.yml file in your project directory. This file contains the API keys and other secrets for connecting to these services. Please reach out to Matt O'Neill (matt.oneill@ey.com) for access.

## Overview of Project Files

- API Folder  
  - app  
    - __init__.py: Initializes the application and brings together all components  
    - views.py: Defines the routes for the application  
    - utilities  
      - __init__.py: Initializes the utilities package  
      - blob_fetch_sas_url.py: Fetches a blob SAS URL  
      - cognitive_search.py: Performs cognitive searches  
      - embedded_search_base_and_comparative.py: Handles embedded searches  
      - embedding.py: Handles embedding operations  
      - langchain_utils.py: Contains utility functions for language chain operations  
      - market_data_api.py: Interacts with a market data API  
      - news_article_api.py: Interacts with a news article API  
      - preprocessing.py: Performs preprocessing on data  
      - prompt_quantitative_sql_snowflake.py: Handles SQL prompts for Snowflake  
      - prompt_templates.py: Contains templates for prompts  
      - redis_db.py: Interacts with a Redis database  
      - snowflake_openai_completion_model.py: Handles the OpenAI completion model for Snowflake  
      - summary_and_classifier_prompt_template.py: Contains templates for summary and classification prompts  
      - summary_template.py: Contains templates for summaries  
  - en_core_web_md-3.6.0.tar.gz: Spacy's English multi-task CNN trained on OntoNotes  
  - requirements.txt: Lists the Python dependencies for the project  
  - run.py: The entry point to run the server  
  
- UI Folder  
  - angular.json: Contains configuration for the Angular CLI  
  - package-lock.json: Generated automatically for any operations where npm modifies the node_modules tree, or package.json  
  - package.json: Lists the packages that your project depends on and allows you to specify the versions of a package that your project can use using semantic versioning rules  
  - src  
    - app  
    - assets  
    - environments  
    - favicon.ico: The icon that is used in the browser tab  
    - index.html: The main HTML page that is served when someone visits your site  
    - main.ts: The main entry point for your application  

- File-Processing Folder  
  - ChunkProcessing  
    - __init__.py: Initializes the ChunkProcessing package  
    - function.json: Contains configuration for the chunk processing function  
    - readme.md: Provides information about the chunk processing function  
  - blob_fetch_sas_url.py: Fetches a blob SAS URL  
  - embedding.py: Handles embedding operations  
  - host.json: Contains configuration for the file processing host  
  - preprocessing.py: Performs preprocessing on data  
  - preprocessing_widget.py: Performs preprocessing on widget data  
  - redis_db.py: Interacts with a Redis database  
  - requirements.txt: Lists the Python dependencies for the file-processing scripts  
  - summary_template.py: Contains templates for summaries  
  - widget_prompt.py: Handles prompts for widgets  

# Contributing

Please contact Matt O'Neill (matt.oneill@ey.com).
