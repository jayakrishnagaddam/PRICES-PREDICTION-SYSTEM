from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
import os
from vegetableprediction import method
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(dotenv_path="database.env")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/predict_price/<vegetable_name>')
def predict_price(vegetable_name):
    try:
        price_prediction = method(vegetable_name)
        formatted_price = "{:.2f}".format(price_prediction)
        return render_template('prediction.html', vegetable=vegetable_name, price=formatted_price)
    except Exception as e:
        return f"Error predicting price for {vegetable_name}: {e}"

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('firstname'),
            'last_name': request.form.get('lastname'),
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        mongo.db.users.insert_one(user_data)

        flash('SIGN UP SUCCESSFULL...YOU CAN NOW LOGIN HERE...', 'success')  # Flash success message
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = mongo.db.users.find_one({'username': username, 'password': password})
        if user_data:
            firstname = user_data['first_name']
            session['username'] = username
            session['first_name']=firstname
            return redirect(url_for('predator', name=firstname))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)  
    flash('You have been logged out', 'success') 
    return redirect(url_for('login'))


@app.route('/predator/<name>')
def predator(name):
    return render_template('predator.html',name=name)


@app.route('/contactus', methods=['POST','GET'])
def contactus():
    if request.method == "POST":
        complaints = {
            'Name': request.form['name'],
            'Email': request.form['email'],
            'Problem': request.form['problem']
        }
        
        mongo.db.complaints.insert_one(complaints)
        
        if session.get('first_name'):  # Check if 'username' is in the session
            name = session['first_name']
            return redirect(url_for('predator', name=name))
    return render_template('contactus.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/vegetable')
def vegetable():
    return render_template('vegetable.html')

@app.route('/localmarkets')
def localmarkets():
    return render_template('localmarkets.html')

@app.route('/predator')
def pradator():
    return render_template('index.html')
@app.route('/received')

def received():
    return render_template('received.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
