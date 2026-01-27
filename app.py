from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

app = Flask(__name__)

ROOT_DIR = Path(__file__).resolve().parent
DATA_FILE = ROOT_DIR / 'data.json'

if not DATA_FILE.exists():
    DATA_FILE.write_text('[]', encoding='utf-8')

def load_users():
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    DATA_FILE.write_text('[]', encoding='utf-8')
    return []

def save_users(users):
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

feedback = load_users()
        

        
@app.route('/')
def start():
	return render_template('start.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        firstname = (request.form.get('firstname') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        repeat_password = request.form.get('repeat-password') or ''

        if not firstname or not email or not password or not repeat_password:
            error = 'All fields are required.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif password != repeat_password:
            error = 'Passwords do not match.'
        elif any(u.get('email', '').lower() == email for u in load_users()):
            error = 'Email is already registered.'

        if error:
            return render_template('signup.html', error=error)

        users = load_users()
        users.append({'firstname': firstname, 'email': email, 'password': password})
        save_users(users)

        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        if not email or not password:
            error = 'Email and password are required.'
        else:
            user = next(
                (u for u in load_users() if u.get('email', '').lower() == email and u.get('password') == password),
                None,
            )
            if user:
                return redirect(url_for('home'))
            error = 'Invalid email or password.'

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
