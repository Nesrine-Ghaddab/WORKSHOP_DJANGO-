from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .agent_config import AGENT_CARD
from django.views.decorators.csrf import csrf_exempt
import json
import time
import requests
from django.shortcuts import render
import google.generativeai as genai
from dotenv import load_dotenv
import os
    
@require_http_methods(["GET"])
def get_agent_card(request):
 """
 Endpoint de Découverte : Permet aux autres de lire notre Agent Card.
 """
 return JsonResponse(AGENT_CARD)

@csrf_exempt
@require_http_methods(["POST"])
def handle_task(request):
    """
    Endpoint de Tâche : Reçoit le message, appelle Gemini, et renvoie 
    le résumé.
    """
    try:
        # --- A. Lecture et Validation ---
        data = json.loads(request.body)
        
        # On sécurise l'extraction du payload
        payload = data.get('payload', {})
        content_to_process = payload.get('content') # Variable unifiée
        task_id = data.get('task_id')
        sender_id = data.get('sender_agent_id')
        if not content_to_process:
         return JsonResponse({"error": "Le champ 'content' est manquant dans le payload"}, status=400)
        print(f"🤖 Traitement Gemini pour la tâche {task_id} (Reçu de {sender_id})...")
        # --- B. Intelligence (Appel Gemini) ---
        try:
    
            prompt = f"Tu es un expert en synthèse. Résume ce texte en français de manière concise : {content_to_process}"
            
            # Appel à Google Gemini
            response_ai = model.generate_content(prompt)
            summary = response_ai.text
            
        except Exception as e:
            # En cas d'erreur de l'IA (ex: quota, internet), on renvoie une erreur propre
            return JsonResponse({"error" : f"Erreur Gemini: {str(e)}"}, status=500)
        # --- C. Construction de la réponse ---
        response_data = {
        "task_id": task_id,
        "status": "completed",
        "result": summary, # C'est ici qu'on met le texte généré
        "metadata": {
    "processor": "Gemini-1.5-Flash",
    "original_length": len(content_to_process)
    }
    }
        return JsonResponse(response_data)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide"}, status=400)
    except Exception as e :
        return JsonResponse({"error": f"Erreur serveur: {str(e)}"},status=500)

def interface_client(request) :
    summary = None
    original_text = ""
    if request.method == "POST":
            original_text = request.POST.get('text_input')
        
            # Le client Web construit le message A2A
            a2a_message = {
            "task_id": "web-req-001",
            "sender": "web-interface",
            "payload": {"content": original_text}
            }
        # Appel HTTP réel vers l'agent (Simulation d'un appel réseau)
        # Note: En prod, utiliser l'URL absolue du serveur
            api_url = "http://127.0.0.1:8000/api/agent/tasks/"
        
            try:
                response = requests.post(api_url, json=a2a_message)
                if response.status_code == 200:
                    summary = response.json().get('result')
                else:
                    summary = "Erreur de l'agent: " + response.text
            except Exception as e:
                summary = f"Erreur de connexion: {str(e)}"
    return render(request, 'summarizer_agent/interface.html', {
        'summary': summary,
        'original_text': original_text
 })
# 1. Chargement de la configuration
load_dotenv()
# Vérification de la clé API pour éviter les crashs silencieux
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ ATTENTION : La clé GEMINI_API_KEY est manquante dans le fichier .env")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')