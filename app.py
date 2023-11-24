from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SAS"
db= PyMongo(app).db


@app.route('/')
def function():
  db.users.insert_one({"b": 2})
  return render_template("index.html")


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
