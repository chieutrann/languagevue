from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
import requests
import json
from datetime import datetime
import re
import asyncio
import random
from data.data_loader import load_vocabulary, load_articles
from dictionary import GermanDictionary
from models import db, SearchedWord, Folder, Vocabulary
import os
from bs4 import BeautifulSoup
from auth import auth_bp, login_required
from flask_cors import CORS
from deep_translator import GoogleTranslator
# secret_key = os
# .environ


# Create Flask app with custom instance path
app = Flask(__name__, 
           static_folder='static',
           instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data'))

# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix='')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'german_dictionary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


    # Initialize database
db.init_app(app)
# Create database tables
with app.app_context():
    db.create_all()

# Initialize dictionary with error handling
try:
    dictionary = GermanDictionary()
except Exception as e:
    print(f"Error initializing dictionary: {e}")
    dictionary = None



# Load data from files
def get_vocabulary():
    return load_vocabulary()


def get_articles():
    return load_articles()


# @app.route('/')
# def index():
#     articles = get_articles()
#     return render_template('index.html', articles=articles)


@app.route('/article/<int:article_id>')
def article_detail(article_id):
    articles = get_articles()
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        vocabulary = get_vocabulary()
        # Highlight vocabulary words in the article
        highlighted_content = highlight_vocabulary(article['content'],
                                                   vocabulary)
        article['highlighted_content'] = highlighted_content
        return render_template('article.html',
                               article=article,
                               vocabulary=vocabulary)
    return "Article not found", 404


@app.route('/vocabulary')
def vocabulary():
    vocabulary_data = get_vocabulary()
    return render_template('vocabulary.html', vocabulary=vocabulary_data)





@app.route('/dictionary')
def dictionary_page():
    return render_template('dictionary.html')



@app.route('/api/dictionary/random')
def random_words():
    count = request.args.get('count', 5, type=int)
    words = dictionary.get_random_words(count)
    return jsonify({'words': words})


@app.route('/api/dictionary/type/<word_type>')
def words_by_type(word_type):
    words = dictionary.get_words_by_type(word_type)
    return jsonify({'type': word_type, 'words': words})


@app.route('/api/dictionary/difficulty/<difficulty>')
def words_by_difficulty(difficulty):
    words = dictionary.get_words_by_difficulty(difficulty)
    return jsonify({'difficulty': difficulty, 'words': words})


@app.route('/api/dictionary/stats')
def dictionary_stats():
    stats = dictionary.get_word_statistics()
    return jsonify(stats)




@app.route('/api/dictionary/conjugate')
def conjugate_verb():
    if not dictionary:
        return jsonify({'error': 'Dictionary not available'}), 500

    verb = request.args.get('verb', '').strip()
    if not verb:
        return jsonify({'error': 'No verb provided'}), 400

    try:
        # Use the new get_conjugations_json method for full conjugation data
        conjugation = dictionary.get_conjugations_json(verb)
        
        # Check if there was an error
        if "error" in conjugation:
            # Fallback to the original method
            conjugation = dictionary.conjugate_verb(verb)
            
        return jsonify({'verb': verb, 'conjugation': conjugation})
    except Exception as e:
        print(f"Error conjugating verb '{verb}': {e}")
        return jsonify({'error': 'Conjugation failed'}), 500

@app.route('/api/dictionary/examples')
def examples():
    word = request.args.get('word').strip()
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    examples = dictionary.get_examples(word)
    return jsonify({'examples': examples})

# // Endpoint to get examples in another language

@app.route('/api/dictionary/examples-other')
def examples_other():
    word = request.args.get('word').strip()
    language = request.args.get('language', 'de')
    target_language = request.args.get('target_language', 'en')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
        
    examples = dictionary.get_example_other_language(word, language, target_language)
    return jsonify(examples)



@app.route('/api/dictionary/autocomplete')
def autocomplete():
    if not dictionary:
        return jsonify({'suggestions': []})

    query = request.args.get('query', '').strip().lower()
    limit = min(request.args.get('limit', 10, type=int),
                20)  # Limit max results

    if not query or len(query) < 1:
        return jsonify({'suggestions': []})

    try:
        suggestions = dictionary.get_autocomplete_suggestions(query, limit)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        print(f"Error getting autocomplete for '{query}': {e}")
        return jsonify({'suggestions': []})


@app.route('/api/dictionary/audio')
def audio():
    word = request.args.get("word")
    if not word:
        return jsonify({'error': 'No word provided'}), 400

    # First check if we have the audio URL in our database
    existing_word = SearchedWord.query.filter_by(word=word).first()
    if existing_word and existing_word.audio_url:
        return jsonify({'audio_url': existing_word.audio_url, 'cached': True})

    # If not in database or no audio URL, fetch from dictionary API
    if not dictionary:
        return jsonify({'error': 'Dictionary not available'}), 500
    
    audio_url = dictionary.get_audio_url(word)
    
    # If we found an audio URL, store it in the database
    if audio_url and existing_word:
        existing_word.audio_url = audio_url
        db.session.commit()
    elif audio_url:
        # If the word doesn't exist in the database yet, create it
        SearchedWord.add_or_update(word=word, audio_url=audio_url)
    
    return jsonify({'audio_url': audio_url, 'cached': False})





def highlight_vocabulary(text, vocabulary):
    """Highlight vocabulary words in the text"""
    highlighted = text
    for german_word in vocabulary.keys():
        # Use word boundaries to match whole words only
        pattern = r'\b' + re.escape(german_word) + r'\b'
        replacement = f'<span class="vocab-word" data-word="{german_word}">{german_word}</span>'
        highlighted = re.sub(pattern,
                             replacement,
                             highlighted,
                             flags=re.IGNORECASE)
    return highlighted


@app.route('/folders')
def folders():
    """Main page showing all folders"""
    folders = Folder.query.all()
    folders_dict = {str(folder.id): folder.to_dict() for folder in folders}
    return render_template('folders.html', folders=folders_dict)

@app.route('/folder/<int:folder_id>')
def folder_view(folder_id):
    """View a specific folder and its vocabularies"""
    folder = Folder.query.get_or_404(folder_id)
    return render_template('folder.html',
                           folder=folder.to_dict(),
                           folder_id=folder_id)

@app.route('/game/<int:folder_id>')
def game_view(folder_id):
    """Game page for a specific folder"""
    folder = Folder.query.get_or_404(folder_id)

    if not folder.vocabularies:
        flash('No vocabularies in this folder to play games', 'warning')
        return redirect(url_for('folder_view', folder_id=folder_id))

    return render_template('game.html',
                           folder=folder.to_dict(),
                           folder_id=folder_id)

@app.route('/api/folders', methods=['GET'])
@login_required
def api_get_folders():
    
    """API endpoint to get all folders"""
    folders = Folder.query.all()
    folders_dict = {str(folder.id): folder.to_dict() for folder in folders}
    return jsonify(folders_dict)

@app.route('/api/folders', methods=['POST'])
@login_required
def api_create_folder():
    lang = request.args.get('lang', )

    """API endpoint to create a new folder"""
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Folder name is required'}), 400


    # Check for duplicate folder names
    existing_folder = Folder.query.filter_by(name=data['name']).first()
    if existing_folder:
        return jsonify({'error': 'already_exists'}), 400


    new_folder = Folder(name=data['name'],
                       description=data.get('description', ''))

    db.session.add(new_folder)
    db.session.commit()

    return jsonify({'id': new_folder.id, 'folder': new_folder.to_dict()}), 201

@app.route('/api/folders/<int:folder_id>', methods=['DELETE'])
@login_required 
def api_delete_folder(folder_id):
    """API endpoint to delete a folder"""
    folder = Folder.query.get_or_404(folder_id)

    db.session.delete(folder)
    db.session.commit()

    return jsonify({'message': 'Folder deleted successfully'})

@app.route('/api/folders/<int:folder_id>/vocabularies', methods=['POST'])
def api_add_vocabulary(folder_id):
    """API endpoint to add vocabulary to a folder"""
    data = request.get_json()

    if not data or 'word' not in data or 'definition' not in data:
        return jsonify({'error': 'Word and definition are required'}), 400

    folder = Folder.query.get_or_404(folder_id)

    # Check for duplicate words in the same folder
    existing_vocab = Vocabulary.query.filter_by(
        folder_id=folder_id, word=data['word']).first()

    if existing_vocab:
        return jsonify({'error': 'Word already exists in this folder'}), 400

    # Try to get audio URL from our dictionary if available
    audio_url = data.get('audio_url', '')
    if not audio_url and dictionary:
        audio_url = dictionary.get_audio_url(data['word'])

    new_vocabulary = Vocabulary(word=data['word'],
                              definition=data['definition'],
                              audio_url=audio_url,
                              image_url=data.get('image_url', ''),
                              folder_id=folder_id)

    db.session.add(new_vocabulary)
    db.session.commit()

    return jsonify({'vocabulary': new_vocabulary.to_dict()}), 201

@app.route('/api/folders/<int:folder_id>/vocabularies/<int:vocab_id>',
           methods=['DELETE'])
def api_delete_vocabulary(folder_id, vocab_id):
    """API endpoint to delete a vocabulary from a folder"""
    vocabulary = Vocabulary.query.filter_by(
        id=vocab_id, folder_id=folder_id).first_or_404()

    db.session.delete(vocabulary)
    db.session.commit()

    return jsonify({'message': 'Vocabulary deleted successfully'})

@app.route('/api/folders/<int:folder_id>/vocabularies/<int:vocab_id>',
           methods=['PUT'])
def api_update_vocabulary(folder_id, vocab_id):
    """API endpoint to update a vocabulary in a folder"""
    data = request.get_json()

    if not data or 'word' not in data or 'definition' not in data:
        return jsonify({'error': 'Word and definition are required'}), 400

    vocabulary = Vocabulary.query.filter_by(
        id=vocab_id, folder_id=folder_id).first_or_404()

    # Check for duplicate words (excluding the current one being updated)
    existing_vocab = Vocabulary.query.filter(
        Vocabulary.folder_id == folder_id,
        Vocabulary.word == data['word'],
        Vocabulary.id != vocab_id).first()

    if existing_vocab:
        return jsonify({'error': 'Word already exists in this folder'}), 400

    # Update the vocabulary
    vocabulary.word = data['word']
    vocabulary.definition = data['definition']
    
    # Try to get audio URL from our dictionary if not provided
    audio_url = data.get('audio_url', '')
    if not audio_url and not vocabulary.audio_url and dictionary:
        audio_url = dictionary.get_audio_url(data['word'])
    
    vocabulary.audio_url = audio_url or vocabulary.audio_url
    vocabulary.image_url = data.get('image_url', '') or vocabulary.image_url
    vocabulary.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({'vocabulary': vocabulary.to_dict()})

@app.route('/api/folders/<int:folder_id>/check-word', methods=['POST'])
def api_check_word(folder_id):
    """API endpoint to check if a word already exists in a folder"""
    data = request.get_json()

    if not data or 'word' not in data:
        return jsonify({'error': 'Word is required'}), 400

    existing_vocab = Vocabulary.query.filter_by(
        folder_id=folder_id, word=data['word']).first()

    return jsonify({'exists': existing_vocab is not None})

@app.route('/api/folders/<int:folder_id>/generate-quiz', methods=['POST'])
def api_generate_quiz(folder_id):
    """API endpoint to generate a quiz from folder vocabularies"""
    data = request.get_json()

    try:
        question_count = int(data.get('question_count', 5)) if data else 5
    except (ValueError, TypeError):
        return jsonify({'error': 'question_count must be an integer'}), 400

    folder = Folder.query.get_or_404(folder_id)
    vocabularies = folder.vocabularies

    if not vocabularies:
        return jsonify({'error': 'No vocabularies in this folder'}), 400

    # Generate quiz questions
    quiz_questions = []
    available_vocabs = list(vocabularies)

    for _ in range(min(question_count, len(vocabularies))):
        if not available_vocabs:
            break

        correct_vocab = random.choice(available_vocabs)
        available_vocabs.remove(correct_vocab)

        quiz_questions.append({
            'question': f'What is the definition of "{correct_vocab.word}"?',
            'correct_answer': correct_vocab.definition,
            'word': correct_vocab.word,
            'audio_url': correct_vocab.audio_url or ''
        })

    return jsonify({'questions': quiz_questions})



@app.route('/api/folders/<int:folder_id>/generate-multiple-choice',
           methods=['POST'])
def api_generate_multiple_choice(folder_id):
    """API endpoint to generate multiple choice questions from folder vocabularies"""
    data = request.get_json()
    
    try:
        question_count = int(data.get('question_count', 5)) if data else 5
        options_count = min(int(data.get('options_count', 4)) if data else 4, 6)
    except (ValueError, TypeError):
        return jsonify({'error': 'question_count and options_count must be integers'}), 400

    folder = Folder.query.get_or_404(folder_id)
    vocabularies = folder.vocabularies

    # Generate multiple choice questions
    if len(vocabularies) < 4:
        return jsonify({
            'error':
            'Need at least 4 vocabularies for multiple choice questions'
        }), 400

    # Generate multiple choice questions
    mc_questions = []
    available_vocabs = vocabularies.copy()

    for _ in range(min(question_count, len(vocabularies))):
        if not available_vocabs:
            break

        # Select a random vocabulary for the correct answer
        correct_vocab = random.choice(available_vocabs)
        available_vocabs.remove(correct_vocab)

        # Select 3 random wrong answers from remaining vocabularies
        wrong_vocabs = [v for v in vocabularies if v != correct_vocab]
        wrong_answers = random.sample(wrong_vocabs, min(3, len(wrong_vocabs)))

        # Create answer choices
        choices = [correct_vocab.definition]
        choices.extend([vocab.definition for vocab in wrong_answers])
        random.shuffle(choices)

        correct_index = choices.index(correct_vocab.definition)

        mc_questions.append({
            'question': f'What is the definition of "{correct_vocab.word}"?',
            'choices': choices,
            'correct_index': correct_index,
            'word': correct_vocab.word,
            'audio_url': correct_vocab.audio_url or ''
        })

    return jsonify({'questions': mc_questions})





def get_adobe_stock_images(word, limit=3):
    """Retrieve image URLs from Adobe Stock search"""
    url = f"https://stock.adobe.com/search?k={word}"

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find image elements with data-lazy attribute (these are the actual stock images)
        images = soup.find_all('img', {'data-lazy': True})

        # If no lazy-loaded images found, try regular images
        if not images:
            images = soup.find_all(
                'img', {'src': re.compile(r'\.jpg|\.jpeg|\.png|\.webp')})

        image_urls = []
        seen_urls = set()  # To avoid duplicates

        for img in images:
            # Try data-lazy first, then src
            src = img.get('data-lazy') or img.get('src')
            if src and 'ftcdn.net' in src and src not in seen_urls:
                # Convert thumbnail URL to full-size URL
                src = src.replace('/220_F_/', '/500_F_/')
                image_urls.append(src)
                seen_urls.add(src)

                if len(image_urls) >= limit:
                    break

        return image_urls

    except requests.RequestException as e:
        print(f"Error fetching Adobe Stock images: {e}")
        # Return some default placeholder images
        return [
            "https://via.placeholder.com/500x500.jpg?text=No+Image+Available",
            "https://via.placeholder.com/500x500.jpg?text=Try+Again+Later",
            "https://via.placeholder.com/500x500.jpg?text=Image+Not+Found"
        ]

@app.route('/api/search-images/<word>')
def api_search_images(word):
    """API endpoint to search for images"""
    images = get_adobe_stock_images(word)
    return jsonify({'images': images})

# // Pronounciation check 



@app.route('/api/vocabulary/batch-save', methods=['POST'])
def api_batch_save_vocabulary():
    """API endpoint to save multiple vocabularies at once"""
    data = request.get_json()
    new_items = data.get('new_items', [])
    modified_items = data.get('modified_items', [])
    new_ids = []
    duplicate_words = []

    # Get all existing words in the folder (case-insensitive)
    folder_id = None
    if new_items:
        folder_id = new_items[0].get('folder_id')
    elif modified_items:
        folder_id = modified_items[0].get('folder_id')
    existing_words = set()
    if folder_id:
        existing_words = set(
            w.word.lower() for w in Vocabulary.query.filter_by(folder_id=folder_id).all()
        )

    # Save new vocabularies only if not already in folder
    for vocab in new_items:
        word_lower = vocab.get('word', '').strip().lower()
        if word_lower and word_lower not in existing_words:
            new_vocab = Vocabulary(
                word=vocab.get('word'),
                definition=vocab.get('definition'),
                folder_id=vocab.get('folder_id'),
                audio_url=vocab.get('audio_url', ''),
                image_url=vocab.get('image_url', '')
            )
            db.session.add(new_vocab)
            db.session.flush()  # Get the new ID before commit
            new_ids.append(new_vocab.id)
            existing_words.add(word_lower)
        elif word_lower:
            duplicate_words.append(vocab.get('word'))

    # Update modified vocabularies
    for vocab in modified_items:
        vocab_id = vocab.get('id')
        existing = Vocabulary.query.get(vocab_id)
        if existing:
            existing.word = vocab.get('word', existing.word)
            existing.definition = vocab.get('definition', existing.definition)
            existing.audio_url = vocab.get('audio_url', existing.audio_url)
            existing.image_url = vocab.get('image_url', existing.image_url)

    db.session.commit()

    return jsonify({'success': True, 'newItems': new_ids, 'duplicates': duplicate_words}), 200

@app.route('/api/search-audio/<word>')
def api_search_audio(word):
    """API endpoint to search for audio pronunciation of a word"""
    if not dictionary:
        return jsonify({'error': 'Dictionary not available'}), 500
    
    audio_url = dictionary.get_audio_url(word)
    if audio_url:
        return jsonify({'audio_url': audio_url}), 200
    else:
        return jsonify({'error': 'Audio not found'}), 404

@app.route('/api/dictionary/get-word', methods=['POST'])
def api_get_word():
    data = request.get_json() or request.form
    word = data.get("word")
    lang_dest = data.get("lang_dest", "en")
    src_lang = data.get("src_lang", "de")

    vietnamese_pattern = r'[ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂĐÊÔƠƯÁÀẢÃẠẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]'
    if not word or ' ' in word or re.search(vietnamese_pattern, word):
        return jsonify({'error': 'Please enter a single word without Vietnamese special characters.'}), 400

    # Check if the word exists in the database
    existing_word = SearchedWord.query.filter_by(word=word).first()
    if existing_word:
        translation = existing_word.get_translation(lang_dest)
        if translation:
            existing_word.search_count += 1
            db.session.commit()
            return jsonify({
                'word': existing_word.word,
                'word_type': existing_word.word_type,
                'definition': translation,
                'audio_url': existing_word.audio_url,
                'search_count': existing_word.search_count,
                'cached': True
            })
        # If translation for this language doesn't exist, fetch and update
        if not dictionary:
            return jsonify({'error': 'Dictionary not available'}), 500
        result = dictionary.get_word(word, src_lang=src_lang, lang_dest=lang_dest)
        if not result.get('error'):
            existing_word.set_translation(result['definition'], lang_dest)
            existing_word.search_count += 1
            if not existing_word.audio_url:
                audio_url = dictionary.get_audio_url(word)
                existing_word.audio_url = audio_url
                result['audio_url'] = audio_url
            db.session.commit()
            result['search_count'] = existing_word.search_count
            result['cached'] = False
            return jsonify(result)

    # If word not in database, fetch from dictionary API and store
    if not dictionary:
        return jsonify({'error': 'Dictionary not available'}), 500

    result = dictionary.get_word(word, src_lang=src_lang, lang_dest=lang_dest)
    if not result.get('error'):
        audio_url = dictionary.get_audio_url(word)
        result['audio_url'] = audio_url
        SearchedWord.add_or_update(
            word=word,
            word_type=result.get('word_type'),
            translation=result.get('definition'),
            audio_url=audio_url,
            lang=lang_dest
        )
        result['cached'] = False

    return jsonify(result)

# Set secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True)