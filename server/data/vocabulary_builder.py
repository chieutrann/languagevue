
import json
import os
from collections import defaultdict

def clean_word(word):
    """Clean and normalize German words"""
    return word.strip()

def get_english_translation(german_word, word_type, gender=None):
    """Generate English translations for German words"""
    
    # Common translations for nouns with articles
    if word_type == "noun" and gender:
        if gender == "der":
            # Masculine nouns - common patterns
            translations = {
                "Abend": "evening", "Morgen": "morning", "Tag": "day",
                "Mann": "man", "Vater": "father", "Sohn": "son",
                "Hund": "dog", "Kaffee": "coffee", "Wein": "wine",
                "Computer": "computer", "Fernseher": "television",
                "Tisch": "table", "Stuhl": "chair", "Ball": "ball",
                "Apfel": "apple", "Baum": "tree", "Garten": "garden",
                "Aal": "eel", "Aargau": "Aargau (canton)", "Abbau": "demolition",
                "Abbruch": "cancellation", "Abenteuerspielplatz": "adventure playground",
                "Abenteurer": "adventurer", "Abfahrer": "skier", "Abfall": "waste",
                "Abflug": "departure", "Abfluss": "drain", "Abgang": "exit",
                "Abgeordneter": "representative", "Abgesang": "swan song",
                "Abgrund": "abyss", "Abiturient": "high school graduate",
                "Ablauf": "process", "Ableger": "offshoot", "Abnehmer": "customer",
                "Abonnent": "subscriber", "Abruf": "retrieval", "Absatz": "sales",
                "Absatzmarkt": "sales market", "Abscheu": "disgust",
                "Abschiebestopp": "deportation stop", "Abschied": "farewell",
                "Abschiedsbrief": "farewell letter", "Abschlag": "discount"
            }
        elif gender == "die":
            # Feminine nouns - common patterns  
            translations = {
                "Zeit": "time", "Million": "million", "Uhr": "clock",
                "Frau": "woman", "Mutter": "mother", "Tochter": "daughter",
                "Katze": "cat", "Milch": "milk", "Schokolade": "chocolate",
                "Schule": "school", "Universität": "university",
                "Tür": "door", "Wand": "wall", "Blume": "flower",
                "Orange": "orange", "Banane": "banana", "Küche": "kitchen",
                "Abberufung": "recall", "Abbildung": "illustration",
                "Abdeckung": "coverage", "Abendakademie": "evening academy",
                "Abendkasse": "box office", "Abendstunde": "evening hour",
                "Abendzeitung": "evening newspaper", "Abfahrt": "departure",
                "Abfallentsorgung": "waste disposal", "Abfallwirtschaft": "waste management",
                "Abfertigung": "processing", "Abfindung": "severance pay",
                "Abfolge": "sequence", "Abfrage": "query", "Abfuhr": "rejection",
                "Abgabe": "submission", "Abgeltung": "settlement",
                "Abgeordnete": "representative", "Abgeordnetenhauswahl": "parliament election"
            }
        elif gender == "das":
            # Neuter nouns - common patterns
            translations = {
                "Prozent": "percent", "Land": "country", "Ich": "I/ego",
                "Haus": "house", "Auto": "car", "Buch": "book",
                "Kind": "child", "Wasser": "water", "Bier": "beer",
                "Fenster": "window", "Zimmer": "room", "Bett": "bed",
                "Brot": "bread", "Ei": "egg", "Fleisch": "meat",
                "Aachen": "Aachen (city)", "Aarau": "Aarau (city)",
                "Abbild": "image", "Abc": "alphabet", "Abchasien": "Abkhazia",
                "Abendblatt": "evening paper", "Abendessen": "dinner",
                "Abendkleid": "evening dress", "Abendland": "the West",
                "Abendmahl": "Last Supper", "Abendprogramm": "evening program",
                "Abenteuer": "adventure", "Aber": "but", "Abgas": "exhaust gas",
                "Abgeordnetenhaus": "parliament", "Abi": "high school diploma",
                "Abitur": "university entrance qualification"
            }
    
    # Verb translations
    elif word_type == "verb":
        translations = {
            "aalen": "to bask", "aasen": "to waste", "abdunkeln": "to darken",
            "abduzieren": "to abduct", "abfackeln": "to burn off",
            "abflauen": "to subside", "abhausen": "to clear off",
            "abholzen": "to deforest", "abkanzeln": "to rebuke",
            "abkapseln": "to isolate", "abkoppeln": "to uncouple",
            "abkupfern": "to copy", "abmagern": "to lose weight",
            "abmontieren": "to dismantle", "abmurksen": "to kill",
            "abnabeln": "to cut umbilical cord", "abschotten": "to seal off",
            "abseifen": "to soap", "abseilen": "to rappel",
            "absolvieren": "to complete", "absondern": "to secrete",
            "absorbieren": "to absorb", "abstatten": "to pay",
            "abstauben": "to dust", "abstrahieren": "to abstract",
            "abstufen": "to grade", "abstumpfen": "to blunt",
            "abwägen": "to weigh", "abzweigen": "to branch off"
        }
        
        # Irregular verbs
        irregular_translations = {
            "abbacken": "to finish baking", "abbedingen": "to negotiate away",
            "abbehalten": "to keep on", "abbeißen": "to bite off",
            "abbekommen": "to get", "abbiegen": "to turn off",
            "abbinden": "to untie", "abbitten": "to apologize for",
            "abblasen": "to call off", "abbleiben": "to stay away",
            "abbleichen": "to fade", "abbrechen": "to break off",
            "abbrennen": "to burn down", "abbringen": "to dissuade",
            "abdingen": "to negotiate", "abdreschen": "to thresh"
        }
        
        if german_word in irregular_translations:
            return irregular_translations[german_word]
        elif german_word in translations:
            return translations[german_word]
    
    # Adjective translations
    elif word_type == "adjective":
        translations = {
            "aalartig": "eel-like", "aalförmig": "eel-shaped", "aalglatt": "slippery",
            "aasfressend": "carrion-eating", "aasig": "carrion-like",
            "abaissiert": "lowered", "abakteriell": "bacteria-free",
            "abartig": "abnormal", "abatisch": "abatic", "abaxial": "abaxial",
            "abbaubar": "degradable", "abbauwürdig": "worth mining",
            "abbildbar": "representable", "abbruchreif": "ready for demolition",
            "abchasisch": "Abkhazian", "abderitisch": "Abderitic",
            "abdikativ": "abdicative", "abdingbar": "negotiable",
            "abdominal": "abdominal", "abdominell": "abdominal",
            "abendfüllend": "full-length", "abendlich": "evening",
            "abenteuerdurstig": "adventure-thirsty", "abenteuerhungrig": "adventure-hungry",
            "abenteuerlich": "adventurous"
        }
        
        if german_word in translations:
            return translations[german_word]
    
    # Default fallback - try to guess based on word patterns
    if german_word.endswith("ung"):
        return f"{german_word.lower().replace('ung', 'ing')}"
    elif german_word.endswith("keit") or german_word.endswith("heit"):
        return f"{german_word.lower().replace('keit', 'ness').replace('heit', 'ness')}"
    elif german_word.endswith("lich"):
        return f"{german_word.lower().replace('lich', 'ly')}"
    elif german_word.endswith("en") and word_type == "verb":
        return f"to {german_word.lower().replace('en', '')}"
    
    # If no translation found, return a placeholder
    return f"[{german_word}]"

