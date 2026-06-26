# 📦 Panduan Instalasi — Amazon Big Data Pipeline

**Teknologi:** PySpark | MySQL | MongoDB | Streamlit  
**Platform:** Windows (dioptimalkan untuk Windows 10/11)

---

## Daftar Isi

1. [Prasyarat Sistem](#1-prasyarat-sistem)
2. [Instalasi Java (JDK 17)](#2-instalasi-java-jdk-17)
3. [Instalasi Hadoop (Winutils)](#3-instalasi-hadoop-winutils)
4. [Instalasi MySQL](#4-instalasi-mysql)
5. [Instalasi MongoDB](#5-instalasi-mongodb)
6. [Instalasi Python & Dependencies](#6-instalasi-python--dependencies)
7. [Konfigurasi MySQL JDBC Driver](#7-konfigurasi-mysql-jdbc-driver)
8. [Persiapan Dataset](#8-persiapan-dataset)
9. [Konfigurasi Proyek](#9-konfigurasi-proyek)
10. [Menjalankan Pipeline](#10-menjalankan-pipeline)
11. [Menjalankan Dashboard Streamlit](#11-menjalankan-dashboard-streamlit)
12. [Verifikasi Instalasi](#12-verifikasi-instalasi)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Prasyarat Sistem

| Komponen | Versi Minimum | Catatan |
|----------|--------------|---------|
| OS | Windows 10 64-bit | Windows 11 juga didukung |
| RAM | 8 GB | Disarankan 16 GB untuk performa optimal |
| Disk | 5 GB ruang bebas | Untuk dataset, database, dan dependencies |
| Python | 3.9 – 3.11 | PySpark belum sepenuhnya mendukung Python 3.12+ |
| Java (JDK) | 17 | Wajib untuk PySpark |

---

## 2. Instalasi Java (JDK 17)

PySpark membutuhkan Java untuk berjalan. Proyek ini dikonfigurasi untuk **JDK 17**.

### Langkah Instalasi

1. Unduh **JDK 17** dari situs resmi Oracle atau Adoptium:
   - Oracle: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html
   - Adoptium (gratis): https://adoptium.net/temurin/releases/?version=17

2. Jalankan installer dan ikuti langkah-langkahnya. Catat lokasi instalasi, contoh:
   ```
   C:\Program Files\Java\jdk-17.0.11
   ```

3. Tambahkan Environment Variable:
   - Buka **System Properties → Environment Variables**
   - Tambahkan variabel baru di **System Variables**:
     - Nama: `JAVA_HOME`
     - Nilai: `C:\Program Files\Java\jdk-17.0.11`
   - Edit variabel `Path`, tambahkan: `%JAVA_HOME%\bin`

4. Verifikasi instalasi:
   ```bash
   java -version
   ```
   Output yang diharapkan:
   ```
   java version "17.0.11" ...
   ```

> **Catatan:** Lokasi JAVA_HOME sudah dikonfigurasi secara otomatis di notebook (`Amazon_BigData_Pipeline.ipynb`). Sesuaikan path-nya jika berbeda dari default.

---

## 3. Instalasi Hadoop (Winutils)

PySpark di Windows membutuhkan file `winutils.exe` dari Hadoop untuk operasi file sistem.

### Langkah Instalasi

1. Unduh Hadoop 3.3.6 (khusus binary Windows) dari:
   https://github.com/cdarlint/winutils/tree/master/hadoop-3.3.6/bin

2. Buat folder: `C:\hadoop-3.3.6\bin`

3. Salin file `winutils.exe` dan `hadoop.dll` ke folder tersebut.

4. Tambahkan Environment Variable:
   - Nama: `HADOOP_HOME`
   - Nilai: `C:\hadoop-3.3.6`
   - Edit variabel `Path`, tambahkan: `%HADOOP_HOME%\bin`

5. Verifikasi:
   ```bash
   winutils ls C:\
   ```

> **Catatan:** Konfigurasi ini sudah terdapat di notebook dan akan diset otomatis saat cell konfigurasi dijalankan.

---

## 4. Instalasi MySQL

### Langkah Instalasi

1. Unduh **MySQL Community Server 8.x** dari:
   https://dev.mysql.com/downloads/mysql/

2. Jalankan installer, pilih setup type **Developer Default** atau minimal **Server only**.

3. Selama instalasi, atur:
   - Port: `3306` (default)
   - Root password: sesuaikan (atau kosongkan jika untuk development lokal)

4. Pastikan service MySQL berjalan:
   ```bash
   # Di PowerShell atau CMD (sebagai Administrator)
   net start MySQL80
   ```

5. Buat database untuk proyek:
   ```sql
   CREATE DATABASE final_bidat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

> **Catatan:** Pipeline akan membuat tabel `orders`, `monthly_summary`, dan `category_stats` secara otomatis saat dijalankan.

---

## 5. Instalasi MongoDB

### Langkah Instalasi

1. Unduh **MongoDB Community Server 7.x** dari:
   https://www.mongodb.com/try/download/community

2. Jalankan installer, pilih **Complete** setup.

3. Centang opsi **Install MongoDB as a Service** agar MongoDB berjalan otomatis.

4. Secara opsional, install **MongoDB Compass** (GUI) untuk memantau data.

5. Verifikasi MongoDB berjalan di port default `27017`:
   ```bash
   mongosh --eval "db.runCommand({ connectionStatus: 1 })"
   ```

> **Catatan:** Pipeline akan membuat database `final_bidat` dan collection `orders_detail` serta `category_insights` secara otomatis.

---

## 6. Instalasi Python & Dependencies

### Prasyarat: Python 3.9 – 3.11

Unduh dari https://www.python.org/downloads/ jika belum terinstal. Pastikan centang **Add Python to PATH** saat instalasi.

### Buat Virtual Environment (Direkomendasikan)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate
```

### Instalasi Package

```bash
pip install pyspark pymongo mysql-connector-python findspark
```

Untuk dashboard Streamlit:

```bash
pip install streamlit pandas plotly
```

Atau instal semua sekaligus dengan membuat file `requirements.txt`:

```
pyspark
pymongo
mysql-connector-python
findspark
streamlit
pandas
plotly
numpy
```

Lalu jalankan:

```bash
pip install -r requirements.txt
```

### Verifikasi Instalasi Package

```bash
python -c "import pyspark; print('PySpark:', pyspark.__version__)"
python -c "import pymongo; print('PyMongo:', pymongo.__version__)"
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
```

---

## 7. Konfigurasi MySQL JDBC Driver

PySpark membutuhkan JDBC driver untuk menulis data ke MySQL.

### Langkah

1. Unduh **MySQL Connector/J 9.x** dari:
   https://dev.mysql.com/downloads/connector/j/

2. Pilih format **Platform Independent (ZIP)**, ekstrak filenya.

3. Letakkan file `.jar` di lokasi yang mudah diakses, contoh:
   ```
   C:\Users\<username>\BIDAT\mysql-connector-j-9.7.0\mysql-connector-j-9.7.0.jar
   ```

4. Catat path lengkap file `.jar` tersebut — akan dimasukkan ke konfigurasi notebook.

---

## 8. Persiapan Dataset

1. Unduh dataset **Amazon Sale Report** (format `.csv`, ±128.000 baris).

2. Simpan di lokasi yang mudah diakses, contoh:
   ```
   C:\Users\<username>\BIDAT\Amazon Sale Report.csv
   ```

3. Pastikan nama file persis: `Amazon Sale Report.csv` (ada spasi).

---

## 9. Konfigurasi Proyek

Buka file `Amazon_BigData_Pipeline.ipynb` di Jupyter Notebook atau JupyterLab, lalu sesuaikan konfigurasi berikut di **Cell 2 (Setup & Konfigurasi)**:

```python
# ==================== CSV PATH ====================
CSV_PATH = r"C:\Users\<username>\BIDAT\Amazon Sale Report.csv"

# ==================== MySQL CONFIG ====================
MYSQL_HOST     = "localhost"
MYSQL_PORT     = 3306
MYSQL_USER     = "root"
MYSQL_PASSWORD = ""  # Isi dengan password MySQL Anda

# ==================== JDBC JAR PATH ====================
POSSIBLE_JDBC_PATHS = [
    r"C:\Users\<username>\BIDAT\mysql-connector-j-9.7.0\mysql-connector-j-9.7.0.jar",
]

# ==================== MongoDB CONFIG ====================
MONGO_URI      = "mongodb://localhost:27017/"
MONGO_DATABASE = "final_bidat"
```

> Ganti `<username>` dengan nama user Windows Anda.

Sesuaikan juga path Java dan Hadoop di **Cell 3** jika berbeda:

```python
JAVA_HOME = r"C:\Program Files\Java\jdk-17.0.11"
os.environ["HADOOP_HOME"] = r"C:\hadoop-3.3.6"
```

---

## 10. Menjalankan Pipeline

1. Pastikan MySQL dan MongoDB sudah berjalan.

2. Aktifkan virtual environment (jika menggunakan):
   ```bash
   venv\Scripts\activate
   ```

3. Buka Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. Buka file `Amazon_BigData_Pipeline.ipynb`.

5. Jalankan cell satu per satu secara berurutan (dari atas ke bawah):
   - Cell 1 — Install dependencies
   - Cell 2 — Setup & konfigurasi
   - Cell 3 — Konfigurasi Java & Hadoop
   - Cell 4 — Inisialisasi PySpark Session
   - Cell 5 dst. — Pipeline data (ingestion → cleaning → processing → write to DB)

> **Penting:** Jangan jalankan semua cell sekaligus (`Kernel > Run All`) — jalankan bertahap untuk memantau log setiap tahap.

---

## 11. Menjalankan Dashboard Streamlit

Dashboard membaca data dari folder `streamlit_data/` yang dibuat otomatis oleh pipeline notebook.

**Pastikan pipeline notebook sudah selesai dijalankan sebelum membuka dashboard.**

```bash
# Dari direktori yang sama dengan file app.py
streamlit run app.py
```

Dashboard akan terbuka otomatis di browser pada alamat:
```
http://localhost:8501
```

### Struktur Data yang Dibutuhkan Dashboard

Pipeline akan menghasilkan folder `streamlit_data/` dengan file-file berikut:

```
streamlit_data/
├── summary.json
├── category_stats.json
├── monthly_summary.json
├── order_status.json
├── top_states.json
├── b2b_b2c.json
├── heatmap_data.json
├── mom_growth.json
└── price_segments.json
```

Jika folder ini belum ada, dashboard akan menampilkan mode demo.

---

## 12. Verifikasi Instalasi

Jalankan checklist berikut untuk memastikan semua komponen siap:

```bash
# Java
java -version

# Python
python --version

# PySpark
python -c "from pyspark.sql import SparkSession; s=SparkSession.builder.getOrCreate(); print('Spark OK:', s.version); s.stop()"

# MySQL (pastikan service berjalan)
mysql -u root -e "SHOW DATABASES;" 2>nul

# MongoDB (pastikan service berjalan)
mongosh --eval "db.adminCommand('ping')"

# Streamlit
streamlit --version
```

---

## 13. Troubleshooting

### ❌ `JAVA_HOME` tidak dikenali
Pastikan variabel environment sudah diatur dengan benar dan **restart terminal** atau komputer setelah mengubah environment variable.

### ❌ PySpark worker crash / `Python worker failed to connect back`
Proyek ini sudah dikonfigurasi dengan `local[2]` dan memory limit untuk menghindari crash. Jika masih terjadi:
- Tutup aplikasi berat lainnya untuk membebaskan RAM.
- Pastikan `PYSPARK_PYTHON` mengarah ke Python yang sama dengan environment aktif.

### ❌ `winutils.exe` error
Pastikan file `winutils.exe` ada di `C:\hadoop-3.3.6\bin\` dan HADOOP_HOME sudah diset dengan benar.

### ❌ MySQL connection refused
- Pastikan service MySQL berjalan: `net start MySQL80`
- Periksa port tidak diblokir firewall.
- Pastikan password di konfigurasi notebook sesuai.

### ❌ `streamlit_data/` tidak ditemukan
Jalankan seluruh pipeline di notebook terlebih dahulu hingga selesai. File JSON akan dibuat otomatis di akhir pipeline.

### ❌ Arrow serialization warning di PySpark
Sudah dinonaktifkan di konfigurasi SparkSession (`arrow.pyspark.enabled = false`). Warning ini aman diabaikan.

---

## Struktur Direktori Proyek

```
📁 Proyek/
├── Amazon_BigData_Pipeline.ipynb   ← Notebook pipeline utama
├── app.py                          ← Dashboard Streamlit
├── requirements.txt                ← Daftar dependencies Python
├── instalasi.md                    ← Panduan instalasi ini
├── 📁 streamlit_data/              ← Dibuat otomatis oleh pipeline
│   ├── summary.json
│   ├── category_stats.json
│   └── ... (8 file JSON lainnya)
└── 📁 checkpoint/                  ← Dibuat otomatis oleh PySpark
```

---

*Panduan ini dibuat untuk proyek Big Data — Mata Kuliah Big Data, Institut Teknologi Del.*
