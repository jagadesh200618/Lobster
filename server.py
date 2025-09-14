from flask import Flask, render_template, render_template_string, request
from scrapper import tagExtract

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form.get("url")
    content = None
    if url != None: content = tagExtract(url)
    return render_template("extract.html", tag=content.child[1])

if __name__ == '__main__':
    app.run()
