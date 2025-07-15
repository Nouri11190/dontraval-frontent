from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
import os
from auth import register_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

jwt = JWTManager(app)

# ----------------  Public pages  ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------  Auth API  ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data['email'], data['password'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data['email'], data['password'])

# ----------------  Upload & Dashboard API  ----------------
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'message': 'No file selected'}), 400
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    return jsonify({'message': 'Upload successful'}), 201

@app.route('/api/dashboard-data')
@jwt_required()
def dash_data():
    user  = get_jwt_identity()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'user': user, 'files': files})

# ----------------  Protected page  ----------------
@app.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
