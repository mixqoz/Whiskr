from flask import Flask, render_template, request, redirect, url_for
import json
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

file = 'data.json'

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",  # "w" = overskriv, "a" = legg til
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

try:
    with open(file, "r") as f:
        feedback = json.load(f)
except:
    feedback = []
    with open(file, "w") as f:
        json.dump(feedback, f)

TZ = ZoneInfo("Europe/Oslo")

def nowNorway():
    return datetime.now(TZ)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    dateAdded = db.Column(db.DateTime(timezone=True), nullable=False, default=nowNorway)

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat-password')

        if password != repeat_password:
            return render_template('signup.html', error="Passwords do not match!")

        # Save data to JSON
        feedback.append({"firstname": firstname, "email": email, "password": password})
        with open(file, "w") as f:
            json.dump(feedback, f)

        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Simple login check
        user = next((u for u in feedback if u["email"] == email and u["password"] == password), None)
        if user:
            return redirect(url_for('home'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
