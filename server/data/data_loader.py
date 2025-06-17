
import json
import os

def load_vocabulary():
    """Load vocabulary from JSON file, generate if doesn't exist"""
    vocab_file = 'data/vocabulary.json'
    
    # Check if vocabulary.json exists, if not generate it
    if not os.path.exists(vocab_file):
        print("Vocabulary file not found. Generating from attached assets...")
        from data.vocabulary_builder import generate_vocabulary
        generate_vocabulary()
    
    try:
        with open(vocab_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        return {}

def load_articles():
    """Load articles from JSON file"""
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_vocabulary(vocabulary):
    """Save vocabulary to JSON file"""
    with open('data/vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=4)

def save_articles(articles):
    """Save articles to JSON file"""
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def add_vocabulary_word(german_word, english_translation):
    """Add a new vocabulary word"""
    vocabulary = load_vocabulary()
    vocabulary[german_word] = english_translation
    save_vocabulary(vocabulary)

def add_article(title, content, difficulty, category, date=None):
    """Add a new article"""
    from datetime import datetime
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    articles = load_articles()
    new_article = {
        "title": title,
        "content": content,
        "date": date,
        "difficulty": difficulty,
        "category": category
    }
    articles.append(new_article)
    save_articles(articles)
