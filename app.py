from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"  # Add a secret key for flash messages
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
            firstname = user_data['first_name']  # Corrected syntax here
            session['username'] = username
            return redirect(url_for('homepage', name=firstname))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/homepage/<name>')
def homepage(name):
    return render_template('homepage.html', name=name)


@app.route('/example/<name>')
def example():
    data=request.args.get('name')
    return render_template('example.html',name=data)



@app.route('/vegetable')
def vegetable():
    return render_template('vegetable.html')

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

@app.route('/kharif')
def kharif():
    return render_template('kharif.html')

@app.route('/rabi')
def rabi():
    return render_template('rabi.html')

@app.route('/zaid')
def zaid():
    return render_template('zaid.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
