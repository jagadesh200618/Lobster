import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def tagExtract(url: str):
    response = requests.get(url)
    soup  = BeautifulSoup(response.content, "html.parser")
    tree = extractHtmlNode(soup)
    tags = []
    def tagName(element):
        if element == None: return
        tags.append(element.tag)
        for child in element.child:
            if child: tagName(child)
    tagName(tree)
    return "\n".join(tags)

class HtmlNode:
    def __init__(self, tag: str, attr: dict):
        self.tag: str= tag
        self.attr: dict = attr
        self.text: Optional[str] = None
        self.child: List[HtmlNode] = []

def extractHtmlNode(element) -> Optional[HtmlNode]:
    # 1. Extracting text
    if element.name == None:
        text = element.strip()
        if text:
            textNode = HtmlNode("text", {})
            textNode.text = text
            return textNode
        return None

    # 2. Extracting Tag
    node = HtmlNode(element.name, dict(element.attrs) if element.attrs else {})

    # 3. Extracting Childrens
    for child in element.children:
        childNode = extractHtmlNode(child)
        if childNode: node.child.append(childNode)

    return node
