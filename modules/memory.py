import redis
import chromadb
import json
from modules.logging import logger

class RedisMemory:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        try:
            self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
            self.redis_client.ping()
            logger.info("Successfully connected to Redis.")
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Could not connect to Redis: {e}")
            self.redis_client = None

    def save_conversation(self, session_id: str, user_input: str, response_text: str):
        if not self.redis_client:
            logger.warning("Redis client not available. Skipping conversation save.")
            return

        conversation_turn = {
            "user": user_input,
            "assistant": response_text
        }
        try:
            self.redis_client.rpush(session_id, json.dumps(conversation_turn))
            logger.debug(f"Saved conversation for session {session_id}")
        except Exception as e:
            logger.error(f"Failed to save conversation to Redis: {e}")

    def get_conversation_history(self, session_id: str, limit: int = 10) -> list:
        if not self.redis_client:
            logger.warning("Redis client not available. Returning empty history.")
            return []

        try:
            history_json = self.redis_client.lrange(session_id, -limit, -1)
            history = [json.loads(turn) for turn in history_json]
            logger.debug(f"Retrieved conversation history for session {session_id}")
            return history
        except Exception as e:
            logger.error(f"Failed to retrieve conversation history from Redis: {e}")
            return []

class ChromaDBMemory:
    def __init__(self, path: str = "chroma_db", collection_name: str = "documents"):
        try:
            self.client = chromadb.PersistentClient(path=path)
            self.collection = self.client.get_or_create_collection(name=collection_name)
            logger.info(f"Successfully connected to ChromaDB collection '{collection_name}'.")
        except Exception as e:
            logger.error(f"Could not connect to ChromaDB: {e}")
            self.client = None
            self.collection = None

    def add_document(self, document: str, metadata: dict = None, doc_id: str = None):
        if not self.collection:
            logger.warning("ChromaDB collection not available. Skipping add document.")
            return

        try:
            self.collection.add(
                documents=[document],
                metadatas=[metadata] if metadata else None,
                ids=[doc_id] if doc_id else None
            )
            logger.debug(f"Added document to ChromaDB: {doc_id or 'auto-id'}")
        except Exception as e:
            logger.error(f"Failed to add document to ChromaDB: {e}")

    def search(self, query: str, n_results: int = 3) -> list:
        if not self.collection:
            logger.warning("ChromaDB collection not available. Returning empty search results.")
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            logger.debug(f"Searched ChromaDB for '{query}'.")
            return results.get('documents', [])
        except Exception as e:
            logger.error(f"Failed to search ChromaDB: {e}")
            return []
