
# app.py
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cv2
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '/@Potato123#'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Model untuk Admin
class Admin(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Simpan admin dalam dictionary (dalam praktik nyata, gunakan database)
admins = {}
admin_password = generate_password_hash("admin123")
admins[1] = Admin(1, "admin", admin_password)

@login_manager.user_loader
def load_user(user_id):
    return admins.get(int(user_id))

# Load model VGG19 menggunakan os.path
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models', 'vgg19_classification_model.h5'))

try:
    model = tf.keras.models.load_model(model_path)
    print(f"Model berhasil dimuat dari: {model_path}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

def preprocess_frame(frame):
    """
    Preprocess frame untuk prediksi dengan model VGG19
    Args:
        frame: Frame dari webcam (BGR format)
    Returns:
        Preprocessed frame siap untuk prediksi
    """
    # Convert BGR to RGB (karena OpenCV menggunakan BGR, tapi model training menggunakan RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Resize ke ukuran yang sama dengan training (224x224)
    resized = cv2.resize(rgb_frame, (224, 224))
    
    # Normalisasi seperti pada training
    normalized = resized / 255.0
    
    # Expand dimensions untuk batch
    expanded = np.expand_dims(normalized, axis=0)
    
    return expanded

# Tambahkan konfigurasi untuk upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder upload ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Proses gambar untuk prediksi
            img = cv2.imread(filepath)
            img = preprocess_frame(img)
            
            # Prediksi
            predictions = model.predict(img)
            classes = ['Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy']
            predicted_class = classes[np.argmax(predictions[0])]
            confidence = float(np.max(predictions[0]) * 100)
            
            # Dictionary solusi (sama seperti sebelumnya)
            solutions = {
                'Potato_Early_blight': [
                    "1. Aplikasikan fungisida yang sesuai dengan dosis yang direkomendasikan",
                    "2. Tingkatkan sirkulasi udara di sekitar tanaman",
                    "3. Hindari penyiraman dari atas daun",
                    "4. Buang daun yang terinfeksi",
                    "5. Rotasi tanaman secara berkala"
                ],
                'Potato_Late_blight': [
                    "1. Aplikasikan fungisida sistemik sesuai anjuran",
                    "2. Tingkatkan sirkulasi udara dengan mengatur jarak tanam",
                    "3. Kurangi kelembaban dengan sistem irigasi tepat",
                    "4. Lakukan sanitasi kebun secara berkala",
                    "5. Hindari penanaman tanaman dalam di sekitar area tanam"
                ],
                'Potato_healthy': [
                    "Tanaman sehat! Lanjutkan perawatan rutin:",
                    "1. Jaga kelembaban tanah yang tepat",
                    "2. Berikan pupuk secara teratur",
                    "3. Pantau hama dan penyakit",
                    "4. Jaga kebersihan area tanam"
                ]
            }
            
            prediction_result = {
                'class': predicted_class,
                'confidence': round(confidence, 2),
                'solutions': solutions[predicted_class],
                'image_path': os.path.join('uploads/', filename)
            }
            
    return render_template('scan.html', prediction=prediction_result)

# Routes untuk admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = next((a for a in admins.values() if a.username == username), None)
        
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        
        flash('Invalid username or password')
    return render_template('admin/login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        pass
    return render_template('admin/dashboard.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# Tambahkan route untuk mengelola dataset (opsional)
@app.route('/admin/dataset', methods=['GET', 'POST'])
@login_required
def manage_dataset():
    if request.method == 'POST':
        # Logic untuk menambah data training
        pass
    return render_template('admin/dataset.html')

if __name__ == '__main__':
    app.run(debug=True)