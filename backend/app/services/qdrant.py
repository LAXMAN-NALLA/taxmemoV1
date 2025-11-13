"""Qdrant Vector DB connection and search service."""
from typing import List, Dict, Any, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.core.config import settings
from openai import OpenAI


class QdrantService:
    """Service for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize Qdrant client."""
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
        else:
            self.client = QdrantClient(url=settings.qdrant_url)
        
        # V1: Use the netherlands_pilot collection from data ingestion
        self.collection_name = "netherlands_pilot"
        # Initialize OpenAI for text embeddings
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
    
    def search(
        self,
        query: str,
        limit: int = 5,
        country: str = "netherlands",
        year: str = "2025"
    ) -> List[Dict[str, Any]]:
        """
        Search the vector database with mandatory metadata filters.
        
        CRITICAL: Must always filter by country="netherlands" and year="2025" for V1.
        
        Args:
            query: Search query text
            limit: Number of results to return (default: 5)
            country: Country filter (default: "netherlands")
            year: Year filter (default: "2025")
        
        Returns:
            List of search results with metadata
        """
        try:
            # Convert query text to embedding vector
            # Qdrant search requires a query vector, not text
            query_vector = self._text_to_embedding(query)
            
            # Perform vector search (no metadata filters for V1 - search all documents)
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    "score": result.score,
                    "payload": result.payload,
                    "id": result.id
                })
            
            return results
        
        except Exception as e:
            # Log error and return empty list
            print(f"Qdrant search error: {str(e)}")
            return []
    
    def format_context(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Format search results into a context string for LLM.
        
        Args:
            search_results: List of search result dictionaries
        
        Returns:
            Formatted context string
        """
        if not search_results:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            payload = result.get("payload", {})
            # LangChain QdrantVectorStore stores: page_content and metadata
            content = payload.get("page_content", "")
            metadata = payload.get("metadata", {})
            source_filename = metadata.get("source_filename") or metadata.get("source", "Unknown")
            
            context_parts.append(f"Context {i} (Source: {source_filename}):\n{content}")
        
        return "\n---\n".join(context_parts)
    
    def _text_to_embedding(self, text: str) -> List[float]:
        """
        Convert text to embedding vector using OpenAI.
        
        Args:
            text: Text to convert to embedding
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Return empty vector as fallback (will result in no matches)
            return [0.0] * 1536  # text-embedding-3-small dimension

