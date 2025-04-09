from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import BaseMessage, BaseRetriever, Document
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.docstore.document import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts.base import BasePromptTemplate
import json
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Type,
)

import numpy as np
from pydantic import BaseModel, root_validator

import json
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Type,
)

import numpy as np
from pydantic import BaseModel, root_validator

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.utils import get_from_dict_or_env
from langchain.vectorstores.base import VectorStore, VectorStoreRetriever
from app.archive.redis_db import Redis_DB

class CustomRedisVectorStoreRetriever(VectorStoreRetriever, BaseModel):
    vectorstore: Redis_DB
    search_type: str = "similarity_limit"
    chunk_numbers: int = 0
    score_threshold: float = 0.5
    chunk_model_size: int = 500
    embeddings: OpenAIEmbeddings
    result_history: List

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @root_validator()
    def validate_search_type(cls, values: Dict) -> Dict:
        """Validate search type."""
        if "search_type" in values:
            search_type = values["search_type"]
            if search_type not in ("similarity", "similarity_limit"):
                raise ValueError(f"search_type of {search_type} not allowed.")
        return values

    def get_relevant_documents(self, query: str) -> List[Document]:
        if self.search_type == "similarity":
            docs =  self.vectorstore.search_redis(self.embeddings,query,chunk_numbers=self.chunk_numbers,score_threshold=self.score_threshold,chunk_size=self.chunk_model_size)
            self.result_history = docs
        elif self.search_type == "similarity_limit":
            docs =  self.vectorstore.search_redis(self.embeddings,query,chunk_numbers=self.chunk_numbers,score_threshold=self.score_threshold,chunk_size=self.chunk_model_size)
            self.result_history = docs
        else:
            raise ValueError(f"search_type of {self.search_type} not allowed.")
        return docs[0]