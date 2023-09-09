import numpy as np
from typing import List, Dict
from functions import Function
from .index import FunctionIndex
from utils.openai_utils import get_embedding

class DescriptionEmbeddingIndex(FunctionIndex):
    ''' function database based on discription embedding vector database'''
    
    functions: Dict[str, Function]
    embeddings: Dict[str, List[float]]

    def __init__(self):
        self.functions = {}
        self.embeddings = {}

    def put(self, function: Function):
        if not isinstance(function, Function):
            raise TypeError('CREATE ERROR: parameter must be of type Function')
        
        name = function.name

        if name not in self.functions:
            self.functions[name] = function
            self.embeddings[name] = get_embedding(function.description)
        else:
            if not self.functions[name].description == function.description:
                self.embeddings[name] = get_embedding(function.description)
            self.functions[name] = function

    def get(self, name: str) -> Function:
        if name not in self.functions:
            return None
        return self.functions[name]
    
    def retrieve(self, query: str, k: int = 3) -> List[Function]:
        query_embedding = get_embedding(query)

        scores = [
            (name, np.inner(query_embedding, embedding))
            for name, embedding in self.embeddings.items()
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [self.functions[name] for name, _ in scores[:k]]