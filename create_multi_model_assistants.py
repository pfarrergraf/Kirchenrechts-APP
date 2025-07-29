"""
create_multi_model_assistants.py - Erstellt mehrere Assistants mit verschiedenen Modellen

Dieses Script hilft beim Erstellen von OpenAI Assistants mit verschiedenen Modellen,
um eine Modellauswahl in der App zu ermöglichen.

Verwendung:
    python create_multi_model_assistants.py
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Lade Umgebungsvariablen
load_dotenv()

# Initialisiere OpenAI Client
client = OpenAI()

# Definiere die zu erstellenden Assistants
ASSISTANT_CONFIGS = [
    {
        "name": "EKHN Kirchenrecht Assistant (GPT-4o)",
        "model": "gpt-4o",
        "description": "Höchste Qualität, umfassende Antworten",
        "key": "GPT-4o (Standard - Beste Qualität)"
    },
    {
        "name": "EKHN Kirchenrecht Assistant (GPT-3.5 Turbo)",
        "model": "gpt-3.5-turbo",
        "description": "Schnellere Antworten, gute Qualität",
        "key": "GPT-3.5-Turbo (Schnell)"
    },
    {
        "name": "EKHN Kirchenrecht Assistant (GPT-4 Turbo)",
        "model": "gpt-4-turbo-preview",
        "description": "Balance zwischen Geschwindigkeit und Qualität",
        "key": "GPT-4-Turbo (Ausgewogen)"
    }
]

# Gemeinsame Instruktionen für alle Assistants
INSTRUCTIONS = """
Du bist ein Experte für das Kirchenrecht der EKHN (Evangelische Kirche in Hessen und Nassau). 
Antworte klar, kurz und mit Paragraphenangabe. 
Beziehe dich auf relevante kirchenrechtliche Dokumente und Bestimmungen. 
Wenn du dir unsicher bist, weise darauf hin und empfehle eine juristische Prüfung.
"""

def create_assistants():
    """Erstellt Assistants für verschiedene Modelle"""
    created_assistants = {}
    
    print("🔧 Erstelle OpenAI Assistants für verschiedene Modelle...\n")
    
    for config in ASSISTANT_CONFIGS:
        try:
            print(f"📋 Erstelle Assistant für {config['model']}...")
            
            # Erstelle den Assistant
            assistant = client.beta.assistants.create(
                name=config["name"],
                model=config["model"],
                instructions=INSTRUCTIONS,
                tools=[{"type": "file_search"}]  # Aktiviere File Search (früher Retrieval)
            )
            
            # Speichere die Assistant-Informationen
            created_assistants[config["key"]] = {
                "id": assistant.id,
                "description": config["description"],
                "model": config["model"]
            }
            
            print(f"✅ Erfolgreich erstellt!")
            print(f"   ID: {assistant.id}")
            print(f"   Name: {assistant.name}")
            print(f"   Model: {assistant.model}\n")
            
        except Exception as e:
            print(f"❌ Fehler beim Erstellen von {config['model']}: {e}\n")
    
    return created_assistants

def save_assistant_config(assistants):
    """Speichert die Assistant-Konfiguration in einer Datei"""
    config_file = "assistant_config.json"
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(assistants, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Konfiguration gespeichert in '{config_file}'")
    
    # Erstelle auch Python-Code zum Kopieren
    print("\n📝 Kopieren Sie folgende Konfiguration in Ihre app.py:\n")
    print("ASSISTANTS = {")
    for key, value in assistants.items():
        print(f'    "{key}": {{')
        print(f'        "id": "{value["id"]}",')
        print(f'        "description": "{value["description"]}",')
        print(f'        "model": "{value["model"]}"')
        print("    },")
    print("}")

def main():
    print("=" * 60)
    print("MULTI-MODEL ASSISTANT CREATOR")
    print("=" * 60)
    print("\nDieses Script erstellt mehrere OpenAI Assistants mit")
    print("verschiedenen Modellen für die Kirchenrechts-App.\n")
    
    # Sicherheitsabfrage
    response = input("⚠️  ACHTUNG: Dies erstellt neue Assistants und kann Kosten verursachen.\n"
                    "Möchten Sie fortfahren? (ja/nein): ")
    
    if response.lower() != "ja":
        print("\n❌ Abgebrochen.")
        return
    
    print("\n")
    
    # Erstelle die Assistants
    created = create_assistants()
    
    if created:
        # Speichere die Konfiguration
        save_assistant_config(created)
        
        print("\n✅ Fertig! Sie können nun die Modellauswahl in der App nutzen.")
        print("\nNächste Schritte:")
        print("1. Kopieren Sie die ASSISTANTS-Konfiguration in app.py")
        print("2. Starten Sie die App neu")
        print("3. Die Modellauswahl sollte nun verfügbar sein")
    else:
        print("\n❌ Es wurden keine Assistants erstellt.")

if __name__ == "__main__":
    main()