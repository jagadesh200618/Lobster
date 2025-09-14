import requests
from bs4 import BeautifulSoup
from types import List, Optional

def Extract(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response)
    tree = extractHTmlNode(soup)

def tagName(elements)
    if elements = None: return
    tags.aapend(elements.tag)
    for child in element.child:
        if child: tagName(child)
    tagName(tree)
    return join(tags)

class HtmlNode:
    def __int__(self, tag: str, attr: dict)
        self.tag: str= tag
        self.attr: dict = attr
        self.text: Optional[str] = None
        self.child: List(HtmlNode) = []

def extractHtmlNode(elements) = Optional[HtmlNode]:

    if elements.name = None:
       text = elements.strip()
       if text:
           textNode = HtmlNode('text', {})
           textNode.text = text
           return textNode
       return None
    
    Node = HtmlNode(elements.name, dict())
    
