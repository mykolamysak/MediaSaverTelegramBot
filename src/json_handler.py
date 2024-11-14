import json
from settings.settings import TRANSLATIONS

class JsonHandler:
    def __init__(self):
        self.file_path = TRANSLATIONS
        self.data = self.load_json()

    def load_json(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
            return {}

    def translate(self, key, lang='EN'):
        return self.data.get(lang, {}).get(key, key)