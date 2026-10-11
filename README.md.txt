   # Python Brute Force Tool

   Script otomatisasi pengujian keamanan (brute force) sederhana menggunakan Python. Tool ini mendukung ekstraksi token CSRF dan eksekusi multi-threading untuk efisiensi.

   ## ⚠️ Disclaimer
   Tool ini dibuat semata-mata untuk **tujuan edukasi** dan **pengujian keamanan yang sah (authorized penetration testing)**. Penulis tidak bertanggung jawab atas segala bentuk penyalahgunaan tool ini terhadap sistem yang tidak dimiliki atau tidak diizinkan oleh pemiliknya.

   ## 🚀 Fitur
   - Mendukung ekstraksi token CSRF (anti-CSRF bypass).
   - Multi-threading untuk eksekusi cepat.
   - Auto-stop pada user tertentu jika password ditemukan (hemat waktu & resource).
   - Command Line Interface (CLI) yang fleksibel.

   ## 📦 Instalasi
   1. Clone atau download repository ini.
   2. Install dependencies yang dibutuhkan:
      ```bash
      pip install -r requirements.txt
      ```

   ## 💻 Cara Penggunaan
   Jalankan script melalui terminal dengan argumen berikut:

   ```bash
   python brutal.py -u <URL_TARGET> -w <FILE_WORDLIST> -U <USER1> <USER2> -t <JUMLAH_THREAD> --token <NAMA_TOKEN>