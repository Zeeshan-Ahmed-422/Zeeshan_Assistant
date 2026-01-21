"""
Vector Store for RAG-based Memory
Stores and retrieves user behavior patterns
"""
import os
import json
from datetime import datetime, timedelta
from config.settings import Settings
from utils.logger import logger

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    from sentence_transformers import SentenceTransformer
    VECTOR_STORE_AVAILABLE = True
except ImportError:
    VECTOR_STORE_AVAILABLE = False
    logger.warning("ChromaDB or SentenceTransformers not available. Memory features limited.")

class VectorStore:
    """Vector store for semantic memory search"""
    
    def __init__(self):
        """Initialize vector store"""
        self.available = VECTOR_STORE_AVAILABLE
        self.client = None
        self.collection = None
        self.encoder = None
        
        if self.available:
            try:
                self._initialize_store()
                logger.info("Vector store initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize vector store: {e}")
                self.available = False
    
    def _initialize_store(self):
        """Initialize ChromaDB and sentence transformer"""
        # Initialize sentence transformer for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        db_path = os.path.join(Settings.DATA_DIR, "chroma_db")
        os.makedirs(db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("user_patterns")
        except:
            self.collection = self.client.create_collection(
                name="user_patterns",
                metadata={"description": "User behavior patterns and preferences"}
            )
    
    def add_pattern(self, command, context, metadata=None):
        """
        Add a command pattern to memory
        
        Args:
            command: User command text
            context: Context information (apps opened, time, etc.)
            metadata: Additional metadata
        """
        if not self.available:
            return False
        
        try:
            doc_id = f"pattern_{datetime.now().timestamp()}"
            
            # Create document text
            doc_text = f"Command: {command}. Context: {json.dumps(context)}"
            
            # Generate embedding
            embedding = self.encoder.encode(doc_text).tolist()
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            metadata.update({
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "context": json.dumps(context)
            })
            
            # Add to collection
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[doc_text],
                metadatas=[metadata]
            )
            
            logger.debug(f"Added pattern to vector store: {command}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding pattern to vector store: {e}")
            return False
    
    def search_similar_patterns(self, query, n_results=5):
        """
        Search for similar command patterns
        
        Args:
            query: Query text
            n_results: Number of results to return
            
        Returns:
            list: Similar patterns with metadata
        """
        if not self.available:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.encoder.encode(query).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Parse results
            patterns = []
            if results and results['metadatas']:
                for metadata in results['metadatas'][0]:
                    patterns.append({
                        "command": metadata.get("command"),
                        "context": json.loads(metadata.get("context", "{}")),
                        "timestamp": metadata.get("timestamp")
                    })
            
            logger.debug(f"Found {len(patterns)} similar patterns for: {query}")
            return patterns
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def get_recent_patterns(self, days=7):
        """
        Get patterns from recent days
        
        Args:
            days: Number of days to look back
            
        Returns:
            list: Recent patterns
        """
        if not self.available:
            return []
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get all documents (ChromaDB doesn't have time-based filtering directly)
            results = self.collection.get()
            
            recent_patterns = []
            if results and results['metadatas']:
                for metadata in results['metadatas']:
                    timestamp = datetime.fromisoformat(metadata.get("timestamp", ""))
                    if timestamp >= cutoff_date:
                        recent_patterns.append({
                            "command": metadata.get("command"),
                            "context": json.loads(metadata.get("context", "{}")),
                            "timestamp": metadata.get("timestamp")
                        })
            
            logger.debug(f"Retrieved {len(recent_patterns)} patterns from last {days} days")
            return recent_patterns
            
        except Exception as e:
            logger.error(f"Error getting recent patterns: {e}")
            return []

# Global vector store instance
vector_store = VectorStore()