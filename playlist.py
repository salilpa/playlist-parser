from flask import Flask

app = Flask(__name__)


#returns a page with links to all websites
@app.route('/', methods=["POST"])
def index():
    return 'Hello World!'