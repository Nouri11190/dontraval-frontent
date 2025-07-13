from flask import (
    Flask, render_template, request, jsonify, send_from_directory
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
import os
from auth import register_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY']      = 'your-secret-key'
app.config['JWT_SECRET_KEY']  = 'your-jwt-secret'
app.config['UPLOAD_FOLDER']   = 'uploads'

# create uploads folder if missing
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

jwt = JWTManager(app)

# ---------- Public ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- Auth ----------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data['email'], data['password'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data['email'], data['password'])

# ---------- Upload ----------
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)
    return jsonify({'message': 'Upload successful'}), 201

# ---------- Dashboard API ----------
@app.route('/api/dashboard-data')
@jwt_required()
def dashboard_data():
    user  = get_jwt_identity()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'user': user, 'files': files})

# ---------- Serve uploaded files (optional) ----------
@app.route('/uploads/<path:fname>')
@jwt_required()
def get_file(fname):
    return send_from_directory(app.config['UPLOAD_FOLDER'], fname)

# ---------- Dashboard page ----------
@app.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
