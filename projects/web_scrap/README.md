# 🧠 YouTube Comment Scraper with Sentiment Analysis

Scraping komentar dari YouTube video menggunakan YouTube Data API v3, lalu melakukan analisis keyword, sentimen, dan visualisasi data seperti wordcloud & tren waktu.

---

## 📌 Fitur

- ✅ Scraping komentar dari satu video YouTube
- 🔍 Filter komentar berdasarkan **keyword** tertentu (contoh: RUU TNI)
- 💬 Analisis **sentimen komentar** (positif / negatif / netral)
- 🌥️ Wordcloud dari teks komentar
- 📈 Visualisasi **tren komentar harian**
- 🚫 Deteksi komentar spam & duplikat
- 📁 Ekspor ke file CSV

---

## 🚀 Cara Menjalankan

### 1. Clone repositori ini:
```bash
git clone https://github.com/Boekanadip/web_scrap.git
cd youtube-comment-scraper
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Jalankan script:
Edit `API_KEY` dan `VIDEO_ID` di dalam script utama, lalu jalankan:
```bash
python main.py
```

---

## 🛠️ Teknologi yang Digunakan

- Python 3
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- Pandas
- TextBlob
- Matplotlib
- WordCloud
- Google API Client

---

## 📄 Output

- File `youtube_filtered_comments.csv` berisi hasil komentar yang sudah difilter dan dianalisis.
- Gambar wordcloud dan tren komentar ditampilkan dengan `matplotlib`.

---

## 🔑 API Key

Untuk menggunakan YouTube Data API:
1. Masuk ke [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru
3. Aktifkan **YouTube Data API v3**
4. Buat API Key dan salin ke variabel `API_KEY` di script

---

## 📬 Kontak

Dikembangkan oleh [Adib Raihan Ashidiq]  
Email: adib.raihann@gmail.com  
GitHub: (https://github.com/Boekanadip)
