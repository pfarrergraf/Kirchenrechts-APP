"""
app.py - Kirchenrechts-Chat mit OpenAI Assistant

Diese Streamlit-Anwendung ermöglicht es Nutzern, kirchenrechtliche Fragen
an einen spezialisierten OpenAI Assistant zu stellen und präzise Antworten
mit Paragraphenangaben zu erhalten.

Starten mit: streamlit run app.py
"""

import streamlit as st
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import Optional

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Initialisiere den OpenAI-Client
# Der API-Key wird automatisch aus der Umgebungsvariable OPENAI_API_KEY geladen
client = OpenAI()

# Define Assistant ID globally
ASSISTANT_ID = "asst_er72T8D7D8xth2HaM0mjxi5m"  # Hier deine Assistant-ID einfügen

# Konfiguration
# Lade Assistant-Konfigurationen aus JSON-Datei
def load_assistant_config():
    """Lädt die Assistant-Konfiguration aus der JSON-Datei"""
    config_file = "assistant_config.json"
    
    # Fallback-Konfiguration, falls keine JSON-Datei existiert
    fallback_config = {
        "GPT-4o (Standard - Beste Qualität)": {
            "id": "asst_er72T8D7D8xth2HaM0mjxi5m",
            "description": "Höchste Qualität, aber längere Antwortzeiten (10-30 Sekunden)",
            "model": "gpt-4o"
        }
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            st.warning(f"⚠️ Keine {config_file} gefunden. Verwende Standard-Konfiguration.")
            return fallback_config
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Assistant-Konfiguration: {e}")
        return fallback_config

# Lade die Assistants
ASSISTANTS = load_assistant_config()

# Standard-Assistant (erster in der Liste)
DEFAULT_ASSISTANT = list(ASSISTANTS.keys())[0] if ASSISTANTS else "GPT-4o (Standard - Beste Qualität)"

# Modell-Informationen
MODEL_INFO = """
**Verfügbare Modelle:**

Die App unterstützt verschiedene AI-Modelle über separate Assistants:

- **GPT-4o**: Beste Qualität, umfassende Antworten, längere Verarbeitung
- **GPT-3.5-Turbo**: Schnellere Antworten, gute Qualität für die meisten Fragen
- **GPT-4-Turbo**: Balance zwischen Geschwindigkeit und Qualität

**Konfiguration:** Die verfügbaren Modelle werden aus der `assistant_config.json` geladen.
Neue Assistants können über `create_multi_model_assistants.py` hinzugefügt werden.
"""

# Seitenkonfiguration
st.set_page_config(
    page_title="EKHN Kirchenrechts-Chat",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS für besseres Styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .info-box {
        background-color: #f0f2f6;
        color: #333333;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .stTextArea textarea {
        font-size: 16px;
        min-height: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

# Titel der Anwendung
st.title("🕊️ EKHN Kirchenrechts-Chat")
st.markdown("*Ihr digitaler Assistent für kirchenrechtliche Fragen*")

# Informationsbox
st.markdown("""
<div class="info-box">
    <strong>Willkommen!</strong> Stellen Sie Ihre Fragen zum Kirchenrecht der EKHN. 
    Der KI-Assistent antwortet präzise mit relevanten Paragraphenangaben.
</div>
""", unsafe_allow_html=True)

# Session State initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_assistant" not in st.session_state:
    st.session_state.selected_assistant = DEFAULT_ASSISTANT

# Chat-Historie anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Modellauswahl
if len(ASSISTANTS) > 1:
    st.selectbox(
        "🤖 Wählen Sie ein AI-Modell:",
        options=list(ASSISTANTS.keys()),
        key="selected_assistant",
        help="Verschiedene Modelle bieten unterschiedliche Geschwindigkeiten und Qualitäten"
    )
    st.caption(ASSISTANTS[st.session_state.selected_assistant]["description"])
    
    # Zeige Modell-Details in einem Expander
    with st.expander("📊 Modell-Details"):
        selected = ASSISTANTS[st.session_state.selected_assistant]
        st.write(f"**Modell:** {selected['model']}")
        st.write(f"**Assistant ID:** `{selected['id']}`")
        st.write(f"**Beschreibung:** {selected['description']}")
else:
    st.info("ℹ️ Aktuell ist nur ein Modell verfügbar. Weitere Modelle können über `create_multi_model_assistants.py` hinzugefügt werden.")

# Eingabefeld für Fragen mit Form für Enter-Unterstützung
with st.form(key="question_form", clear_on_submit=True):
    question = st.text_area(
        "Stellen Sie Ihre kirchenrechtliche Frage:",
        height=100,
        placeholder="Geben Sie hier Ihre Frage ein...",
        key="question_input"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.form_submit_button(
            "📤 Frage senden",
            use_container_width=True,
            type="primary",
            help="Klicken Sie hier oder drücken Sie Ctrl+Enter zum Senden"
        )

# Verarbeitung der Frage
if submit_button and question:
    # Füge die Benutzerfrage zur Historie hinzu
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Zeige den Assistant-Response Container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        status_container = st.container()

        try:
            # Hole die Assistant-Konfiguration
            assistant_config = ASSISTANTS[st.session_state.selected_assistant]
            assistant_id = assistant_config["id"]

            # Erstelle die vollständige Chat-Historie für den Assistant
            full_history = [
                {"role": message["role"], "content": message["content"]}
                for message in st.session_state.messages
            ]

            # Phase 1: Thread erstellen
            with st.spinner("🚀 Neue Konversation wird gestartet..."):
                thread = client.beta.threads.create()
                st.success("✅ Konversation erfolgreich gestartet")

            # Phase 2: Nachricht senden
            with st.spinner("📝 Ihre Frage wird an den Assistenten übermittelt..."):
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=json.dumps(full_history)  # Sende die gesamte Historie als JSON
                )
                st.success("✅ Frage erfolgreich übermittelt")

            # Phase 3: Assistant-Verarbeitung starten
            with st.spinner(f"🤖 {st.session_state.selected_assistant} wird aktiviert..."):
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=assistant_id
                )
                st.success("✅ Assistent wurde aktiviert")

            # Phase 4: Antwort-Generierung
            status_placeholder = st.empty()
            elapsed_time = 0

            while run.status not in ["completed", "failed", "cancelled", "expired"]:
                elapsed_time += 0.5

                # Dynamische Status-Updates basierend auf der verstrichenen Zeit
                if elapsed_time < 3:
                    status_text = "🔍 Assistent analysiert Ihre Frage..."
                elif elapsed_time < 8:
                    status_text = "📚 Relevante Kirchenrechts-Dokumente werden durchsucht..."
                elif elapsed_time < 15:
                    status_text = "✍️ Assistent formuliert eine präzise Antwort..."
                else:
                    status_text = f"⏳ Verarbeitung läuft... ({int(elapsed_time)}s) - Komplexe Anfragen können bis zu 30s dauern"

                status_placeholder.info(status_text)

                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            # Status-Container leeren
            status_placeholder.empty()

            # Prüfe ob der Run erfolgreich war
            if run.status == "completed":
                # Phase 5: Antwort abrufen
                with st.spinner("💬 Antwort wird abgerufen..."):
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    assistant_message = messages.data[0].content[0].text.value

                # Antwort anzeigen
                message_placeholder.markdown(assistant_message)

                # Füge die Antwort zur Historie hinzu, falls nicht bereits vorhanden
                if not any(msg['content'] == assistant_message for msg in st.session_state.messages):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                # Quellen anzeigen
                if "sources" in messages.data[0].content[0]:
                    sources = messages.data[0].content[0].sources
                    st.markdown("### Quellen")
                    for source in sources:
                        st.markdown(f"- [{source['title']}]({source['url']})")
            else:
                # Fehlerbehandlung für fehlgeschlagene Runs
                status_container.empty()
                error_msg = f"❌ Der Assistent konnte die Anfrage nicht verarbeiten. Status: {run.status}"
                message_placeholder.error(error_msg)

                if run.status == "failed" and run.last_error:
                    st.error(f"Fehlerdetails: {run.last_error.message}")

        except Exception as e:
            # Allgemeine Fehlerbehandlung
            error_message = f"❌ Ein Fehler ist aufgetreten: {str(e)}"
            message_placeholder.error(error_message)

            # Detaillierte Fehlerhinweise
            with st.expander("🔧 Fehlerdiagnose"):
                st.write("**Mögliche Ursachen:**")
                st.write("1. **API-Key fehlt oder ist ungültig**: Überprüfen Sie die `.env`-Datei")
                st.write("2. **Assistant ID ist falsch**: Vergewissern Sie sich, dass die Assistant ID korrekt ist")
                st.write("3. **Keine Internetverbindung**: Prüfen Sie Ihre Netzwerkverbindung")
                st.write("4. **API-Limits erreicht**: Überprüfen Sie Ihr OpenAI-Dashboard")
                st.write("\n**Fehlermeldung:**")
                st.code(str(e))

# Sidebar mit zusätzlichen Informationen
with st.sidebar:
    st.header("ℹ️ Informationen")
    
    # Beispielfragen
    st.subheader("📝 Beispielfragen")
    example_questions = [
        "Darf eine Pfarrerin das Abendmahl ohne Ordination spenden?",
        "Welche Voraussetzungen gelten für die Wahl zum Kirchenvorstand?",
        "Wie ist das Verfahren bei Amtspflichtverletzungen geregelt?",
        "Was sind die Aufgaben des Presbyteriums?",
        "Welche Rechte hat die Gemeindeversammlung?"
    ]
    
    for eq in example_questions:
        if st.button(eq, key=eq):
            st.session_state.messages.append({"role": "user", "content": eq})
            st.rerun()
    
    # Hinweise
    st.subheader("💡 Hinweise")
    st.info(
        "Diese App nutzt KI zur Beantwortung kirchenrechtlicher Fragen. "
        "Die Antworten sollten als Orientierung dienen und ersetzen keine "
        "professionelle Rechtsberatung."
    )
    
    # Modell-Informationen
    with st.expander("🤖 Über das verwendete Modell"):
        st.markdown(MODEL_INFO)
    
    # Kosten-Tracker (optional)
    st.subheader("💰 Nutzung")
    st.write(f"Anzahl Fragen in dieser Sitzung: {len([m for m in st.session_state.messages if m['role'] == 'user'])}")
    
    # Reset-Button
    if st.button("🔄 Neue Unterhaltung"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>
            Powered by OpenAI Assistants API |
            <a href='https://github.com/openai/openai-python' target='_blank'>OpenAI Python SDK</a> |
            <a href='https://platform.openai.com/docs/assistants' target='_blank'>Assistants API Docs</a>
        </small>
    </div>
    """, 
    unsafe_allow_html=True
)

# Live-Datenabruf von kirchenrecht-ekhn.de
if "live_data_fetched" not in st.session_state:
    st.session_state.live_data_fetched = False

# Schlüsselwörter für Live-Datenabruf
LIVE_DATA_KEYWORDS = ["KDO", "KGO", "Besoldung", "Entgelt", "Amtsblätter"]

def should_use_live_data(query):
    """Prüft, ob die Anfrage Live-Daten erfordert."""
    return any(keyword.lower() in query.lower() for keyword in LIVE_DATA_KEYWORDS)

# Dynamische Entscheidung zwischen Vector Store und Live-Datenabruf
if submit_button and question:
    if should_use_live_data(question):
        # Live-Datenabruf
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANTS[st.session_state.selected_assistant]["id"]
        )

        with st.spinner("Live-Daten werden abgerufen..."):
            st.info("Ich durchsuche kirchenrecht-ekhn.de")
            while run.status != "completed":
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status == "completed":
                live_answer = client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value
                st.success(live_answer)
            else:
                st.error("Fehler beim Abrufen der Live-Daten.")
    else:
        # Vector Store verwenden
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANTS[st.session_state.selected_assistant]["id"])

        with st.spinner("Antwort wird generiert..."):
            while run.status != "completed":
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status == "completed":
                answer = client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value
                st.success(answer)
            else:
                st.error("Fehler beim Generieren der Antwort.")