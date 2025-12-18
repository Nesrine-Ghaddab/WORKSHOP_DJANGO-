import requests
import uuid
import json
# URL de l'agent que nous venons de créer
BASE_URL = "http://127.0.0.1:8000/api/agent"
def test_discovery():
    """Étape 1 : Découvrir qui est l'agent"""
    print("--- 1. TEST DÉCOUVERTE (GET Agent Card) ---")
    try:
        response = requests.get(f"{BASE_URL}/info/")
        if response.status_code == 200:
            print("✅ Succès ! Carte d'identité reçue :")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
             print(f"❌ Erreur : {response.status_code}")
    except Exception as e:
         print(f"❌ Erreur de connexion : {e}")
    print("\n")
def test_task_submission():
    """Étape 2 : Lui envoyer du travail"""
    print("--- 2. TEST ENVOI DE TÂCHE (POST Message) ---")
    
    # Construction du message A2A 
    task_payload = {
    "task_id": str(uuid.uuid4()),
    "sender_agent_id": "agent-client-test",
    "type": "task_request",
    "timestamp": "2024-03-20T10:00:00Z",
    "payload": {
    "action": "summarize",
    "content": "Django est un framework web Python de haut niveau qui encourage un développement rapide et une conception propre et pragmatique. Construit par des développeurs expérimentés, il prend en charge une grande partie des tracas du développement web."
    }
    }
    try:
        response = requests.post(f"{BASE_URL}/tasks/", json=task_payload)
    
        if response.status_code == 200:
            print("✅ Tâche traitée avec succès ! Réponse :")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erreur {response.status_code} : {response.text}")
    except Exception as e:
         print(f"❌ Erreur de connexion : {e}")
if __name__ == "__main__":
    test_discovery()
    test_task_submission()