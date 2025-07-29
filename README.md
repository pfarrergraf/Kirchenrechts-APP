# 🕊️ Kirchenrechts-App mit OpenAI Assistant und Streamlit GUI

## Überblick

Diese innovative App kombiniert die Leistungsfähigkeit von OpenAI's Assistant API mit einer benutzerfreundlichen Streamlit-Oberfläche, um kirchenrechtliche Fragen der Evangelischen Kirche in Hessen und Nassau (EKHN) präzise und schnell zu beantworten. Die Lösung demonstriert die praktische Anwendung modernster KI-Technologie in einem spezialisierten Fachbereich.

## 🎯 Funktionalitäten

- **Intelligente Fragebeantwortung**: Nutzt einen speziell trainierten OpenAI Assistant für kirchenrechtliche Expertise
- **Benutzerfreundliche Oberfläche**: Moderne Web-GUI mit Streamlit für einfache Bedienung
- **Sichere API-Key-Verwaltung**: Umgebungsvariablen-basierte Konfiguration für maximale Sicherheit
- **Retrieval-gestützte Antworten**: Der Assistant greift auf umfangreiche kirchenrechtliche Dokumente zu
- **Schnelle Antwortzeiten**: Effiziente Verarbeitung durch die Assistants API

## 📋 Voraussetzungen

