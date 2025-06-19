"""
Simple test script for autocomplete functionality
Run this directly to test the autocomplete logic without going through the web server
"""

import sys
from dictionary import GermanDictionary

def test_autocomplete():
    print("Initializing German Dictionary...")
    dictionary = GermanDictionary()
    
    # Test cases
    test_queries = ["ab", "haus", "fahr", "spiel", "z"]
    
    for query in test_queries:
        print(f"\n\nTesting autocomplete for '{query}':")
        try:
            suggestions = dictionary.get_autocomplete_suggestions(query, 10)
            print(f"Found {len(suggestions)} suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion['word']} - {suggestion['type']}")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_autocomplete()
