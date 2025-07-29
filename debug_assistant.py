# kirchenrecht_debug.py
import os
import openai
import time
from dotenv import load_dotenv

# Lade Umgebungsvariablen (stelle sicher, dass OPENAI_API_KEY in .env oder der Umgebung gesetzt ist)
load_dotenv()

# --- KONFIGURATION ---
# Trage hier die ID des Assistants ein, den du überprüfen möchtest.
# Du findest sie in der assistant_config.json oder im OpenAI Playground.
ASSISTANT_ID = "asst_er72T8D7D8xth2HaM0mjxi5m"  # WICHTIG: Ersetze dies mit einer deiner echten IDs

# Deine Testfrage
TEST_FRAGE = "Welche Voraussetzungen gelten für die Wahl zum Kirchenvorstand?"

# --- INITIALISIERUNG ---
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("✅ OpenAI Client erfolgreich initialisiert.")
except Exception as e:
    print(f"❌ Fehler bei der Initialisierung des OpenAI Clients: {e}")
    exit()

# --- SCHRITT 1: ASSISTANT-KONFIGURATION PRÜFEN ---
print(f"\n--- 🔍 Überprüfe Assistant {ASSISTANT_ID} ---")
try:
    assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
    print(f"Name: {assistant.name}")
    print(f"Modell: {assistant.model}")
    
    # Überprüfen, ob das File Search Tool aktiviert ist
    if any(tool.type == 'file_search' for tool in assistant.tools):
        print("✅ 'File Search' Tool ist aktiviert.")
    else:
        print("⚠️ WARNUNG: 'File Search' Tool ist NICHT aktiviert. Das ist wahrscheinlich der Hauptfehler!")

    # Überprüfen, ob ein Vektor-Store angebunden ist
    if assistant.tool_resources and assistant.tool_resources.file_search and assistant.tool_resources.file_search.vector_store_ids:
        vector_store_id = assistant.tool_resources.file_search.vector_store_ids[0]
        print(f"✅ Angebundener Vector Store: {vector_store_id}")
    else:
        print("⚠️ WARNUNG: Kein Vector Store an den Assistant angebunden!")

except Exception as e:
    print(f"❌ Fehler beim Abrufen des Assistants: {e}")
    print("   Stelle sicher, dass die ASSISTANT_ID korrekt ist und du die nötigen Berechtigungen hast.")
    exit()

# --- SCHRITT 2: EINEN TEST-RUN DURCHFÜHREN ---
print("\n--- 🚀 Starte einen Test-Run ---")
try:
    # Neuen Thread für den Test erstellen
    thread = client.beta.threads.create()
    print(f"Thread erstellt: {thread.id}")

    # Nachricht zum Thread hinzufügen
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=TEST_FRAGE
    )
    print(f"Frage an Thread gesendet: '{TEST_FRAGE}'")

    # Run starten und mehr Kontext für die Suche erlauben
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        # Dieser Parameter ist sehr nützlich, um die Suche zu verbessern!
        tool_resources={"file_search": {"max_num_results": 10}}
    )
    print(f"Run gestartet: {run.id}")

    # Warten, bis der Run abgeschlossen ist
    print("⏳ Warte auf Abschluss des Runs...", end="", flush=True)
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
        print(".", end="", flush=True)
    
    print(f"\n✅ Run abgeschlossen mit Status: {run.status}")

    if run.status == "failed":
        print(f"❌ Run fehlgeschlagen. Grund: {run.last_error.message}")

except Exception as e:
    print(f"❌ Fehler während des Test-Runs: {e}")
    exit()

# --- SCHRITT 3: ERGEBNISSE UND DEBUG-LOGS ANALYSIEREN ---
if run.status == "completed":
    print("\n--- 💬 Antwort des Assistants ---")
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # Die Antwort ist normalerweise die erste Nachricht in der Liste
    response_text = messages.data[0].content[0].text.value
    print(response_text)

    print("\n--- 🕵️‍♂️ DEBUG: Analyse der Run Steps ---")
    try:
        steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
        
        file_search_found = False
        for step in steps.data:
            if step.type == "tool_calls":
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == 'file_search':
                        file_search_found = True
                        print("✅ Ein 'file_search' Tool Call wurde gefunden!")
                        print("   - Suchanfragen:", tool_call.file_search)
        
        if not file_search_found:
            print("❌ KRITISCH: Es wurde KEIN 'file_search' Tool Call in den Run Steps gefunden.")
            print("   Der Assistant hat die Wissensdatenbank NICHT für die Antwort genutzt.")
            print("   Überprüfe dringend die Instruktionen des Assistants!")

    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Run Steps: {e}")

print("\n--- Test abgeschlossen ---")
