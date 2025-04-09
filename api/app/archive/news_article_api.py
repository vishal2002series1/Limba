import spacy
import requests
import warnings
import logging
from datetime import datetime, timedelta
import os

# Load the spaCy model
nlp = spacy.load("C:\\Users\\CV341PF\\OneDrive - EY\\Documents\\Projects\\irah-master\\irah-master\\api\\en_core_web_md-3.6.0\\en_core_web_md\\en_core_web_md-3.6.0")

logger = logging.getLogger(__name__)
logger.info("Check")
warnings.filterwarnings('ignore')

NEWS_ARTICLE_API_ENDPOINT = os.getenv("ZZ_NEWS_ARTICLE_API_ENDPOINT")
NEWS_ARTICLE_API_KEY =  os.getenv("ZZ_NEWS_ARTICLE_API_KEY")

class News_Article:
    def __init__(self):
        pass

    def _extract_entities(self, query):
        doc = nlp(query)
        org_entities = []  # Initialize an empty list for the lemmatized org entities
        per_entities = [f'"{ent.text}"' for ent in doc.ents if ent.label_ == 'PERSON']
        loc_entities = [f'"{ent.text}"' for ent in doc.ents if ent.label_ == 'LOC']

        for ent in doc.ents:
            if ent.label_ == 'ORG':
                org_entity_lemma = ' '.join([token.lemma_ for token in ent if token.lemma_.isalpha()])
                org_entities.append(org_entity_lemma)  # Add the lemmatized org entity to the list

        return org_entities, per_entities, loc_entities

    def get_news(self, query):
        logger.info("##### Inside news article process #####")
        org_entities, per_entities, loc_entities = self._extract_entities(query)

        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        params = {
            'q': ' OR '.join(org_entities),
            'search_in': 'title',
            'lang': 'en',
            'from_': from_date,
            'to_': to_date,
            'sort_by': 'rank',
            'page_size': 100,
            'theme': 'Finance',
            'ORG_entity_name': ' OR '.join(org_entities),
            'PER_entity_name': ' OR '.join(per_entities),
            'clustering_enabled': True,
            'clustering_threshold': 0.7,
            'clustering_variable': 'title'
        }

        headers = {'x-api-token': NEWS_ARTICLE_API_KEY}
        article_list = []

        response = requests.get(NEWS_ARTICLE_API_ENDPOINT, params=params, headers=headers, verify=False)

        if response.status_code == 200:
            logger.info("#### news api got success response #######")
            clusters = response.json().get('clusters', [])[:10]
            for cluster in clusters:
                articles = cluster.get('articles', [])
                if articles:
                    top_article = articles[0]
                    article_list.append({"doc_id": top_article['title'], "blob_file_url": top_article['link']})
            return article_list
        else:
            logger.info(f"Failed to fetch news. Status Code: {response.status_code}, Message: {response.text}")
            return article_list