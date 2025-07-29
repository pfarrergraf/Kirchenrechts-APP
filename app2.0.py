"""
app2.0.py - Erweiterte Version des Kirchenrechts-Chats mit OpenAI Assistant

Diese Streamlit-Anwendung bietet zusätzliche Funktionen und Verbesserungen
für eine optimierte Benutzererfahrung und erweiterte Funktionalität.

Starten mit: streamlit run app2.0.py
"""

import streamlit as st
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import Optional

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Schlüsselwörter für Live-Datenabruf
LIVE_DATA_KEYWORDS = ["KDO", "KGO", "Besoldung", "Entgelt", "Amtsblätter"]

def should_use_live_data(query):
    """Forciert die Nutzung von Live-Daten."""
    return True

# Initialisiere den OpenAI-Client
client = OpenAI()

# Konfiguriere das Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Seitenkonfiguration
st.set_page_config(
    page_title="EKHN Kirchenrechts-Chat 2.0",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
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
st.title("🕊️ EKHN Kirchenrechts-Chat 2.0")
st.markdown("*Ihr digitaler Assistent für kirchenrechtliche Fragen - jetzt mit erweiterten Funktionen*")

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
            logging.info("Starte neue Konversation...")
            with st.spinner("🚀 Neue Konversation wird gestartet..."):
                thread = client.beta.threads.create()
                logging.info(f"✅ Konversation erfolgreich gestartet: Thread ID {thread.id}")

            # Phase 2: Nachricht senden
            logging.info("Übermittle Frage an Assistenten...")
            with st.spinner("📝 Ihre Frage wird an den Assistenten übermittelt..."):
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=json.dumps(full_history)  # Sende die gesamte Historie als JSON
                )
                logging.info("✅ Frage erfolgreich übermittelt.")

            # Phase 3: Assistant-Verarbeitung starten
            logging.info(f"Aktiviere {st.session_state.selected_assistant} Assistenten...")
            with st.spinner(f"🤖 {st.session_state.selected_assistant} wird aktiviert..."):
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=assistant_id
                )
                logging.info(f"✅ Assistent wurde aktiviert: Run ID {run.id}")

            # Phase 4: Antwort-Generierung
            status_placeholder = st.empty()
            elapsed_time = 0

            while run.status not in ["completed", "failed", "cancelled", "expired"]:
                elapsed_time += 0.5

                # Dynamische Status-Updates basierend auf der verstrichenen Zeit
                if should_use_live_data(question):
                    if elapsed_time < 3:
                        status_text = "🔍 Durchsuche kirchenrecht-ekhn.de..."
                    elif elapsed_time < 8:
                        status_text = "📚 Analysiere Live-Daten..."
                    else:
                        status_text = f"⏳ Live-Datenabruf läuft... ({int(elapsed_time)}s)"
                else:
                    if elapsed_time < 3:
                        status_text = "🔍 Assistent analysiert Ihre Frage..."
                    elif elapsed_time < 8:
                        status_text = "📚 Relevante Kirchenrechts-Dokumente werden durchsucht..."
                    elif elapsed_time < 15:
                        status_text = "✍️ Assistent formuliert eine präzise Antwort..."
                    else:
                        status_text = f"⏳ Verarbeitung läuft... ({int(elapsed_time)}s) - Komplexe Anfragen können bis zu 30s dauern"

                status_placeholder.info(status_text)
                logging.debug(f"Run-Status-Update: {status_text} | Current Run ID: {run.id}, Status: {run.status}")
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            logging.info(f"Run beendet mit Status: {run.status}")

            # Status-Container leeren
            status_placeholder.empty()

            # Prüfe ob der Run erfolgreich war
            if run.status == "completed":
                # Phase 5: Antwort abrufen
                with st.spinner("💬 Antwort wird abgerufen..."):
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    assistant_message = messages.data[0].content[0].text.value
                    logging.info("Antwort erfolgreich abgerufen.")

                # Antwort anzeigen
                message_placeholder.markdown(assistant_message)
                logging.debug(f"Angezeigte Assistenten-Nachricht: {assistant_message[:50]}...")

                # Füge die Antwort zur Historie hinzu, falls nicht bereits vorhanden
                if not any(msg['content'] == assistant_message for msg in st.session_state.messages):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    logging.info("Assistenten-Nachricht zur Session State Historie hinzugefügt.")
                else:
                    logging.info("Assistenten-Nachricht ist bereits in der Historie, füge sie nicht erneut hinzu.")

                # Quellen anzeigen
                if "sources" in messages.data[0].content[0]:
                    sources = messages.data[0].content[0].sources
                    st.markdown("### Quellen")
                    for source in sources:
                        st.markdown(f"- [{source['title']}]({source['url']})")
                    logging.info("Quellen angezeigt.")

                # Live-Data Status aktualisieren
                if should_use_live_data(question):
                    st.session_state.live_data_fetched = True
                    logging.info("Live-Datenabruf Status aktualisiert.")
            else:
                # Fehlerbehandlung für fehlgeschlagene Runs
                logging.error(f"Assistent konnte Anfrage nicht verarbeiten. Status: {run.status}")
                status_container.empty()
                error_msg = f"❌ Der Assistent konnte die Anfrage nicht verarbeiten. Status: {run.status}"
                message_placeholder.error(error_msg)

                if run.status == "failed" and run.last_error:
                    logging.error(f"Fehlerdetails des Runs: {run.last_error.message}")
                    st.error(f"Fehlerdetails: {run.last_error.message}")

        except Exception as e:
            # Allgemeine Fehlerbehandlung
            logging.critical(f"Kritischer Fehler aufgetreten: {str(e)}", exc_info=True)
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
        st.markdown("""
        **Verfügbare Modelle:**

        - **GPT-4o**: Beste Qualität, umfassende Antworten, längere Verarbeitung
        - **GPT-3.5-Turbo**: Schnellere Antworten, gute Qualität für die meisten Fragen
        - **GPT-4-Turbo**: Balance zwischen Geschwindigkeit und Qualität

        **Konfiguration:** Die verfügbaren Modelle werden aus der `assistant_config.json` geladen.
        Neue Assistants können über `create_multi_model_assistants.py` hinzugefügt werden.
        """)
    
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
