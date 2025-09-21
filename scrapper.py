from lxml import etree
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Config:
    tag: bool = True
    attr: bool = True
    text: bool = True

class HtmlNode:
    def __init__(self, tag: str, attr: dict):
        self.tag: str= tag
        self.attr: dict = attr
        self.text: Optional[str] = None
        self.child: List[HtmlNode] = []
        self.lxml_element: Optional[etree._lxml_element] = None

    def toJson(self, config: Config):
        result = {}
        if config.tag:
            result["tag"] = self.tag
        if config.attr:
            result["attr"] = self.attr
        if config.text:
            result["text"] = self.text

        result["child"] = [child.toJson(config) for child in self.child]
        
        return result


def extractHtmlNode(element) -> Optional[HtmlNode]:
    # text
    if isinstance(element, (str, bytes)):
        text = str(element).strip()
        if text:
            textNode = HtmlNode('text', {})
            textNode.text = text
            return textNode
        return None

    # skip 
    if not hasattr(element, 'tag'):
        return None
    if not isinstance(element.tag, str):
        return None

    # node
    attr = dict(element.attrib) if element.attrib else {}
    node = HtmlNode(element.tag, attr)

    # store element for search
    node.lxml_element = element

    # child
    for child in element:
        childNode = extractHtmlNode(child)
        if childNode: node.child.append(childNode)

    return node
