"""
Keyword Extraction untuk pencarian berita
"""
import re
from collections import Counter

def extract_keywords(text, top_n=3):
    """
    Extract keyword penting dari teks untuk pencarian berita
    
    Args:
        text: Input teks berita
        top_n: Jumlah keyword yang diambil (default 3)
    
    Returns:
        List of keywords
    """
    # Stopwords bahasa Indonesia (simplified)
    stopwords = {
        'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan', 'untuk',
        'pada', 'adalah', 'oleh', 'akan', 'telah', 'atau', 'dalam', 'juga',
        'ada', 'tidak', 'dapat', 'sudah', 'bisa', 'hanya', 'maka', 'jika',
        'karena', 'saat', 'ketika', 'setelah', 'sebelum', 'agar', 'supaya',
        'sebagai', 'tentang', 'antara', 'selama', 'melalui', 'bagi', 'oleh',
        'tersebut', 'hal', 'mereka', 'kami', 'kita', 'saya', 'anda', 'ia',
        'dia', 'nya', 'mu', 'ku', 'kah', 'lah', 'pun', 'per', 'ya', 'tapi',
        'namun', 'tetapi', 'ataupun', 'sedangkan', 'bahwa', 'hingga', 'sambil'
    }
    
    # Lowercase dan ambil kata
    text_lower = text.lower()
    
    # Hapus tanda baca kecuali spasi
    text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
    
    # Split menjadi kata-kata
    words = text_clean.split()
    
    # Filter: minimal 3 karakter, bukan stopword, bukan angka
    meaningful_words = [
        word for word in words 
        if len(word) >= 3 
        and word not in stopwords 
        and not word.isdigit()
    ]
    
    # Hitung frekuensi
    word_freq = Counter(meaningful_words)
    
    # Ambil top N keywords
    top_keywords = [word for word, _ in word_freq.most_common(top_n)]
    
    # Jika kurang dari top_n, ambil semua yang ada
    if len(top_keywords) < top_n and len(meaningful_words) > 0:
        # Ambil beberapa kata pertama yang meaningful
        additional = [w for w in meaningful_words if w not in top_keywords]
        top_keywords.extend(additional[:top_n - len(top_keywords)])
    
    return top_keywords[:top_n]


def create_search_query(keywords):
    """
    Membuat query pencarian dari keywords
    
    Args:
        keywords: List of keywords
    
    Returns:
        String query untuk pencarian
    """
    return ' '.join(keywords)
