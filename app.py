from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

file = 'data.json'

try:
    with open(file, "r") as f:
        feedback = json.load(f)
except:
    feedback = []
    with open(file, "w") as f:
        json.dump(feedback, f)
        
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
