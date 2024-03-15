from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"
app.config["MONGO_URI"] = "mongodb+srv://2100090162:manigaddam@deepsheild.kzgpo9p.mongodb.net/VegetableDB"
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
            firstname = user_data['first_name']
            session['username'] = username
            session['first_name']=firstname
            return redirect(url_for('predator', name=firstname))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/predator/<name>')
def predator(name):
    return render_template('predator.html',name=name)

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/vegetable')
def vegetable():
    return render_template('vegetable.html')

@app.route('/localmarkets')
def localmarkets():
    return render_template('localmarkets.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  
    flash('You have been logged out', 'success') 
    return redirect(url_for('login'))

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

@app.route('/predator')
def pradator():
    return render_template('index.html')
@app.route('/received')

def received():
    return render_template('received.html')

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
