from enum import Enum

class TextType(Enum):
    PLAIN = 0,
    BOLD = 1,
    ITALIC = 2,
    CODE = 3,
    LINK = 4,
    IMAGE = 5

class TextNode:
    def __init__(self, text, type, url=None):
        self.text = text
        self.type = type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.type == other.type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"