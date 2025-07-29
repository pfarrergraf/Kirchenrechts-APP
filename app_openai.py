# kirchenrecht_debug.py
import os, openai
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ASSISTANT_ID = "asst_er72T8D7D8xth2HaM0mjxi5m"
THREAD_ID    = "thread_..."         # einmalig anlegen & wiederverwenden
VECTOR_ID    = "vs_..."             # dein bestehender Vector Store

# --- einmalig sicherstellen, dass File Search aktiv ist
client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tools=[{"type": "file_search", "vector_store_ids": [VECTOR_ID]}],
    instructions=(
        "Du bist der Kirchenrechts-Experte. "
        "Nutze **ausschließlich** unsere hinterlegte Kirchenrechtsbibliothek, "
        "zitiere Paragraph & Absatz."
    )
)

# --- Prompteingabe
client.beta.threads.messages.create(
    thread_id=THREAD_ID,
    role="user",
    content="Ist die Taufe zwingend Voraussetzung für kirchliche Trauung?"
)

# --- Run starten
run = client.beta.threads.runs.create(
    assistant_id=ASSISTANT_ID,
    thread_id=THREAD_ID,
    file_search={"max_num_results": 8},  # mehr Kontext zulassen
)

# --- Poll bis fertig
while run.status not in {"completed", "failed"}:
    run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=THREAD_ID)

msgs = client.beta.threads.messages.list(thread_id=THREAD_ID)
print(msgs.data[0].content[0].text.value)

# --- Debug: Hat Retrieval stattgefunden?
steps = client.beta.threads.runs.steps.list(
    thread_id=THREAD_ID, run_id=run.id
)
for s in steps.data:
    if s.type == "tool":
        print("TOOL CALL:", s)
