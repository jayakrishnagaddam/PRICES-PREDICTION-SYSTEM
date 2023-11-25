from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SAS"
db = PyMongo(app).db

@app.route('/')
def function():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Access form data using request.form
          user_data = {
       'first_name':request.form.get('firstname'),
        'last_name':  request.form.get('lastname'),
        'username': request.form.get('username'),
       'password':  request.form.get('password')
          }

          db.users.insert_one(user_data)

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
