"""
assistant_setup.py - Einmalige Erstellung eines OpenAI Assistants

Dieses Skript erstellt einen neuen OpenAI Assistant mit Retrieval-Funktionen
für kirchenrechtliche Fragen der EKHN.

WICHTIG: Dieses Skript sollte nur EINMAL ausgeführt werden!
Die generierte Assistant-ID muss in app.py eingetragen werden.

Verwendung:
    python assistant_setup.py
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Initialisiere den OpenAI-Client
# Der API-Key wird automatisch aus der Umgebungsvariable OPENAI_API_KEY geladen
client = OpenAI()

print("🔧 Erstelle neuen OpenAI Assistant...")

try:
    # Erstelle einen neuen Assistant mit spezifischen Einstellungen
    assistant = client.beta.assistants.create(
        name="EKHN Kirchenrecht Assistant",
        model="gpt-4o",
        instructions="Du bist ein Experte für das Kirchenrecht der EKHN (Evangelische Kirche in Hessen und Nassau). "
                    "Antworte klar, kurz und mit Paragraphenangabe. "
                    "Beziehe dich auf relevante kirchenrechtliche Dokumente und Bestimmungen. "
                    "Wenn du dir unsicher bist, weise darauf hin und empfehle eine juristische Prüfung.",
        tools=[{"type": "file_search"}]  # Aktiviere File Search für Dokumentenzugriff (früher Retrieval)
    )
    
    print("✅ Assistant erfolgreich erstellt!")
    print(f"📋 Assistant ID: {assistant.id}")
    print(f"📌 Name: {assistant.name}")
    print(f"🤖 Model: {assistant.model}")
    print("\n⚠️  WICHTIG: Kopiere die Assistant ID und füge sie in app.py ein!")
    print(f"\nASSISTANT_ID = \"{assistant.id}\"")
    
    # Optional: Speichere die ID in einer Datei
    with open("assistant_id.txt", "w") as f:
        f.write(f"ASSISTANT_ID={assistant.id}\n")
        f.write(f"Name: {assistant.name}\n")
        f.write(f"Model: {assistant.model}\n")
        f.write(f"Created at: {assistant.created_at}\n")
    
    print("\n💾 Assistant ID wurde auch in 'assistant_id.txt' gespeichert.")
    
except Exception as e:
    print(f"❌ Fehler beim Erstellen des Assistants: {e}")
    print("\nMögliche Ursachen:")
    print("1. Ungültiger API-Key in .env")
    print("2. Keine Internetverbindung")
    print("3. OpenAI API-Limits erreicht")
    print("4. Fehlerhafte Model-Bezeichnung")