import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify


def get_example_other_language(word, src_lang: str = "de", lang_dest: str = "en"):
    """Get example sentences for a word from Glosbe"""
    try:
        url = f"https://glosbe.com/{src_lang}/{lang_dest}/{word}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Correctly handle class lists
        # Get all <p> elements with specific classes
        german_paragraphs = soup.find_all("p", class_="w-1/2 dir-aware-pr-1")
        target_paragraphs = soup.find_all("p", class_="w-1/2 px-1 ml-2")

        pairs = []
        for de, target in zip(german_paragraphs, target_paragraphs):
            de_text = de.get_text(separator=" ", strip=True)
            target_text = target.get_text(separator=" ", strip=True)
            pairs.append({
                "sentence": de_text,
                "translation": target_text
            })
            
        return pairs
    except Exception as e:
        print(f"Error getting example sentences for '{word}': {e}")
        return []
    



app = Flask(__name__)

@app.route('/api/dictionary/examples-other', methods=['GET'])
@app.route('/api/dictionary/examples-other')
def examples_other():
    word = request.args.get('word').strip()
    language = request.args.get('language', 'de')
    target_language = request.args.get('target_language', 'en')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
        
    examples = get_example_other_language(word, language, target_language)
    return jsonify(examples)


print(get_example_other_language("Haus", "de", "en"))