from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import UserMixin



db = SQLAlchemy()

class SearchedWord(db.Model):
    __tablename__ = 'searched_words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)
    word_type = db.Column(db.String(50))
    translations = db.Column(db.Text)  # Store translations as JSON string
    audio_url = db.Column(db.String(500))
    search_count = db.Column(db.Integer, default=1)
    first_searched_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_searched_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SearchedWord {self.word}>'

    def get_translation(self, lang='en'):
        """Get translation for specific language"""
        if not self.translations:
            return None
        translations = json.loads(self.translations)
        return translations.get(lang)

    def set_translation(self, translation, lang='en'):
        """Set translation for specific language"""
        translations = {}
        if self.translations:
            translations = json.loads(self.translations)
        translations[lang] = translation
        self.translations = json.dumps(translations)

    @staticmethod
    def add_or_update(word, word_type=None, translation=None, audio_url=None, lang='en'):
        """Add a new word or update existing word's search count and timestamp"""
        existing = SearchedWord.query.filter_by(word=word).first()
        if existing:
            existing.search_count += 1
            existing.last_searched_at = datetime.utcnow()
            if word_type and not existing.word_type:
                existing.word_type = word_type
            if translation:
                existing.set_translation(translation, lang)
            if audio_url and not existing.audio_url:
                existing.audio_url = audio_url
        else:
            new_word = SearchedWord(
                word=word,
                word_type=word_type,
                audio_url=audio_url
            )
            if translation:
                new_word.set_translation(translation, lang)
            db.session.add(new_word)
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving searched word: {e}")
            return False 

# Folder model

class Folder(db.Model):
    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship with vocabularies
    vocabularies = db.relationship('Vocabulary',
                                   backref='folder',
                                   lazy=True,
                                   cascade='all, delete-orphan')
    user = db.relationship('User', backref='folders')

    def __init__(self, name, description='', user_id=None):
        self.name = name
        self.description = description
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'vocabularies': [vocab.to_dict() for vocab in self.vocabularies],
            'user_id': self.user_id
        }

class Vocabulary(db.Model):
    __tablename__ = 'vocabularies'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(500), nullable=True, default='')
    image_url = db.Column(db.String(500), nullable=True, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Foreign key to folder
    folder_id = db.Column(db.Integer,
                          db.ForeignKey('folders.id'),
                          nullable=False)

    def __init__(self,
                 word,
                 definition,
                 audio_url='',
                 image_url='',
                 folder_id=None):
        self.word = word
        self.definition = definition
        self.audio_url = audio_url
        self.image_url = image_url
        self.folder_id = folder_id

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'definition': self.definition,
            'audio_url': self.audio_url or '',
            'image_url': self.image_url or '',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'folder_id': self.folder_id
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'