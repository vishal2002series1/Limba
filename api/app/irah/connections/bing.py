# from langchain.utilities import BingSearchAPIWrapper
from langchain_community.utilities import BingSearchAPIWrapper
import os

bing_search = BingSearchAPIWrapper(bing_subscription_key = os.getenv("ZZ_BING_SUBSCRIPTION_KEY"),
                                   bing_search_url = os.getenv("ZZ_BING_SEARCH_URL"))