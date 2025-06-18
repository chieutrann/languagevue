import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from main import GermanDictionary

# def get_example_other_language(word, src_lang: str = "de", lang_dest: str = "en"):
#     """Get example sentences for a word from Glosbe"""
#     try:
#         url = f"https://glosbe.com/{src_lang}/{lang_dest}/{word}"
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # Correctly handle class lists
#         # Get all <p> elements with specific classes
#         german_paragraphs = soup.find_all("p", class_="w-1/2 dir-aware-pr-1")
#         target_paragraphs = soup.find_all("p", class_="w-1/2 px-1 ml-2")

#         pairs = []
#         for de, target in zip(german_paragraphs, target_paragraphs):
#             de_text = de.get_text(separator=" ", strip=True)
#             target_text = target.get_text(separator=" ", strip=True)
#             pairs.append({
#                 "sentence": de_text,
#                 "translation": target_text
#             })
            
#         return pairs
#     except Exception as e:
#         print(f"Error getting example sentences for '{word}': {e}")
#         return []
    



# app = Flask(__name__)

# @app.route('/api/dictionary/examples-other', methods=['GET'])
# def examples_other():
#     word = request.args.get('word').strip()
#     language = request.args.get('language', 'de')
#     target_language = request.args.get('target_language', 'en')
    
#     if not word:
#         return jsonify({'error': 'No word provided'}), 400
        
#     examples = get_example_other_language(word, language, target_language)
#     return jsonify(examples)

def get_audio_url( word):
        """Get audio URL for a word from DWDS"""
        url = f"https://www.dwds.de/wb/{word}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            audio_tag = soup.find("audio")
            if audio_tag:
                source = audio_tag.find("source")
                if source and source.get("src"):
                    audio_url = source["src"]
                    # Ensure URL is absolute
                    if not audio_url.startswith('http'):
                        audio_url = f"https://www.dwds.de{audio_url}"
                    return audio_url
            return None
            
        except Exception as e:
            print(f"Audio URL fetch error for '{word}': {e}")
            return None



print(get_audio_url("Haus"))


