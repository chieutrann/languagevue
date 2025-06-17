
# Data Management

This directory contains all the learning content for the German language app.

## Files

- `vocabulary.json` - German-English word pairs
- `articles.json` - German news articles with metadata
- `data_loader.py` - Utility functions for loading and saving data

## Adding New Content

### Adding Vocabulary
```python
from data.data_loader import add_vocabulary_word
add_vocabulary_word("das Auto", "the car")
```

### Adding Articles
```python
from data.data_loader import add_article
add_article(
    title="New Article Title",
    content="Article content in German...",
    difficulty="beginner",  # or "intermediate", "advanced"
    category="technology"   # or "weather", "culture", etc.
)
```

## Difficulty Levels
- `beginner` - Simple vocabulary and sentence structure
- `intermediate` - More complex vocabulary and grammar
- `advanced` - Advanced vocabulary and complex sentences

## Categories
- `technology` - Tech news and innovations
- `weather` - Weather reports and forecasts
- `culture` - Cultural events and traditions
- `sports` - Sports news and events
- `politics` - Political news and events
- `economy` - Economic news and business
