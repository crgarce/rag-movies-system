from typing import List, Optional

class Document:
    def __init__(self, title: str, image: str, content: str, embedding: Optional[List[float]] = None):
        self.title = title
        self.image = image
        self.content = content
        self.embedding = embedding
