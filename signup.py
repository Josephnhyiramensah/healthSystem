from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
import os

# Generate a secure secret key
secret_key = os.urandom(24)

# Set the Flask app's secret key
app.secret_key = secret_key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

db.create_all()

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Render the sign-up page
@app.route('/signup', methods=['GET'])
def signup_page():
    if current_user.is_authenticated:
        return "You are already logged in."
    return render_template('signup_login.html')

# Handle user registration
@app.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return "You are already registered and logged in."

    username = request.form['name']
    password = request.form['password']

    # Hash the password before storing it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return "User registered successfully. You can now log in."

# Render the login page
@app.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return "You are already logged in."
    return render_template('signup_login.html')

# Handle user login
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return "You are already logged in."

    username = request.form['name']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return "Logged in successfully."

    return "Login failed. Please check your credentials."

# Log out the user
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return "Logged out successfully."

if __name__ == '__main__':
    app.run(debug=True)