- **Python 3.10** oder höher
- **OpenAI API-Key** (erhältlich unter [platform.openai.com](https://platform.openai.com))
- **Bestehender OpenAI Assistant** mit Retrieval-Funktion (ID: `asst_er72T8D7D8xth2HaM0mjxi5m`)
- **Internetverbindung** für API-Zugriff

## 🚀 Installation

### 1. Repository klonen oder Dateien herunterladen

```bash
git clone <repository-url>
cd Kirchenrechts-APP
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. OpenAI API-Key konfigurieren

Bearbeiten Sie die `.env`-Datei und ersetzen Sie den Platzhalter mit Ihrem API-Key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ Wichtig**: Geben Sie Ihren API-Key niemals öffentlich weiter!

## 🎮 Nutzung

### App starten

```bash
streamlit run app.py
```

Die App öffnet sich automatisch in Ihrem Standard-Webbrowser unter `http://localhost:8501`.

### Bedienung

1. **Optional**: Wählen Sie ein AI-Modell aus (wenn mehrere verfügbar sind)
2. Geben Sie Ihre kirchenrechtliche Frage in das große Textfeld ein
3. Senden Sie die Frage ab mit:
   - **Ctrl+Enter** (Windows/Linux) bzw. **Cmd+Enter** (Mac)
   - Oder klicken Sie auf den Button "📤 Frage senden"
4. Verfolgen Sie den Fortschritt:
   - 🚀 Konversation wird gestartet
   - 📝 Frage wird übermittelt
   - 🤖 Assistant wird aktiviert
   - 🔍 Frage wird analysiert
   - 📚 Dokumente werden durchsucht
   - ✍️ Antwort wird formuliert
5. Die Antwort erscheint nach 10-30 Sekunden (je nach Modell und Komplexität)

### Beispielfragen

- "Darf eine Pfarrerin das Abendmahl ohne Ordination spenden?"
- "Welche Voraussetzungen gelten für die Wahl zum Kirchenvorstand?"
- "Wie ist das Verfahren bei Amtspflichtverletzungen geregelt?"

## 📁 Projektstruktur

```
Kirchenrechts-APP/
├── .env                              # Umgebungsvariablen (API-Key)
├── app.py                            # Hauptanwendung mit Streamlit-GUI
├── assistant_setup.py                # Einmalige Assistant-Erstellung (optional)
├── create_multi_model_assistants.py  # Script für Multi-Model-Support
├── requirements.txt                  # Python-Abhängigkeiten
└── README.md                        # Diese Dokumentation
```

### Dateibeschreibungen

- **`.env`**: Sichere Speicherung des OpenAI API-Keys
- **`app.py`**: Kernlogik der Anwendung mit GUI und API-Integration
- **`assistant_setup.py`**: Hilfsskript zur Erstellung eines neuen Assistants (nur bei Bedarf)
- **`requirements.txt`**: Liste aller benötigten Python-Pakete

## 🤖 OpenAI Assistant Konfiguration

Die App nutzt einen vordefinierten Assistant mit der ID `asst_er72T8D7D8xth2HaM0mjxi5m`. Dieser Assistant:

- Ist spezialisiert auf EKHN-Kirchenrecht
- Verfügt über Retrieval-Funktionen für umfassende Dokumentensuche
- Antwortet präzise mit Paragraphenangaben

Falls Sie einen eigenen Assistant erstellen möchten, nutzen Sie `assistant_setup.py` und aktualisieren Sie die ID in `app.py`.

### Multi-Model-Support

Um verschiedene AI-Modelle in der App anzubieten:

1. Führen Sie das Script aus:
   ```bash
   python create_multi_model_assistants.py
   ```

2. Das Script erstellt Assistants für:
   - GPT-4o (beste Qualität, längere Antwortzeit)
   - GPT-3.5-Turbo (schnell, gute Qualität)
   - GPT-4-Turbo (ausgewogen)

3. Kopieren Sie die generierte Konfiguration in `app.py`

4. Starten Sie die App neu - die Modellauswahl erscheint automatisch

## 💰 Kostenkontrolle

### OpenAI Dashboard Einstellungen

1. Besuchen Sie [platform.openai.com/usage](https://platform.openai.com/usage)
2. Setzen Sie ein monatliches Ausgabenlimit (z.B. 5€)
3. Überwachen Sie regelmäßig Ihre Nutzung

### Kostenschätzung

- Pro Anfrage: ca. 0,01-0,05€ (abhängig von Fragelänge und Antwortumfang)
- Monatlich bei moderater Nutzung: 5-20€

## 🚀 Deployment-Optionen

| Option | Beschreibung | Zielgruppe |
|--------|--------------|------------|
| **Lokal** | `streamlit run app.py` | Entwicklung & Tests |
| **Executable** | `pyinstaller app.py` | Windows-Nutzer ohne Python |
| **Streamlit Cloud** | [streamlit.io](https://streamlit.io) | Online-Demo für Investoren |
| **VPS/Cloud** | AWS, Azure, Google Cloud | Produktiver Betrieb |

## 🔧 Fehlerbehandlung

### Häufige Probleme und Lösungen

| Problem | Lösung |
|---------|--------|
| "Invalid API Key" | Überprüfen Sie den API-Key in `.env` |
| Keine Antwort | Internetverbindung prüfen, API-Limits checken |
| "Assistant not found" | Assistant-ID in `app.py` verifizieren |
| Lange Wartezeiten | OpenAI-Status prüfen, ggf. später erneut versuchen |

### Debug-Modus

Für detaillierte Fehlerinformationen können Sie Streamlit im Debug-Modus starten:

```bash
streamlit run app.py --logger.level=debug
```

## 🔐 Sicherheitshinweise

1. **API-Key-Schutz**: 
   - Niemals im Code hart kodieren
   - `.env` nicht in Version Control committen
   - Regelmäßig rotieren

2. **Nutzungslimits**:
   - Monatliche Ausgabengrenzen setzen
   - API-Nutzung überwachen

3. **Datenschutz**:
   - Keine sensiblen Daten in Fragen eingeben
   - DSGVO-konforme Nutzung sicherstellen

## 💼 Für Investoren

### Warum diese Lösung?

- **Skalierbar**: Von Einzelnutzung bis Enterprise-Deployment
- **Kosteneffizient**: Pay-per-Use-Modell ohne hohe Initialkosten
- **Zukunftssicher**: Basiert auf modernster OpenAI-Technologie
- **Benutzerfreundlich**: Keine technischen Vorkenntnisse erforderlich
- **Erweiterbar**: Einfache Integration weiterer Rechtsgebiete

### ROI-Potenzial

- **Zeitersparnis**: 90% schnellere Rechtsfindung
- **Kostenreduktion**: Weniger externe Rechtsberatung nötig
- **Qualitätssteigerung**: Konsistente, aktuelle Antworten
- **Skalierungseffekte**: Marginalkosten nahe null bei steigender Nutzung

### Nächste Schritte

1. Live-Demo vereinbaren
2. Pilotprojekt mit ausgewählten Nutzern
3. Feedback sammeln und iterieren
4. Vollständiges Rollout planen

### Neue Features

- **Detaillierte Statusmeldungen**: Transparente Anzeige aller Verarbeitungsschritte
- **Multi-Model-Support**: Vorbereitet für verschiedene AI-Modelle
- **Verbesserte UX**: Größeres Eingabefeld, Ctrl+Enter-Support, besseres visuelles Feedback

## 📞 Support & Kontakt

Bei Fragen oder für eine Demo-Präsentation kontaktieren Sie uns gerne.

---

**Version**: 1.0.0  
**Letzte Aktualisierung**: Januar 2025  
**Lizenz**: Proprietär