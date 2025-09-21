import json
import requests
from lxml import html
from typing import List
from scrapper import Config, HtmlNode, extractHtmlNode
from flask import Flask, render_template, render_template_string, request, session, Response, jsonify

app = Flask(__name__)
app.secret_key = "my-secrect-key"
html_cache = {}

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form.get("url")
    content = None
    if url != None: 
        try:
            response = requests.get(url)
            response.raise_for_status()
            # store raw html
            raw_lxml_tree = html.fromstring(response.content)
            html_cache["original_lxml_tree"] = raw_lxml_tree
            # Convert to HtmlNode for rendering
            content = extractHtmlNode(raw_lxml_tree)
            html_cache["extracted"] = content
        except requests.exceptions.RequestException as e:
            # Handle request errors gracefully
            return f"Error: Failed to fetch the URL. {e}", 400
    return render_template("extract.html", tag=content)

def convert_filter_to_xpath(filters):
    if not filters: return "//*[1=0]"
    xpath_parts = []
    def build_xpath_segment(current_filters):
        if not current_filters:
            return ""    
        current_filter = current_filters[0]
        part = ""
        if current_filter['type'] == 'tagname':
            part = current_filter['value']
        elif current_filter['type'] == 'text':
            part = f"*[contains(text(), '{current_filter['value']}')]"
        elif current_filter['type'] == 'xpath':
            part = f"{current_filter['value']}"
        if 'depth_options' in current_filter and current_filter['depth_options']:
            part += "/" + build_xpath_segment(current_filter['depth_options'])
        return part
    # For the top level, use // to search the entire document
    top_level_filter = build_xpath_segment(filters)
    return f"//{top_level_filter}"

def build_filtered_tree(lxml_elements) -> HtmlNode:
    """
    Builds a single custom HtmlNode tree from a list of filtered lxml elements.
    """
    # Create a new root node to hold the filtered elements
    root_node = HtmlNode('div', {'id': 'filtered-results'})
    
    # We use a set to ensure we only process unique elements
    unique_elements = list(set(lxml_elements))

    for element in unique_elements:
        node = extractHtmlNode(element)
        if node:
            root_node.child.append(node)
    
    return root_node


@app.route('/filter', methods=['POST'])
def filterFn():
    filter_data = request.get_json()
    xpath = convert_filter_to_xpath(filter_data["filters"])
    # Retrieve the original, raw lxml tree directly from the cache
    original_lxml_tree = html_cache.get("original_lxml_tree")
    if not original_lxml_tree:
        return jsonify({"error": "Original tree not found. Please extract a URL first."}), 400
    # Perform the XPath search on the original lxml tree
    filtered_elements = original_lxml_tree.xpath(xpath)
    filtered_nodes = build_filtered_tree(filtered_elements)
    print(filtered_nodes.toJson(Config()))
    return render_template_string("{% from 'tree.html' import render_node %}{{ render_node(tag) }}", tag=filtered_nodes)

@app.route('/download', methods=['POST'])
def download():
    filter_data = request.get_json()
    xpath = convert_filter_to_xpath(filter_data["filters"])
    # Retrieve the original, raw lxml tree directly from the cache
    original_lxml_tree = html_cache.get("original_lxml_tree")
    if not original_lxml_tree:
        return jsonify({"error": "Original tree not found. Please extract a URL first."}), 400
    # Perform the XPath search on the original lxml tree
    filtered_elements = original_lxml_tree.xpath(xpath)
    filtered_nodes = build_filtered_tree(filtered_elements)
    config = Config()
    output = filtered_nodes.toJson(config)
    json_output = json.dumps(output, indent=4)

    response = Response(
        json_output,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=result.json"}
    )
    return response
    
    

if __name__ == '__main__':
    app.run()

