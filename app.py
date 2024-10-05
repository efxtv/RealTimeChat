from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB

# Initialize SocketIO
socketio = SocketIO(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    emit('user_joined', {'name': data['name'], 'room': data['room']}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', data, broadcast=True)

@socketio.on('upload_image')
def handle_image(data):
    emit('receive_image', {'image_path': data['image_path'], 'room': data['room']}, broadcast=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return {'error': 'No file uploaded'}, 400
    photo = request.files['photo']
    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = f'/static/images/{filename}'
        return {'image_path': image_path}

if __name__ == '__main__':
    socketio.run(app, debug=True)
