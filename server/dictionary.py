import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Optional, Any
import random
import urllib.parse
from data.data_loader import load_vocabulary, save_vocabulary
from deep_translator import GoogleTranslator

class GermanDictionary:

    def __init__(self):
        self.vocabulary = load_vocabulary()
        self._all_words = None  # Cache for autocomplete words
        self.translate_url = "https://translate.argosopentech.com/translate"

        # Core dictionary with detailed information
        self.detailed_dictionary = {
            "die Nachrichten": {
                "translation": "the news",
                "type": "noun",
                "gender": "feminine",
                "plural": "die Nachrichten",
                "example": "Ich schaue jeden Abend die Nachrichten.",
                "example_translation": "I watch the news every evening.",
                "difficulty": "beginner"
            },
            "heute": {
                "translation": "today",
                "type": "adverb",
                "example": "Heute ist ein schöner Tag.",
                "example_translation": "Today is a beautiful day.",
                "difficulty": "beginner"
            },
            "Deutschland": {
                "translation": "Germany",
                "type": "noun",
                "gender": "neuter",
                "example": "Deutschland liegt in Europa.",
                "example_translation": "Germany is located in Europe.",
                "difficulty": "beginner"
            },
            "wichtig": {
                "translation": "important",
                "type": "adjective",
                "example": "Das ist sehr wichtig für mich.",
                "example_translation": "That is very important to me.",
                "difficulty": "beginner"
            },
            "verstehen": {
                "translation": "to understand",
                "type": "verb",
                "conjugation": {
                    "ich": "verstehe",
                    "du": "verstehst",
                    "er/sie/es": "versteht",
                    "wir": "verstehen",
                    "ihr": "versteht",
                    "sie/Sie": "verstehen"
                },
                "example": "Ich verstehe Deutsch ein bisschen.",
                "example_translation": "I understand German a little bit.",
                "difficulty": "beginner"
            },
            "lernen": {
                "translation": "to learn",
                "type": "verb",
                "conjugation": {
                    "ich": "lerne",
                    "du": "lernst",
                    "er/sie/es": "lernt",
                    "wir": "lernen",
                    "ihr": "lernt",
                    "sie/Sie": "lernen"
                },
                "example": "Ich lerne Deutsch.",
                "example_translation": "I am learning German.",
                "difficulty": "beginner"
            },
            "brauchen": {
                "translation": "to need",
                "type": "verb",
                "conjugation": {
                    "ich": "brauche",
                    "du": "brauchst",
                    "er/sie/es": "braucht",
                    "wir": "brauchen",
                    "ihr": "braucht",
                    "sie/Sie": "brauchen"
                },
                "example": "Ich brauche Hilfe.",
                "example_translation": "I need help.",
                "difficulty": "beginner"
            },
            "kaufen": {
                "translation": "to buy",
                "type": "verb",
                "conjugation": {
                    "ich": "kaufe",
                    "du": "kaufst",
                    "er/sie/es": "kauft",
                    "wir": "kaufen",
                    "ihr": "kauft",
                    "sie/Sie": "kaufen"
                },
                "example": "Ich kaufe Brot.",
                "example_translation": "I buy bread.",
                "difficulty": "beginner"
            }
        }

    def _translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Helper method to translate text using MyMemory Translation API"""
        try:
            # MyMemory API endpoint
            url = f"https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"{source_lang}|{target_lang}"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data and "responseData" in data and "translatedText" in data["responseData"]:
                return data["responseData"]["translatedText"]
            return ""
        except Exception as e:
            print(f"Translation error: {e}")
            return ""
        



        # Functio to find audio for a word
    def get_audio_url(self, word):
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

    def get_word(self, word: str, src_lang: str = "de", lang_dest: str = "en") -> Dict[str, Any]:
        """Fetch word data from DWDS API"""
        url = f"https://www.dwds.de/wb/{word}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Check if DWDS reports "keine Wörterbuchartikel vorhanden" (not found)
            if soup.find('p', class_='label label-danger'):
                return {'error': 'Word not found in dictionary.'}
            
            # Extract word type
            word_type_elem = soup.find('span', class_='dwdswb-ft-blocktext')
            word_type = word_type_elem.text.strip().split(" · ")[0] if word_type_elem else ""

            # Get translation            # translation = ts.translate_text(word, from_language=src_lang, to_language=lang_dest)
            try:
                # Log the translation attempt with languages for debugging
                print(f"Attempting translation: '{word}' from {src_lang} to {lang_dest}")
                translation = GoogleTranslator(source=src_lang, target=lang_dest).translate(word)
                print(f"Translation result: '{translation}'")
            except Exception as e:
                print(f"Translation error: {e}")
                # Fallback to direct mapping if translation fails
                if lang_dest == 'vi':
                    translation = self._fallback_translation(word, src_lang, lang_dest)
                else:
                    translation = word

            # Extract article
            lemma_tag = soup.find("h1", class_="dwdswb-ft-lemmaansatz")
            article = " ".join(sibling.string.strip()
                             for sibling in lemma_tag.find("b").next_siblings
                             if sibling.string) if lemma_tag else ""

            audio_url = self.get_audio_url(word)

            return {
                'definition': translation,
                'word_type': word_type,
                'article': article,
                'audio_url': audio_url
            }
        except Exception as e:
            print(f"lookup error for '{word}': {e}")
            return {"error": "Word not found"}
        





    

    def _extract_definition(self, soup: BeautifulSoup) -> str:
        """Extract definition from Glosbe page with fallback selectors"""
        selectors = [
            "h3.align-top.inline.translation__item__pharse.leading-10.text-primary-700.break-words.font-medium.text-base.cursor-pointer",
            "span.text-primary-700.break-words.font-medium.text-base.cursor-pointer",
            ".translation__item__pharse", ".text-primary-700"
        ]

        for selector in selectors:
            elem = soup.select_one(selector)
            if elem and elem.text.strip():
                return elem.text.strip()

        return "No definition found"

    def _extract_article(self, soup: BeautifulSoup) -> str:
        """Extract article for German nouns"""
        try:
            outer_span = soup.find(
                'span', class_='text-xxs text-gray-500 inline-block')
            if outer_span:
                inner_spans = outer_span.find_all(
                    'span', class_='inline-block dir-aware-pr-1')
                if len(inner_spans) > 1:
                    return inner_spans[1].text.strip()
        except Exception:
            pass
        return ""

    def _get_verb_conjugations(self, word: str) -> Dict[str, Any]:
        """Fetch verb conjugations from verbformen.de with improved parsing"""
        try:
            url = f"https://www.verbformen.de/konjugation/?w={word}"
            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            conjugations = {}

            # Process conjugation blocks
            for block in soup.find_all("div", class_="vTbl"):
                tense_tag = block.find("h2", class_="wG")
                if not tense_tag:
                    continue

                tense = tense_tag.text.strip()
                table = block.find("table")
                if not table:
                    continue

                rows = table.find_all("tr")

                if tense == "Partizip":
                    conjugations[tense] = self._parse_partizip(rows)
                else:
                    tense_forms = self._parse_regular_tense(rows)
                    if tense_forms:
                        conjugations[tense] = tense_forms

            # Return present tense for compatibility
            return conjugations.get("Präsens", conjugations.get("Present", {}))

        except requests.RequestException as e:
            print(f"Error fetching conjugations for '{word}': {e}")
            return {}
        except Exception as e:
            print(f"Error parsing conjugations for '{word}': {e}")
            return {}

    def _parse_partizip(self, rows: List) -> Dict[str, str]:
        """Parse Partizip forms"""
        if len(rows) >= 2:
            return {
                "Partizip I": rows[0].get_text(strip=True),
                "Partizip II": rows[1].get_text(strip=True)
            }
        return {}

    def _parse_regular_tense(self, rows: List) -> Dict[str, str]:
        """Parse regular tense conjugations"""
        tense_forms = {}
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 2:
                subject = tds[0].text.strip()
                form = tds[1].get_text(strip=True)
                if subject and form:
                    tense_forms[subject] = form
        return tense_forms

    def fuzzy_search(self, word: str, limit: int = 5) -> List[str]:
        """Find similar words using improved similarity algorithm"""
        word_lower = word.lower()
        suggestions = []

        # Search in all dictionaries
        all_words = list(self.detailed_dictionary.keys()) + list(
            self.vocabulary.keys())

        # Calculate similarity scores
        scored_words = []
        for german_word in set(all_words):
            similarity = self._calculate_similarity(word_lower,
                                                    german_word.lower())
            if similarity > 0.3:  # Threshold for similarity
                scored_words.append((german_word, similarity))

        # Sort by similarity and return top matches
        scored_words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, score in scored_words[:limit]]

    def _calculate_similarity(self, query: str, word: str) -> float:
        """Calculate similarity score between two words"""
        # Exact substring match gets high score
        if query in word or word in query:
            return 0.8

        # Length difference penalty
        len_diff = abs(len(query) - len(word))
        if len_diff > 3:
            return 0.0

        # Character difference counting
        max_len = max(len(query), len(word))
        if max_len == 0:
            return 0.0

        matches = sum(a == b for a, b in zip(query, word))
        return matches / max_len

    def load_words_from_assets(self) -> List[str]:
        """Efficiently load all words from asset files for autocomplete"""
        base_dir = Path("attached_assets")

        def load_words(filename: str) -> List[str]:
            filepath = base_dir / filename
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    words = [line.strip() for line in f if line.strip()]
                    return words
            except FileNotFoundError:
                print(f"Asset file not found: {filepath}")
                return []
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                return []

        # Load words without prefixes
        all_words = []
        all_words.extend(load_words("substantiv_singular_der.txt"))
        all_words.extend(load_words("substantiv_singular_die.txt"))
        all_words.extend(load_words("substantiv_singular_das.txt"))
        all_words.extend(load_words("Adjektive.txt"))
        all_words.extend(load_words("Verben_regelmaesig.txt"))
        all_words.extend(load_words("Verben_unregelmaeßig_Infinitiv.txt"))

        # Add dictionary words
        all_words.extend(self.detailed_dictionary.keys())
        all_words.extend(self.vocabulary.keys())

        return sorted(list(set(filter(None, all_words))))

    def get_autocomplete_suggestions(self,
                                     query: str,
                                     limit: int = 10) -> List[Dict[str, str]]:
        """Get smart autocomplete suggestions with caching"""
        if not self._all_words:
            self._all_words = self.load_words_from_assets()

        query_lower = query.lower()
        suggestions = []

        # Priority 1: Exact prefix matches
        prefix_matches = [
            word for word in self._all_words
            if word.lower().startswith(query_lower)
        ]

        for word in prefix_matches[:limit]:
            suggestions.append({"word": word, "type": "starts_with"})

        # Priority 2: Contains matches (if we need more)
        if len(suggestions) < limit:
            contains_matches = [
                word for word in self._all_words
                if query_lower in word.lower()
                and not word.lower().startswith(query_lower)
            ]

            remaining_slots = limit - len(suggestions)
            for word in contains_matches[:remaining_slots]:
                suggestions.append({"word": word, "type": "contains"})

        return suggestions

    def get_words_by_type(self, word_type: str) -> List[Dict[str, str]]:
        """Get all words of a specific type"""
        return [{
            "word": german_word,
            "translation": details["translation"],
            "example": details.get("example", "")
        } for german_word, details in self.detailed_dictionary.items()
                if details.get("type") == word_type]

    def get_words_by_difficulty(self, difficulty: str) -> List[Dict[str, str]]:
        """Get words by difficulty level"""
        return [{
            "word": german_word,
            "translation": details["translation"],
            "type": details.get("type", "unknown")
        } for german_word, details in self.detailed_dictionary.items()
                if details.get("difficulty") == difficulty]

    def get_random_words(self, count: int = 5) -> List[Dict[str, str]]:
        """Get random words for practice"""
        all_words = list(self.detailed_dictionary.keys())
        count = min(count, len(all_words))

        if count == 0:
            return []

        random_words = random.sample(all_words, count)
        return [{
            "word": word,
            "translation": self.detailed_dictionary[word]["translation"],
            "type": self.detailed_dictionary[word].get("type", "unknown"),
            "example": self.detailed_dictionary[word].get("example", "")
        } for word in random_words]

    def get_word_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the dictionary"""
        total_words = len(self.detailed_dictionary)
        word_types = {}
        difficulty_levels = {}

        for details in self.detailed_dictionary.values():
            word_type = details.get("type", "unknown")
            difficulty = details.get("difficulty", "unknown")

            word_types[word_type] = word_types.get(word_type, 0) + 1
            difficulty_levels[difficulty] = difficulty_levels.get(
                difficulty, 0) + 1

        return {
            "total_words": total_words,
            "word_types": word_types,
            "difficulty_levels": difficulty_levels,
            "vocabulary_size": len(self.vocabulary)
        }

    def add_word_to_dictionary(self,
                               german_word: str,
                               translation: str,
                               word_type: str = "unknown",
                               gender: Optional[str] = None,
                               example: str = "",
                               example_translation: str = "",
                               difficulty: str = "unknown",
                               conjugation: Optional[Dict[str, str]] = None):
        """Add a new word to the dictionary with validation"""
        if not german_word or not translation:
            raise ValueError("German word and translation are required")

        word_data = {
            "translation": translation,
            "type": word_type,
            "example": example,
            "example_translation": example_translation,
            "difficulty": difficulty
        }

        if gender:
            word_data["gender"] = gender
        if conjugation:
            word_data["conjugation"] = conjugation

        self.detailed_dictionary[german_word] = word_data
        self.vocabulary[german_word] = translation
        save_vocabulary(self.vocabulary)

        # Clear cache to refresh autocomplete
        self._all_words = None


    def get_examples(self,word):
        url = f"https://www.verbformen.de/konjugation/beispiele/{word}.htm"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = []
            for h2 in soup.find_all("h2", class_="rNt"):
                heading = h2.get_text(strip=True)
                examples = []
                for ul in soup.find_all("ul", class_="rLst rLstGt"):
                    for li in ul.find_all("li", recursive=False):
                        if not li.get_text(strip=True):
                            continue

                        # Extract sentence from the 'href' query parameter 't'
                        a_tag = li.find("a", class_="rInf")
                        if not a_tag or "href" not in a_tag.attrs:
                            continue
                        href = a_tag["href"]
                        sentence = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("t", [""])[0]

                        # Extract English translation (last <span>)
                        translation_span = li.find_all("span")[-1]
                        translation = translation_span.get_text(strip=True) if translation_span else ""

                        examples.append({
                            "sentence": sentence,
                            "translation": translation
                        })

                if examples:
                    results.append({"heading": heading, "examples": examples})

            return results
        except Exception as e:
            print(f"Examples lookup error for '{word}': {e}")
            return []
        


    # Get example sentences for a word from Glosbe
        
    def get_example_other_language(self,word, src_lang: str = "de", lang_dest: str = "en"):
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

    def get_conjugations_json(self, word):
        """Get conjugations using the format you specified"""
        try:
            r = requests.get(
                f"https://www.verbformen.de/konjugation/?w={word}", timeout=10)
            r.raise_for_status()
        except requests.RequestException:
            return {"error": "word not found"}

        soup = BeautifulSoup(r.text, "html.parser")
        conjugations = {}

        for block in soup.find_all("div", class_="vTbl"):
            tense_tag = block.find("h2", class_="wG")
            if not tense_tag:
                continue
                
            tense = tense_tag.get_text(strip=True)
                   
            if tense == "Infinitiv":
                continue  # Skip Infinitiv

            table = block.find("table")
            if not table:
                continue

            rows = table.find_all("tr")
            if tense == "Partizip":
                if len(rows) >= 2:
                    partizip1 = rows[0].get_text(strip=True)
                    partizip2 = rows[1].get_text(strip=True)
                    conjugations[tense] = {
                        "Partizip I": partizip1,
                        "Partizip II": partizip2
                    }
            else:
                conjugations[tense] = {}
                for row in rows:
                    tds = row.find_all("td")
                    if len(tds) < 2:
                        continue
                    subject = tds[0].get_text(strip=True)
                    form = tds[1].get_text(strip=True)
                    conjugations[tense][subject] = form

        return conjugations

    def clear_cache(self):
        """Clear all cached data"""
        self._all_words = None

    def _fallback_translation(self, word: str, src_lang: str, lang_dest: str) -> str:
        """Fallback method for translations when the main translator fails"""
        # For German -> Vietnamese common words
        de_vi_dict = {
            "heute": "hôm nay",
            "haus": "ngôi nhà",
            "frau": "phụ nữ",
            "mann": "đàn ông",
            "kind": "đứa trẻ",
            "schule": "trường học",
            "arbeit": "công việc",
            "wasser": "nước",
            "brot": "bánh mì",
            "buch": "quyển sách",
            "auto": "xe hơi",
            "Deutschland": "nước Đức",
            "gut": "tốt",
            "schlecht": "tệ"
        }
        
        # For Vietnamese -> German common words
        vi_de_dict = {
            "hôm nay": "heute",
            "ngôi nhà": "das Haus",
            "phụ nữ": "die Frau",
            "đàn ông": "der Mann",
            "đứa trẻ": "das Kind",
            "trường học": "die Schule",
            "công việc": "die Arbeit",
            "nước": "das Wasser",
            "bánh mì": "das Brot",
            "quyển sách": "das Buch",
            "xe hơi": "das Auto",
            "nước Đức": "Deutschland",
            "tốt": "gut",
            "tệ": "schlecht"
        }
        
        word_lower = word.lower()
        
        if src_lang == "de" and lang_dest == "vi":
            return de_vi_dict.get(word_lower, f"[No translation for: {word}]")
        elif src_lang == "vi" and lang_dest == "de":
            return vi_de_dict.get(word_lower, f"[Keine Übersetzung für: {word}]")
        else:
            return f"[Translation from {src_lang} to {lang_dest} not supported in fallback mode]"