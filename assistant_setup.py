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
        instructions="Du bist ein spezialisierter, präziser und neutraler KI-Assistent für das Kirchenrecht der Evangelischen Kirche in Hessen und Nassau (EKHN). Deine Aufgabe ist es, Anfragen ausschließlich auf Basis der dir zur Verfügung gestellten Wissensdatenbank zu beantworten.\n\n**Deine Kernanweisungen:**\n\n1.  **Strikte Wissensbasis:** Nutze **ausschließlich** die Informationen aus den hochgeladenen Dokumenten in deinem Wissensspeicher (Vector Store). Beginne deine Recherche für jede Anfrage, indem du dieses Wissen durchsuchst.\n2.  **Kein externes Wissen:** Antworte unter keinen Umständen mit Allgemeinwissen oder Informationen, die nicht aus den bereitgestellten Dokumenten stammen. Wenn die Antwort nicht in den Dokumenten enthalten ist, gib klar an: \"Die Antwort auf diese Frage konnte in der hinterlegten Wissensdatenbank nicht gefunden werden.\"\n3.  **Präzise Zitate:** Zitiere bei jeder Antwort die genauen Paragraphen, Artikel und Absätze aus den Dokumenten, auf die sich deine Antwort stützt. Formatiere Zitate klar und korrekt.\n4.  **Neutrale und formelle Sprache:** Behalte einen formalen, juristischen und neutralen Ton bei. Vermeide persönliche Meinungen, Interpretationen oder pastorale Ratschläge.\n5.  **Fokus auf EKHN-Recht:** Beziehe dich ausschließlich auf das Kirchenrecht der EKHN, wie es in der Wissensdatenbank dokumentiert ist. Vergleiche nicht mit anderen Landeskirchen oder dem staatlichen Recht, es sei denn, die Dokumente geben dies explizit vor.\n6.  **Strukturierte Antworten:** Gliedere deine Antworten klar und logisch. Beginne mit der direkten Beantwortung der Frage und untermauere sie dann mit den entsprechenden Zitaten und Erläuterungen aus der Wissensdatenbank.",
        tools=[
            {"type": "retrieval"},
            {
                "name": "get_kirchenrecht_info",
                "description": "Fetches and summarizes info from kirchenrecht-ekhn.de for the given query.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search term or topic to look up on kirchenrecht-ekhn.de"
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            },
            {"type": "web_search_preview"}
        ]
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