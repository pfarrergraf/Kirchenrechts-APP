📘 INSTRUCTIONS.md für RooCode (MCP-Server)
🧠 Ziel
Diese Anleitung beschreibt, wie du mit RooCode auf einem MCP-Server eine App erstellst, die:

über die OpenAI Assistants API auf einen Assistant mit Retrieval (Vector Store) zugreift,
eine grafische Benutzeroberfläche (GUI) mit Streamlit bietet,
den API-Key sicher aus einer .env-Datei liest,
Fragen an den Assistant sendet und Antworten anzeigt,
und sich für Investoren oder Nutzer einfach demonstrieren lässt.

📦 Voraussetzungen
Python 3.10 oder höher
OpenAI API-Key (in .env gespeichert)
Assistant mit Retrieval ist bereits bei OpenAI erstellt
RooCode-Umgebung mit Architekt, Coder, Debugger

🗂️ Projektstruktur
kirchenrecht_app/
├── .env
├── app.py
├── assistant_setup.py
├── requirements.txt
└── README.md

🔐 .env – API-Key speicher
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

📦 Requirements.txt - Pakete für die App
openai
streamlit
python-dotenv

🧱 assistant_setup.py – Assistant einmalig erstellen
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

assistant = client.beta.assistants.create(
    name="EKHN Kirchenrecht Assistant",
    model="gpt-4o",
    instructions="Du bist ein Experte für das Kirchenrecht der EKHN. Antworte klar, kurz und mit Paragraphenangabe.",
    tools=[{"type": "retrieval"}]
)

print("Assistant ID:", assistant.id)
💡 Hinweis: Nur einmal ausführen. Die assistant.id notieren und in app.py verwenden.

🖥️ app.py – Streamlit GUI
import streamlit as st
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

st.title("🕊️ EKHN Kirchenrechts-Chat")

ASSISTANT_ID = "ASSISTANT_ID = "asst_er72T8D7D8xth2HaM0mjxi5m"
# Hier deine Assistant-ID einfügen

question = st.text_input("Stelle deine Frage:")

if st.button("Frage stellen") and question:
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=question)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    with st.spinner("Antwort wird generiert..."):
        while run.status != "completed":
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        answer = client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value
        st.success(answer)

🚀 Starten
pip install -r requirements.txt
streamlit run app.py

💰 Kostenkontrolle
OpenAI Dashboard → Usage → „Set usage limit“ → z. B. 5 €
Im Code kannst du run.usage.total_tokens auslesen und eigene Limits setzen
📦 Deployment-Optionen
Option	Beschreibung
streamlit run app.py	Lokale Demo
pyinstaller app.py	.exe für Windows
streamlit.io oder VPS	Online-Zugang für Investoren

🧪 Testen der App


Beispiel-Frage:
> „Darf eine Pfarrerin das Abendmahl ohne Ordination spenden?“

Erwartete Antwort:
> Der Assistant sollte einen relevanten Paragraphen aus dem Kirchenrecht zitieren und eine kurze, klare Begründung liefern.

## 🧰 Fehlerbehandlung

- Wenn keine Antwort erscheint: Stelle sicher, dass dein API-Key korrekt in `.env` gespeichert ist.
- Wenn `run.status` nicht `completed` wird: Überprüfe deine Internetverbindung und API-Limits.
- Bei `InvalidRequestError`: Prüfe, ob der Assistant korrekt erstellt wurde und die ID stimmt.

## 🔐 Sicherheit

- Gib deinen API-Key **niemals öffentlich weiter**.
- Nutze `.env` und `python-dotenv`, um den Key aus dem Code herauszuhalten.
- Setze im OpenAI-Dashboard ein **Usage-Limit**, z. B. 5 € pro Monat.
