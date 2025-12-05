from mcp.server.fastmcp import FastMCP
import os
import json

mcp = FastMCP(name="flights_server")

FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

@mcp.resource("flights://today")

def flights_resource():
     with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()

def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""

    flights = _load_flights()

    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return f"""
                Vol {flight["flight_number"]} ({flight["airline"]})
            {flight["departure_city"]} → {flight["arrival_city"]}
            Départ : {flight["departure_time"]} | Arrivée : 
            {flight["arrival_time"]}
            Statut : {flight["status"]}
            """
    return f"Vol {flight_number} non trouvé aujourd'hui."

@mcp.tool()

def flights_to(destination: str) -> str:
    """Liste tous les vols à destination d'une ville aujourd'hui."""
    flights = _load_flights()
    matches = [f for f in flights if destination.lower() in
f["arrival_city"].lower()]
    if not matches:
        return f"Aucun vol trouvé vers {destination.title()} aujourd'hui."
   
    result = f"Vols vers {destination.title()} ({len(matches)}trouvé(s)) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} ({f['airline']}) → {f['arrival_city']} à {f['arrival_time']} – {f['status']}\n"
        return result.strip()

@mcp.tool()
def flights_by_status(status: str) -> str:
    """
    Liste tous les vols ayant un statut particulier aujourd'hui.
    Exemples de statut : "À l'heure", "Retardé", "Annulé", "Embarquement"...
    """
    flights = _load_flights()
    normalized_status = status.strip().lower()
    matches = [
        f for f in flights
        if f.get("status", "").lower() == normalized_status
    ]

    if not matches:
        return f"Aucun vol avec le statut « {status.title()} » aujourd'hui."

    result = f"Vols avec le statut « {status.title()} » ({len(matches)} trouvé(s)) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} {f['airline']} | {f['departure_city']} → {f['arrival_city']} | {f['departure_time']} - {f['arrival_time']}\n"
    return result.strip()

@mcp.tool()
def upcoming_departures_from_paris(hours: int = 2) -> str:
    """
    Liste les vols au départ de Paris dans les prochaines heures (par défaut 2h).
    Utile pour les passagers qui arrivent à l'aéroport et veulent savoir ce qui part bientôt.
    """
    import datetime

    flights = _load_flights()
    now = datetime.datetime.now()
    limit = now + datetime.timedelta(hours=hours)

    upcoming = []
    for f in flights:
        if f["departure_city"] != "Paris":
            continue
        try:
            dep_time = datetime.datetime.strptime(f["departure_time"], "%H:%M")
            dep_time = dep_time.replace(year=now.year, month=now.month, day=now.day)
            if now <= dep_time <= limit:
                upcoming.append(f)
        except ValueError:
            continue  

    if not upcoming:
        return f"Aucun départ de Paris dans les prochaines {hours} heure(s)."

    upcoming.sort(key=lambda x: x["departure_time"])

    result = f"Départs de Paris dans les prochaines {hours}h ({len(upcoming)} vol(s)) :\n\n"
    for f in upcoming:
        result += f"• {f['flight_number']} {f['airline']} → {f['arrival_city']} à {f['departure_time']} – {f['status']}\n"
    return result.strip()

if __name__ == "__main__":
    mcp.run(transport='stdio')