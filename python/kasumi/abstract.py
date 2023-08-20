from __future__ import annotations

'''
    This file contains the class for the Kasumi SDK.
    It is used to interact with the Kasumi API.
'''
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Iterator
from .base_cls import TokenType

class KasumiException(Exception):
    """
    This class is used to represent an exception raised by the Kasumi SDK.
    """
    pass

class AbstractKasumiEmbeddingItem(ABC):
    """
    This class is used to represent an embedding item.
    You can use it to store the embedding and the id of the item.
    Remember that the id is the id of the item in the `Your` database.
    """
    embedding: List[float] = []
    similarity: float = 0.0
    id: str = ""

    @abstractmethod
    def __init__(self, embedding: List[float], id: str):
        pass

    @abstractmethod
    def set_similarity(self, similarity: float) -> None:
        pass

    @abstractmethod
    def get_similarity(self) -> float:
        pass

class AbstractKasumiConfigration(ABC):
    _token: str = ""
    _search_key: str = ""
    _kasumi_url: str = ""
    _app_id: int = 0

    @abstractmethod
    def __init__(self, app_id: int, token: str, search_key: str, kasumi_url: str = "http://kasumi.miduoduo.org:8196"):
        pass

    @abstractmethod
    def get_app_id(self) -> int:
        pass
        
    @abstractmethod
    def get_token(self) -> str:
        pass
    
    @abstractmethod
    def get_search_key(self) -> str:
        pass
    
    @abstractmethod
    def get_kasumi_url(self) -> str:
        pass

class AbstractKasumiSearchResultField(ABC):
    """
    AbstractAbstractKasumiSearchResultField is used to represent a field in the search result.
    _key: The key of the field.
    _content: The content of the field.
    _llm_disabled: this field will not be sent to the LLM if this is set to True.
    _show_disabled: this field will not be shown to the client if this is set to True.
    """
    _key: str = ""
    _content: str = ""
    _llm_disabled: bool = False
    _show_disabled: bool = False

    @abstractmethod
    def __init__(self,key: str, content: str, llm_disabled: bool = False, show_disabled: bool = False):
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class AbstractKasumiSearchResult(ABC):
    _fields: List[AbstractKasumiSearchResultField] = []

    @abstractmethod
    def __init__(self, fields: List[AbstractKasumiSearchResultField]):
        self.fields = fields
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fields": [field.to_dict() for field in self._fields]
        }
    
    @staticmethod
    @abstractmethod
    def load_from_dict(data: Dict[str, Any], disabled_llm_columns: List[str] = None, disabled_show_columns: List[str] = None) -> AbstractKasumiSearchResult:
        pass

class AbstractKasumiSpider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @abstractmethod
    def search(self, column: str, value: str) -> Iterator[AbstractKasumiSearchResult]:
        pass

class AbstractKasumiSearchStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def possible_columns(self) -> List[str]:
        pass

    @abstractmethod
    def search(self, app: AbstractKasumi, column: str, value: str) -> Iterator[AbstractKasumiSearchResult]:
        pass

