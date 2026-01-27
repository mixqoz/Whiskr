from flask import Flask, render_template, request, redirect, url_for
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

try:
    with open(file, "r") as f:
        feedback = json.load(f)
except:
    feedback = []
    with open(file, "w") as f:
        json.dump(feedback, f)
        

        
@app.route('/')
def start():
	return render_template('start.html')

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


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
