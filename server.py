from flask import Flask, render_template, jsonify
from scrape_twitter import scrape_twitter
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["trending_topics"]
collection = db["topics"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    record = scrape_twitter()
    return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)
