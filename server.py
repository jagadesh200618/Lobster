from flask import Flask, render_template, render_template_string, request
from scrapper import tagExtract

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form.get("url")
    content = ""
    if url != None: content = tagExtract(url)
    return render_template("extract.html", url=render_template_string(content))

if __name__ == '__main__':
    app.run()
