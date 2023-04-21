from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import os
from werkzeug.utils import secure_filename
from flask_login import UserMixin

app = Flask(__name__)
dropzone = Dropzone(app)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, video/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 100  # Set max file size limit (in MB)
app.config['DROPZONE_MAX_FILES'] = 10
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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


if __name__ == '__main__':
    app.run(debug=True)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = {
    "user1": User("user1", "user1@example.com", "password1"),
    "user2": User("user2", "user2@example.com", "password2"),
}