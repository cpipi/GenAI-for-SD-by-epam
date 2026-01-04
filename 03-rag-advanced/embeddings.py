"""
Shared embedding utility for consistent embeddings across ingestion and retrieval. 
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

class EmbeddingModel:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            print("📥 Loading embedding model (all-MiniLM-L6-v2)...")
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            print("   ✅ Model loaded")
    
    def encode(self, texts: Union[List[str], str], **kwargs) -> Union[List[List[float]], List[float]]:
        """Encode texts into embeddings. 
        
        Args:
            texts: Single text string or list of texts
            **kwargs: Additional arguments passed to SentenceTransformer. encode()
                     (e. g., show_progress_bar, batch_size, etc.)
        
        Returns:
            Single embedding vector (list of floats) or list of embedding vectors
        """
        if isinstance(texts, str):
            texts = [texts]
            single = True
        else:
            single = False
        
        # Set default values but allow override via kwargs
        encode_params = {
            'convert_to_numpy': True,
            'normalize_embeddings': True,
            'show_progress_bar': False
        }
        encode_params.update(kwargs)  # Override with any user-provided kwargs
        
        embeddings = self._model.encode(texts, **encode_params)
        
        # Convert to list - handle both numpy arrays and lists
        if isinstance(embeddings, np.ndarray):
            result = embeddings.tolist()
        else:
            result = embeddings
        
        # Return single embedding or list of embeddings
        return result[0] if single else result
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return 384  # all-MiniLM-L6-v2