from main import app, db
from models import SearchedWord
import json

def migrate_database():
    with app.app_context():
        # Get all existing words
        words = SearchedWord.query.all()
        
        # For each word, convert single translation to JSON format
        for word in words:
            if hasattr(word, 'translation') and word.translation:
                # Create new translations JSON
                word.translations = json.dumps({'en': word.translation})
                # Remove old translation column data
                delattr(word, 'translation')
        
        try:
            db.session.commit()
            print("Database migration completed successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_database() 