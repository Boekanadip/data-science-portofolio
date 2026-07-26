import streamlit as st
import sys
import os

# Tambahkan path untuk import
sys.path.insert(0, os.path.dirname(__file__))

from app.predict import predict
from app.decision import make_decision
from keyword_extract import extract_keywords, create_search_query
from news_search_v2 import search_news_multi_source, format_news_results

# Konfigurasi halaman
st.set_page_config(
    page_title="Deteksi Berita Hoaks",
    page_icon="🔍",
    layout="wide"
)

# CSS Custom untuk indikator visual
st.markdown("""
<style>
    .confidence-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .very-high {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .medium {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }
    .low {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
    }
    .disclaimer-box {
            padding: 15px;
            border-left: 4px solid #ff9800;
            background-color: #fff3e0;
            margin: 20px 0;
            border-radius: 5px;
            color: #000000;  /* ← TAMBAHKAN INI */
    }
    .news-card {
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin: 10px 0;
        background-color: #ffffff;  /* ← Putih penuh */
        color: #000000;  /* ← Teks hitam */
    }
    .news-card h4 {
        color: #1a1a1a;  /* ← Judul gelap */
    }
    .news-card p {
        color: #333333;  /* ← Isi gelap */
    }
    .news-card a {
        color: #1976d2;  /* ← Link biru */
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Deteksi Berita Hoaks")
st.markdown("Sistem deteksi berita hoaks dengan fitur pencarian referensi berita otomatis.")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Tentang Sistem")
    st.markdown("""
    **Fitur:**
    - 🎯 Deteksi hoaks berita bahasa Indonesia
    - 📊 Indikator kepastian visual
    - 📰 Pencarian berita referensi otomatis
    - ⚠️ Peringatan untuk prediksi tidak pasti
    
    **Cara Kerja:**
    1. Masukkan teks berita
    2. Sistem akan menganalisis
    3. Tampilkan hasil + referensi berita
    """)
    
    st.divider()
    
    # Opsi advanced
    st.header("⚙️ Pengaturan")
    auto_search = st.checkbox("Pencarian Berita Otomatis", value=True)

# Input teks
st.header("📝 Input Berita")
text_input = st.text_area(
    "Masukkan teks berita yang ingin dianalisis:",
    height=200,
    placeholder="Contoh: Pemerintah mengumumkan kebijakan baru tentang..."
)

# Tombol prediksi
if st.button("🔍 Analisis Berita", type="primary", use_container_width=True):
    if not text_input.strip():
        st.error("❌ Mohon masukkan teks berita terlebih dahulu!")
    else:
        with st.spinner("🤖 Menganalisis berita..."):
            # Prediksi
            pred = predict(text_input)
            decision = make_decision(pred)
            
            # Extract keywords untuk pencarian
            keywords = extract_keywords(text_input, top_n=3)
            search_query = create_search_query(keywords)
        
        st.divider()
        
        # HASIL PREDIKSI
        st.header("📊 Hasil Analisis")
        
        # Confidence level indicator
        confidence = pred['confidence']
        
        if confidence >= 0.80:
            conf_class = "very-high"
            conf_emoji = "🟢"
            conf_text = "Sangat Yakin"
        elif confidence >= 0.65:
            conf_class = "high"
            conf_emoji = "🟡"
            conf_text = "Yakin"
        elif confidence >= 0.50:
            conf_class = "medium"
            conf_emoji = "🟠"
            conf_text = "Cukup Yakin"
        else:
            conf_class = "low"
            conf_emoji = "🔴"
            conf_text = "Kurang Yakin"
        
        # Display confidence box
        tingkat_kepastian = confidence * 100
        tingkat_keraguan = 100 - tingkat_kepastian

        st.markdown(f"""
                    <div class="confidence-box {conf_class}">
                    {conf_emoji} Tingkat Kepastian: {conf_text} ({tingkat_kepastian:.1f}%)<br>
                    ❓ Tingkat Keraguan: ({tingkat_keraguan:.1f}%)
                    </div>
                    """, 
                unsafe_allow_html=True)

        
        # Keputusan
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Keputusan", decision)
        
        with col2:
            st.metric("Probabilitas Valid", f"{pred['p_hoaks']*100:.2f}%")
        
        with col3:
            st.metric("Probabilitas Hoaks", f"{pred['p_valid']*100:.2f}%")
        
        # Disclaimer jika confidence rendah
        if confidence < 0.65:
            st.markdown(f"""
            <div class="disclaimer-box">
                ⚠️ <b>Perhatian:</b> Sistem kurang yakin dengan prediksi ini (confidence: {confidence*100:.1f}%).
                <br><br>
                <b>Rekomendasi:</b>
                <ul>
                    <li>Cek sumber berita asli</li>
                    <li>Bandingkan dengan berita dari media terpercaya</li>
                    <li>Lihat referensi berita terkait di bawah</li>
                    <li>Jangan langsung percaya atau menyebarkan</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # PENCARIAN BERITA TERKAIT
        if auto_search:
            st.header("📰 Referensi Berita Terkait")
            st.markdown(f"**Keyword pencarian:** _{', '.join(keywords)}_")
            
            with st.spinner("🔍 Mencari berita terkait di Google News..."):
                news_results = search_news_multi_source(search_query, max_results=5)
            
            if news_results:
                st.success(f"✅ Ditemukan {len(news_results)} berita terkait:")
                
                for i, news in enumerate(news_results, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="news-card">
                            <h4>{i}. {news['title']}</h4>
                            <p>📰 <b>Sumber:</b> {news['source']}</p>
                            <p>🔗 <a href="{news['url']}" target="_blank">Baca Selengkapnya</a></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if news['snippet']:
                            st.markdown(f"_{news['snippet'][:200]}..._")
                        
                        st.markdown("")
                
                st.info("💡 **Tips:** Cross-check informasi dengan membaca beberapa sumber berita terpercaya di atas.")
            else:
                st.warning("⚠️ Tidak ditemukan berita terkait. Coba dengan teks yang lebih spesifik atau kata kunci yang berbeda.")
        else:
            st.info("ℹ️ Pencarian berita otomatis dinonaktifkan. Aktifkan di sidebar untuk melihat referensi berita.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>⚠️ <b>Disclaimer:</b> Sistem ini adalah alat bantu. Selalu verifikasi dari sumber terpercaya.</p>
    <p>Dibuat dengan menggunakan Streamlit & PyTorch</p>
</div>
""", unsafe_allow_html=True)
