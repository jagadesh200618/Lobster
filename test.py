
from scrapper import tagExtract, Config

url = "https://www.google.com"
node = tagExtract(url)

config = Config()
print(node.toJson(config))