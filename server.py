from flask import Flask, render_template, render_template_string, request, session, Response
from scrapper import tagExtract, Config
import json

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
        content = tagExtract(url)
        html_cache["extracted"] = content
    return render_template("extract.html", tag=content)

@app.route('/filter', methods=['POST'])
def filterFn():
    filter_data = request.get_json()
    print(filter_data)
    content = html_cache["extracted"]
    return render_template("extract.html", tag=content)


@app.route('/download', methods=['POST'])
def download():
    filter_data = request.get_json()
    content = html_cache["extracted"]
    config = Config()
    output = content.toJson(config)
    json_output = json.dumps(output, indent=4)

    response = Response(
        json_output,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=result.json"}
    )
    return response
    
    

if __name__ == '__main__':
    app.run()

