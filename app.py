from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SAS"
db= PyMongo(app).db


@app.route('/')
def function():
  user_data={
    'username': 1,
    'pass' : 2
  }
  db.users.insert_one(user_data)
  return render_template("index.html")
@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/signup')
def signup():
  return render_template('signup.html')
if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
