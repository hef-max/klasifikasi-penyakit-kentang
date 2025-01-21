# Potato Leaf Disease Classification

Proyek ini adalah aplikasi berbasis Flask yang menggunakan model VGG19 untuk mengklasifikasikan penyakit pada daun kentang. Aplikasi ini memungkinkan pengguna untuk mengunggah gambar daun kentang dan mendapatkan prediksi penyakit serta rekomendasi solusi penanganannya.

## 📂 Struktur Folder

```
├── app/
│   ├── models/vgg19_classification_model.h5  # File model klasifikasi
│   ├── static/
│   │   └── uploads/        # Folder untuk menyimpan gambar yang diunggah pengguna
│   ├── templates/
│   │   └── admin/          # Template HTML untuk admin
│   └── __pycache__/        # Folder cache Python
├── app.py                  # Entry point aplikasi Flask
├── requirements.txt        # Daftar dependensi Python
├── README.md               # Dokumentasi proyek
├── .gitignore               # File untuk mengecualikan file tertentu dari repository Git
```

## 🚀 Fitur

- **Klasifikasi Penyakit:** Mendeteksi penyakit daun kentang menggunakan model VGG19.
- **Unggah Gambar:** Pengguna dapat mengunggah gambar untuk diprediksi.
- **Hasil Prediksi:** Menampilkan hasil prediksi beserta tingkat kepercayaan.
- **Saran Perawatan:** Menampilkan solusi berdasarkan hasil prediksi.
- **Autentikasi Admin:** Halaman login untuk administrator.
- **Dashboard Admin:** Mengelola data dan melihat laporan.

## 🛠️ Instalasi dan Menjalankan Aplikasi

1. **Clone repository:**
   ```bash
   git clone https://github.com/username/potato-disease-classification.git
   cd potato-disease-classification
   ```

2. **Buat dan aktifkan virtual environment (opsional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk macOS/Linux
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi:**
   ```bash
   python app.py
   ```

5. **Akses aplikasi di browser:**
   ```
   http://127.0.0.1:5000
   ```

## 📷 Cara Penggunaan

1. Buka aplikasi di browser.
2. Unggah gambar daun kentang melalui halaman utama.
3. Klik tombol "Prediksi".
4. Lihat hasil prediksi dan solusi yang direkomendasikan.

## 🏗️ Teknologi yang Digunakan

- **Flask** – Framework web untuk Python
- **TensorFlow/Keras** – Untuk model deep learning VGG19
- **OpenCV** – Untuk pemrosesan gambar
- **Werkzeug** – Untuk keamanan dan manajemen file
- **Flask-Login** – Untuk autentikasi pengguna
- **HTML/CSS/Bootstrap** – Untuk tampilan antarmuka

## ⚙️ Konfigurasi

- File konfigurasi dapat disesuaikan dalam `app.py` seperti:

  ```python
  app.config['SECRET_KEY'] = '/@Potato123#'
  app.config['UPLOAD_FOLDER'] = 'static/uploads'
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
  ```

- Pastikan direktori upload tersedia:
  ```python
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  ```

## 🗃️ Data dan Model

- Model yang digunakan: **VGG19**
- Kelas klasifikasi yang didukung:
  - **Potato_Early_blight**
  - **Potato_Late_blight**
  - **Potato_healthy**

## 🔐 Admin Panel

1. Akses admin di: `http://127.0.0.1:5000/admin/login`
2. Gunakan kredensial default:
   - **Username:** `admin`
   - **Password:** `admin123`

## 📜 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Selamat menggunakan aplikasi klasifikasi penyakit daun kentang ini! 🚀