def load_words_from_file(file_path):
    """Load words from a text file"""
    words = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = clean_word(line)
                if word and word not in words:  # Remove duplicates
                    words.append(word)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return words

def build_vocabulary_from_assets():
    """Build comprehensive vocabulary from attached asset files"""
    vocabulary = {}
    
    # Process masculine nouns (der)
    der_words = load_words_from_file('attached_assets/substantiv_singular_der.txt')
    for word in der_words:
        full_word = f"der {word}"
        translation = get_english_translation(word, "noun", "der")
        vocabulary[full_word] = f"the {translation}"
    
    # Process feminine nouns (die)
    die_words = load_words_from_file('attached_assets/substantiv_singular_die.txt')
    for word in die_words:
        full_word = f"die {word}"
        translation = get_english_translation(word, "noun", "die")
        vocabulary[full_word] = f"the {translation}"
    
    # Process neuter nouns (das)
    das_words = load_words_from_file('attached_assets/substantiv_singular_das.txt')
    for word in das_words:
        full_word = f"das {word}"
        translation = get_english_translation(word, "noun", "das")
        vocabulary[full_word] = f"the {translation}"
    
    # Process regular verbs
    regular_verbs = load_words_from_file('attached_assets/Verben_regelmaesig.txt')
    for verb in regular_verbs:
        translation = get_english_translation(verb, "verb")
        vocabulary[verb] = translation
    
    # Process irregular verbs
    irregular_verbs = load_words_from_file('attached_assets/Verben_unregelmaeßig_Infinitiv.txt')
    for verb in irregular_verbs:
        translation = get_english_translation(verb, "verb")
        vocabulary[verb] = translation
    
    # Process adjectives
    adjectives = load_words_from_file('attached_assets/Adjektive.txt')
    for adj in adjectives:
        translation = get_english_translation(adj, "adjective")
        vocabulary[adj] = translation
    
    return vocabulary

def save_vocabulary_json(vocabulary):
    """Save vocabulary to JSON file"""
    try:
        with open('data/vocabulary.json', 'w', encoding='utf-8') as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=4)
        print(f"Vocabulary saved with {len(vocabulary)} entries")
    except Exception as e:
        print(f"Error saving vocabulary: {e}")

def generate_vocabulary():
    """Main function to generate vocabulary from assets"""
    print("Building vocabulary from attached assets...")
    vocabulary = build_vocabulary_from_assets()
    
    print(f"Generated {len(vocabulary)} vocabulary entries")
    
    # Save to JSON file
    save_vocabulary_json(vocabulary)
    
    # Print some statistics
    der_count = len([k for k in vocabulary.keys() if k.startswith('der ')])
    die_count = len([k for k in vocabulary.keys() if k.startswith('die ')])
    das_count = len([k for k in vocabulary.keys() if k.startswith('das ')])
    verb_count = len([k for k in vocabulary.keys() if not k.startswith(('der ', 'die ', 'das ')) and not any(c.isupper() for c in k[1:])])
    adj_count = len(vocabulary) - der_count - die_count - das_count - verb_count
    
    print(f"Statistics:")
    print(f"  - Masculine nouns (der): {der_count}")
    print(f"  - Feminine nouns (die): {die_count}")
    print(f"  - Neuter nouns (das): {das_count}")
    print(f"  - Verbs: {verb_count}")
    print(f"  - Adjectives: {adj_count}")
    
    return vocabulary

if __name__ == "__main__":
    generate_vocabulary()
