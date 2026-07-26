"""
News Search dengan Multiple Fallback
"""
import requests
from bs4 import BeautifulSoup
import time

def search_bing_news(query, max_results=5):
    """
    Search berita dari Bing News (lebih reliable dari Google)
    """
    results = []
    
    try:
        # URL Bing News search
        encoded_query = requests.utils.quote(query)
        url = f"https://www.bing.com/news/search?q={encoded_query}&FORM=HDRSC6"
        
        print(f"DEBUG - Bing URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG - Bing Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Bing news cards
            articles = soup.find_all('div', class_='news-card')
            
            if not articles:
                # Fallback: cari dengan class lain
                articles = soup.find_all('div', attrs={'data-card': True})
            
            print(f"DEBUG - Found {len(articles)} Bing articles")
            
            for article in articles[:max_results]:
                try:
                    # Title dan link
                    title_elem = article.find('a', class_='title')
                    if not title_elem:
                        title_elem = article.find('a')
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    # Source
                    source_elem = article.find('span', class_='source')
                    if not source_elem:
                        source_elem = article.find('div', class_='source')
                    source = source_elem.get_text(strip=True) if source_elem else "Unknown"
                    
                    # Snippet
                    snippet_elem = article.find('div', class_='snippet')
                    if not snippet_elem:
                        snippet_elem = article.find('p')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'source': source,
                            'url': link,
                            'snippet': snippet
                        })
                
                except Exception as e:
                    print(f"DEBUG - Error parsing article: {e}")
                    continue
        
    except Exception as e:
        print(f"DEBUG - Bing search error: {e}")
    
    return results


def search_duckduckgo_news(query, max_results=5):
    """
    Search dari DuckDuckGo News (alternatif lain)
    """
    results = []
    
    try:
        url = f"https://duckduckgo.com/?q={requests.utils.quote(query)}&iar=news&ia=news"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG - DuckDuckGo Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            
            print(f"DEBUG - Found {len(articles)} DDG articles")
            
            for article in articles[:max_results]:
                try:
                    title_elem = article.find('h2')
                    link_elem = article.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        results.append({
                            'title': title,
                            'source': 'Various',
                            'url': link,
                            'snippet': ''
                        })
                
                except Exception as e:
                    continue
    
    except Exception as e:
        print(f"DEBUG - DDG search error: {e}")
    
    return results


def create_fake_news_for_demo(query):
    """
    Fallback: Buat berita dummy untuk demo jika semua scraping gagal
    """
    return [
        {
            'title': f'Berita terkait: {query} - Artikel 1',
            'source': 'Contoh Media',
            'url': 'https://www.detik.com',
            'snippet': 'Ini adalah contoh berita karena scraping sedang tidak tersedia. Silakan cari manual di Google News.'
        },
        {
            'title': f'Berita terkait: {query} - Artikel 2',
            'source': 'Contoh Media',
            'url': 'https://www.kompas.com',
            'snippet': 'Untuk hasil lebih akurat, silakan search manual dengan keyword yang ditampilkan.'
        }
    ]


def search_news_multi_source(query, max_results=5):
    """
    Coba multiple sources dengan fallback
    """
    print(f"\n=== SEARCHING NEWS: {query} ===")
    
    # Try 1: Bing News
    print("Trying Bing News...")
    results = search_bing_news(query, max_results)
    
    if results:
        print(f"✓ Success with Bing: {len(results)} results")
        return results
    
    # Try 2: DuckDuckGo
    print("Trying DuckDuckGo...")
    results = search_duckduckgo_news(query, max_results)
    
    if results:
        print(f"✓ Success with DuckDuckGo: {len(results)} results")
        return results
    
    # Fallback: Demo data
    print("⚠ All sources failed, using demo data")
    return create_fake_news_for_demo(query)


def format_news_results(news_list):
    """
    Format hasil pencarian berita
    """
    if not news_list:
        return "⚠️ Tidak ada berita terkait yang ditemukan."
    
    formatted = []
    for i, news in enumerate(news_list, 1):
        formatted.append(f"""
**{i}. {news['title']}**
📰 Sumber: {news['source']}
🔗 [Baca Selengkapnya]({news['url']})
""")
        if news['snippet']:
            formatted.append(f"_{news['snippet'][:150]}..._\n")
    
    return '\n'.join(formatted)
