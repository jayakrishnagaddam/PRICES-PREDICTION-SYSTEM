from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Add a secret key for flash messages
app.config["MONGO_URI"] = "mongodb://localhost:27017/SAS"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = mongo.db.users.find_one({'username': username, 'password': password})

        if user_data:
            flash('Login successful', 'success')  # Flash success message
            return redirect(url_for('homepage'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

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

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
