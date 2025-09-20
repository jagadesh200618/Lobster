from scrapper import tagExtract, HtmlNode
from typing import Optional

def view_tree(node: Optional[HtmlNode], indent: int = 0) -> None:
    """
    Print HtmlNode tree structure as indented list
    """
    if not node:
        print("No results found")
        return
    
    spaces = "  " * indent
    
    if node.tag == "text":
        text = node.text[:50] + "..." if len(node.text) > 50 else node.text
        print(f"{spaces}TEXT: '{text}'")
    else:
        attrs = " ".join([f'{k}="{v}"' for k, v in node.attr.items()][:3])
        attrs_str = f" {attrs}" if attrs else ""
        print(f"{spaces}<{node.tag}{attrs_str}>")
    
    for child in node.child:
        view_tree(child, indent + 1)


url = "https://www.google.com"

result = tagExtract(url)

filtered = result.xpath("//*[@id='gws-output-pages-elements-homepage_additional_languages__als']")
view_tree(filtered)



