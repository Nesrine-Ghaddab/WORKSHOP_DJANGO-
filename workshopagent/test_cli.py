import requests
import uuid
URL = "http://127.0.0.1:8000/api/agent/tasks/"
TEXTE = "L'intelligence artificielle générative est une rupture technologique majeure..."
payload = {
 "task_id": str(uuid.uuid4()),
 "sender": "cli-test-agent",
 "payload": {"content": TEXTE}
}
print("⏳ Envoi de la demande...")
resp = requests.post(URL, json=payload)
print(f"✅ Réponse : {resp.json()['result']}")