class AbstractKasumiSearchResponse(ABC):
    _code: int = 0
    _message: str = ""
    _data: List[AbstractKasumiSearchResult]

    @abstractmethod
    def __init__(self, code: int, message: str, data: List[AbstractKasumiSearchResult]):
        pass

    @abstractmethod
    def get_code(self) -> int:
        pass

    @abstractmethod
    def get_message(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> List[AbstractKasumiSearchResult]:
        pass

class AbstractKasumiInfoResponse(ABC):
    _code: int = 0
    _message: str = ""
    _data: Dict[str, Any]

    @abstractmethod
    def __init__(self, code: int, message: str, data: Dict[str, Any]):
        pass

    @abstractmethod
    def get_code(self) -> int:
        pass

    @abstractmethod
    def get_message(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        pass

class AbstractKasumiSession(object):
    _user_token: str = ""

class AbstractKasumi(ABC):
    """
    This class is used to interact with the Kasumi API.

    :param config: The configuration of the Kasumi SDK.
    
    :raises all methods in Kasumi may raise KasumiException if the Kasumi API returns an error.
    """
    _config: AbstractKasumiConfigration = None
    _search_strategy: List[AbstractKasumiSearchStrategy] = []
    _spiders: List[AbstractKasumiSpider] = []
    _sessions: Dict[int, AbstractKasumiSession] = {}

    @abstractmethod
    def __init__(self, config: AbstractKasumiConfigration):
        pass

    @abstractmethod
    def embeding_text(self, text: str) -> List[float]:
        pass
        
    @abstractmethod
    def search_embedding_similarity(self, embedding: List[float], limit: int = 10) -> List[AbstractKasumiEmbeddingItem]:
        pass

    @abstractmethod
    def get_embedding_by_id(self, id: str) -> AbstractKasumiEmbeddingItem:
        pass

    @abstractmethod
    def insert_embedding(self, embedding: List[float], id: str) -> bool:
        pass

    @abstractmethod
    def add_search_strategy(self, strategy: AbstractKasumiSearchStrategy) -> None:
        pass

    @abstractmethod
    def add_spider(self, spider: AbstractKasumiSpider) -> None:
        pass

    @abstractmethod
    def get_search_strategies(self) -> List[AbstractKasumiSearchStrategy]:
        pass

    @abstractmethod
    def get_spiders(self) -> List[AbstractKasumiSpider]:
        pass

    @abstractmethod
    def _handle_request_info(self, request: Dict[str, Any]) -> AbstractKasumiInfoResponse:
        pass
    
    @abstractmethod
    def _handle_request_search(self, request: Dict[str, Any]) -> AbstractKasumiSearchResponse:
        pass

    @abstractmethod
    def run_forever(self) -> None:
        pass

class AbstractKasumiEmbedding(ABC):
    @abstractmethod
    def insert_embedding(app: AbstractKasumi, embedding: List[float], id: str) -> bool:
        """
        This function is used to insert an embedding into the Kasumi database.

        will not cost any KaToken but has a limit of 1000 times per day.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param embedding: The embedding to insert.
        :return: True if the embedding was inserted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def embedding_text(app: AbstractKasumi, text: str, token_type: TokenType, token: str):
        """
        This function is used to get the embedding of a text.

        cause it's necessary to cost tokens to embedding text in Kasumi, so you should pass the token_type and token to this function.
        token_type declare the type of the token, to security reason, if the caller is user not developer, Kasumi will send an encrypted token to the caller, finally pass it here.
        but if developer call this function, you can pass TokenType.PLAINTEXT and token to this function.

        :param text: The text to get the embedding of.
        :param token_type: The type of the token. Can be TokenType.PLAINTEXT or TokenType.ENCRYPTION.
        :return: The embedding of the text.
        """

    @abstractmethod
    def search_similarity(app: AbstractKasumi, embedding: List[float], token_type: TokenType, token: str, limit: int = 10) -> List[AbstractKasumiEmbeddingItem]:
        """
        This function is used to search for embeddings that are similar to a given embedding.

        search similarity will cause at least 1 KaToken, so you should pass the token_type and token to this function.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param embedding: The embedding to search for.
        :param limit: The maximum number of embeddings to return.
        :return: A list of EmbeddingSimilarity objects.
        """
        pass

    @abstractmethod
    def get_embedding_by_id(app: AbstractKasumi, id: str, token_type: TokenType, token: str) -> AbstractKasumiEmbeddingItem:
        """
        This function is used to get the embedding of an item by its id.

        get embedding by id will cause at least 1 KaToken, so you should pass the token_type and token to this function.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param id: The id of the item.
        :return: The embedding of the item.
        """
        pass

class AbstractKasumiEmbedding(ABC):
    @abstractmethod
    def insert_embedding(app: AbstractKasumi, embedding: List[float], id: str) -> bool:
        """
        This function is used to insert an embedding into the Kasumi database.

        will not cost any KaToken but has a limit of 1000 times per day.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param embedding: The embedding to insert.
        :return: True if the embedding was inserted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def embedding_text(app: AbstractKasumi, text: str, token_type: TokenType, token: str) -> List[float]:
        """
        This function is used to get the embedding of a text.

        cause it's necessary to cost tokens to embedding text in Kasumi, so you should pass the token_type and token to this function.
        token_type declare the type of the token, to security reason, if the caller is user not developer, Kasumi will send an encrypted token to the caller, finally pass it here.
        but if developer call this function, you can pass TokenType.PLAINTEXT and token to this function.

        :param text: The text to get the embedding of.
        :param token_type: The type of the token. Can be TokenType.PLAINTEXT or TokenType.ENCRYPTION.
        :return: The embedding of the text.
        """

    @abstractmethod
    def search_similarity(app: AbstractKasumi, embedding: List[float], token_type: TokenType, token: str, limit: int = 10) -> List[AbstractKasumiEmbeddingItem]:
        """
        This function is used to search for embeddings that are similar to a given embedding.

        search similarity will cause at least 1 KaToken, so you should pass the token_type and token to this function.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param embedding: The embedding to search for.
        :param limit: The maximum number of embeddings to return.
        :return: A list of EmbeddingSimilarity objects.
        """
        pass

    @abstractmethod
    def get_embedding_by_id(app: AbstractKasumi, id: str, token_type: TokenType, token: str) -> AbstractKasumiEmbeddingItem:
        """
        This function is used to get the embedding of an item by its id.

        get embedding by id will cause at least 1 KaToken, so you should pass the token_type and token to this function.

        :param app_id: The id of the app.
        :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
        :param id: The id of the item.
        :return: The embedding of the item.
        """
        pass