# Azyroth Framework 🚀

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Framework web Python modern yang elegan dan powerful, dirancang dengan inspirasi dari keanggunan dan produktivitas [Laravel](https://laravel.com/). Azyroth menyediakan fondasi yang kokoh untuk membangun aplikasi web yang luar biasa dengan arsitektur yang bersih dan performa yang optimal.

---

## ✨ Fitur Utama

-   **Struktur Proyek Elegan**: Arsitektur direktori yang terorganisir, memisahkan logika aplikasi, konfigurasi, dan rute dengan jelas.
-   **CLI Tooling `azyroth`**: Dilengkapi dengan Command-Line Interface yang powerful untuk mempercepat pengembangan (membuat proyek, controller, migrasi, dll.).
-   **ORM & Migrasi**: Dibangun di atas SQLAlchemy dan Alembic untuk interaksi database yang intuitif dan manajemen skema yang mudah.
-   **Routing Sederhana**: Sistem routing yang bersih dan mudah dikelola, terinspirasi dari kesederhanaan Flask dan Laravel.
-   **Service-Oriented**: Mengadopsi konsep *Service Provider* untuk bootstrapping komponen aplikasi secara terorganisir.

---

## ⚙️ Prasyarat

Sebelum memulai, pastikan sistem Anda memiliki:
-   **Python** 3.9+
-   **Git**
-   **MariaDB** atau **MySQL Server**

---

## 📦 Instalasi

Instal Azyroth Framework langsung dari repositori GitHub menggunakan `pip`. Perintah ini akan membuat `azyroth` CLI tersedia di sistem Anda.

```bash
pip install git+[https://github.com/Fikkanel/Azyroth-Framework.git](https://github.com/Fikkanel/Azyroth-Framework.git)
```
---
## 🚀 Panduan Memulai Cepat (Quick Start)
Buat aplikasi pertama Anda hanya dalam beberapa menit.
### 1. Buat Proyek Baru
``` bash
azyroth new nama-project
```

### 2. Masuk ke Direktori Proyek
``` bash 
cd blog-saya
```

### 3. Siapkan Lingkungan (Environment)
Setiap proyek Azyroth membutuhkan virtual environment dan dependensinya sendiri.
```bash
# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate

# Instal dependensi khusus aplikasi
pip install -r requirements.txt
```

### 4. Konfigurasi Database
``` bash
# Salin file environment (di Azyroth v0.1.0+ ini terjadi otomatis)
cp .env.example .env
```

### 5. Jalankan Migrasi Database
``` bash
azyroth db:migrate
```

### Jalankan Server Pengembangan
```bash
python -m public.index
```
---
## 🤝 Berkontribusi
Kontribusi untuk Azyroth sangat kami hargai! Silakan fork repositori ini, buat branch baru untuk fitur atau perbaikan Anda, dan kirimkan Pull Request.

---
## 📜 Lisensi
Azyroth Framework adalah software open-source yang dilisensikan di bawah Lisensi MIT.
EOF


