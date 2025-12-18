AGENT_CARD = {
    "agent_id": "agent-resume-01",
    "name": "Super Summarizer",
    "description": "Un agent expert en synthèse de texte.",
    "version": "1.0.0",
    "capabilities": [
    "text-processing",
    "summarization"
    ],
    # On indique aux autres agents où nous contacter
    "endpoints": {
    "tasks": "/api/agent/tasks/",
    "info": "/api/agent/info/"
    },
    "status": "active"
}