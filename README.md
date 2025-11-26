# SocialSight Analytics

**Platform Analisis Sosial Media untuk YouTube**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Tentang Proyek

SocialSight Analytics adalah platform analisis media sosial yang dirancang khusus untuk menganalisis data YouTube secara mendalam dan komprehensif. Proyek ini dikembangkan sebagai final project mata kuliah **Workshop Analisis Sosial Media**.

## ✨ Fitur Utama

### 1. **Executive Summary** 📊
- Ringkasan metrik kunci (total video, views, likes, comments)
- Analisis performa channel berdasarkan subscriber
- Breakdown performa kategori konten
- Tren upload dalam 30 hari terakhir
- Key insights otomatis

### 2. **View & Reach Analytics** 👁️
- Distribusi views across videos
- Analisis tren pertumbuhan views harian dan kumulatif
- Deteksi view spikes otomatis
- Analisis performa per channel
- Metrik reach dan penetrasi audience

### 3. **Engagement Analytics** ❤️
- Metrik engagement komprehensif (likes, comments, engagement rate)
- Perbandingan likes vs comments
- Top performing videos by engagement
- Korelasi engagement vs views
- Analisis durasi video terhadap engagement

### 4. **Content Analysis** 📝
- Analisis frekuensi upload berdasarkan hari
- Performa kategori konten
- Identifikasi best time to post
- Top 10 performing posts dengan cards menarik
- Metrik hashtag dan karakteristik konten

### 5. **Sentiment & Comment Analysis** 💬
- Analisis sentimen komentar (Positive, Negative, Neutral)
- Normalisasi teks dan slang language processing
- Identifikasi kata-kata paling sering muncul
- Tren sentimen over time
- Comment-level analysis dengan detail

### 6. **Topic Analysis** 🏷️
- Non-Negative Matrix Factorization (NMF) untuk topic modeling
- Word cloud dari judul video
- Distribusi video per topic
- Top videos per topic dengan confidence score
- Analisis performa per topic

### 7. **Data Explorer** 📂
- Filter data by channel, kategori, dan views
- Numeric summary statistics
- Category breakdown analysis
- Custom column selection untuk data table
- Export data dalam format CSV dan Excel

## 🚀 Cara Penggunaan

### Prerequisites
```bash
Python 3.8+
pip
```

### Instalasi

1. Clone repository
```bash
git clone https://github.com/username/socialsight-analytics.git
cd socialsight-analytics
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Download model sentiment analysis (jika belum tersedia)
```bash
# Letakkan model sentiment di folder: ./models/sentiment_analysis/
```

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📁 Struktur Proyek

```
socialsight-analytics/
├── app.py                          # Main application
├── requirements.txt                # Dependencies
├── utils/
│   ├── styles.py                   # Custom CSS styling
│   ├── helpers.py                  # Helper functions
│   └── sidebar.py                  # Sidebar navigation
├── modules/
│   ├── executive_summary.py        # Executive summary page
│   ├── engagement_analytics.py     # Engagement analytics page
│   ├── content_analysis.py         # Content analysis page
│   ├── view_reach_analytics.py     # View & reach analytics page
│   ├── sentiment_comment_analysis.py # Sentiment analysis page
│   ├── topic_analysis.py           # Topic modeling page
│   └── data_explorer.py            # Data explorer page
├── models/
│   ├── sentiment_analysis/         # Pre-trained sentiment model
│   └── topic_modeling/             # NMF model files
├── data/
│   ├── combined_stop_words.txt     # Stopword mappings
│   ├── informal_formal_1.csv       # Slang dictionary 1
│   ├── informal_formal_2.txt       # Slang dictionary 2
│   └── update_combined_slang_words.txt # Slang dictionary 3
└── README.md
```

## 📊 Format Data Input

Aplikasi menerima file CSV atau Excel dengan struktur kolom sebagai berikut:

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| Video ID | String | ID unik video |
| Judul | String | Judul video |
| Tanggal Upload | Date | Tanggal upload (format: YYYY-MM-DD atau ISO) |
| Channel | String | Nama channel |
| Country | String | Kode negara |
| Subscribers | Integer | Jumlah subscriber channel |
| Total Video Cha Tags | String | Tags video (comma-separated) |
| Kategori | String | Kategori konten |
| Views | Integer | Total views |
| Likes | Integer | Total likes |
| Comments | Integer | Total comments |
| Durasi | String | Durasi video (format: PT5M30S) |
| Definition | String | Kualitas video (hd/sd) |
| Dimension | String | Dimensi video (2d/3d) |
| Komentar Lengkap | String | Daftar komentar (untuk sentiment analysis) |

## 🛠️ Teknologi yang Digunakan

- **Streamlit** - Web framework untuk data apps
- **Pandas** - Data manipulation dan analysis
- **Plotly** - Interactive visualizations
- **Scikit-learn** - Machine learning (NMF topic modeling)
- **Transformers** - Pre-trained models untuk sentiment analysis
- **WordCloud** - Visualization word frequency
- **NumPy** - Numerical computing

## 📈 Analisis yang Dilakukan

### Engagement Metrics
- Engagement Rate: (Likes + Comments) / Views × 100%
- Likes Rate: Likes / Views × 100%
- Comment Rate: Comments / Views × 100%
- Engagement Quality: Likes / (Comments + 1)

### Content Performance
- Best Time to Post (berdasarkan engagement rate)
- Top Performing Content Categories
- View Distribution Analysis
- Upload Frequency Patterns

### Sentiment Analysis
- Natural Language Processing untuk preprocessing teks
- Normalisasi slang language Indonesia
- Classification: Positive, Negative, Neutral
- Trend sentimen over time

### Topic Modeling
- Non-Negative Matrix Factorization (NMF)
- Automatic topic extraction
- Topic distribution per video
- Confidence scoring

## 👥 Tim Pengembang

Proyek ini adalah hasil kolaborasi tim untuk mata kuliah **Workshop Analisis Sosial Media**

## 📝 Catatan Penting

1. **Data Privacy**: Pastikan dataset yang diupload sudah mendapatkan izin dari pemilik
2. **Model Sentiment**: Model sentiment analysis menggunakan bahasa Indonesia dan memerlukan preprocessing
3. **File Size**: Rekomendasikan dataset tidak lebih dari 100,000 records untuk performa optimal
4. **Encoding**: File CSV sebaiknya menggunakan encoding UTF-8 untuk kompatibilitas terbaik

## 🐛 Troubleshooting

### Error: "Model not loaded"
Solusi: Pastikan folder `./models/sentiment_analysis/` dan `./models/topic_modeling/` sudah tersedia dengan file model yang lengkap

### Error: "Column not found"
Solusi: Pastikan nama kolom di dataset sesuai dengan yang diharapkan aplikasi. Perhatikan huruf besar-kecil (case-sensitive)

### Error: "UnicodeDecodeError"
Solusi: Cek encoding file CSV. Aplikasi akan mencoba utf-8, latin-1, dan cp1252 secara otomatis

---

**Dikembangkan untuk Workshop Analisis Sosial Media** ✨

Terakhir diupdate: 2025
