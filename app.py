from flask import Flask, render_template, request, redirect, url_for, flash
from flask_dropzone import Dropzone
from flask_login import LoginManager, UserMixin, login_user, current_user
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
dropzone = Dropzone(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, video/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 100
app.config['DROPZONE_MAX_FILES'] = 10
app.config['UPLOAD_FOLDER'] = 'static/uploads'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = {
    "user1": User("user1", "user1@example.com", "password1"),
    "user2": User("user2", "user2@example.com", "password2"),
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_urls = [f'/static/uploads/{f}' for f in files]
    return render_template('index.html', file_urls=file_urls)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Files uploaded successfully!", 204
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users.values():
            if user.username == username and user.password == password:
                login_user(user)
                return redirect(url_for('index'))
        return "Invalid username or password.", 403
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('signup'))
        if username in users:
            flash('Username already taken.')
            return redirect(url_for('signup'))
        user_id = f"user{len(users) + 1}"
        user = User(user_id, username, password)
        users[user_id] = user
        login_user(user)
        flash('Account created successfully!')
        return redirect(url_for('index'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
