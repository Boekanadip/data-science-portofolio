# 🛍️ Analisis Penjualan E-Commerce

## 📌 Deskripsi
Proyek ini bertujuan untuk menganalisis data transaksi penjualan dari toko e-commerce. Fokus utamanya adalah membersihkan data, menemukan insight seperti produk terlaris, waktu puncak penjualan, dan performa berdasarkan negara atau pelanggan. Data yang digunakan berasal dari dataset publik dan dianalisis menggunakan Python.

## 🎯 Tujuan
- Melakukan pembersihan data (data wrangling & cleaning)
- Menemukan produk paling laku dan pendapatan tertinggi
- Mengidentifikasi waktu-waktu puncak penjualan
- Menyajikan visualisasi yang menarik dari hasil analisis

## 🗂️ Struktur Proyek

```
ecommerce-sales-analysis/
├── data/                  # Dataset mentah dan hasil cleaning
│   └── ecommerce_sales.csv
│
├── notebooks/             # Notebook eksplorasi dan visualisasi
│   └── eda.ipynb
│
├── scripts/               # Script Python untuk pembersihan data
│   └── clean_data.py
│
├── visualizations/        # Output gambar grafik dari notebook
│   └── top_products.png
│
├── README.md              # Penjelasan proyek ini
├── requirements.txt       # Library yang digunakan
├── LICENSE                # Lisensi proyek
└── .gitignore             # File/folder yang tidak perlu di-commit
```

## 🚀 Cara Menjalankan

1. Clone repositori:
   ```bash
   git clone https://github.com/username/ecommerce-sales-analysis.git
   cd ecommerce-sales-analysis
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan Jupyter Notebook:
   ```bash
   jupyter notebook notebooks/eda.ipynb
   ```

## 📚 Teknologi
- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Jupyter Notebook

## 🖼️ Contoh Output Visualisasi
- 📊 Top Produk Terlaris
- ⏰ Jam Puncak Transaksi
- 💸 Produk dengan Pendapatan Tertinggi

> Gambar visualisasi disimpan di dalam folder `visualizations/`.

## 📄 Lisensi
Proyek ini dilindungi oleh **MIT License**. Silakan gunakan, modifikasi, dan kontribusi sesuai kebutuhan.

---

💡 Proyek ini dapat dikembangkan lebih lanjut dengan segmentasi pelanggan (RFM), analisis prediktif, dan dashboard interaktif menggunakan Streamlit atau Tableau.
