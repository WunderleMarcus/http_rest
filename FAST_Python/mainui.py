from fastapi import FastAPI

# ------------------------------------------------------------
# GRUNDIDEE EINER API
# ------------------------------------------------------------
# Eine API (Application Programming Interface) ist eine Schnittstelle,
# über die Programme miteinander kommunizieren können.
#
# Beispiel:
# Browser → Anfrage (Request) → Server (unsere API)
# Server → Antwort (Response) → Browser
#
# FastAPI hilft uns dabei, solche APIs einfach zu erstellen.
# ------------------------------------------------------------


# ------------------------------------------------------------
# APP INITIALISIEREN
# ------------------------------------------------------------
# Hier erstellen wir unsere API-Anwendung.
# Diese Instanz ("app") wird später vom Server gestartet.
# ------------------------------------------------------------

app = FastAPI(
    title="Test API",
    description="Einfache lokale API für den heutigen Mittwoch",
    version="1.0.0"
)


# ============================================================
# ROOT ENDPOINT
# ============================================================
# Ein "Endpoint" ist eine URL, über die man mit der API spricht.
#
# @app.get("/") bedeutet:
# - Diese Funktion wird ausgeführt, wenn jemand die URL "/" aufruft
# - GET ist eine HTTP-Methode zum Abrufen von Daten
# ------------------------------------------------------------

@app.get("/")
def read_root():
    """
    Diese Funktion wird aufgerufen, wenn die Startseite der API
    geöffnet wird.
    """

    # Rückgabe erfolgt als Dictionary (ähnlich wie JSON)
    # FastAPI wandelt dieses automatisch in JSON um
    return {
        "message": "Willkommen zur lokalen Test API von Marcus in 25-11 "
    }


# Beispiel:
# GET http://localhost:8000/
#
# Antwort:
# {
#   "message": "Willkommen zur lokalen Test API von Marcus in 25-11 "
# }


# ============================================================
# GET MIT PATH PARAMETER
# ============================================================
# Path Parameter sind Werte, die direkt in der URL stehen.
#
# Beispiel:
# /items/5
#
# Hier ist "5" der Wert für item_id
# ------------------------------------------------------------

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
    Diese Funktion verarbeitet Anfragen an /items/{item_id}

    Parameter:
    - item_id: kommt aus der URL (z. B. /items/10)
    - q: optionaler Query-Parameter (z. B. ?q=schule)
    """

    # item_id wird automatisch als int interpretiert
    # q ist optional (Standardwert = None)

    return {
        "item_id": item_id,
        "query": q
    }


# Beispiel:
# GET /items/10?q=schule
#
# Erklärung:
# - item_id = 10
# - q = "schule"
#
# Antwort:
# {
#   "item_id": 10,
#   "query": "schule"
# }


# ============================================================
# GET MIT QUERY PARAMETERN (SIMULATION VON "ERSTELLEN")
# ============================================================
# Normalerweise würde man für das Erstellen von Daten POST verwenden.
# Hier simulieren wir das mit GET, um es einfacher zu halten.
#
# Query Parameter stehen nach einem "?" in der URL:
# ?name=Stift&price=2.5
# ------------------------------------------------------------

@app.get("/create-item/")
def create_item(name: str, price: float, description: str = None):
    """
    Diese Funktion simuliert das Erstellen eines Items.

    Parameter:
    - name: Name des Produkts (Pflichtfeld)
    - price: Preis (Pflichtfeld)
    - description: optionale Beschreibung
    """

    # Wir bauen manuell ein Dictionary zusammen
    # (da wir kein Pydantic verwenden)
    item = {
        "name": name,
        "price": price,
        "description": description
    }

    # Rückgabe des "erstellten" Objekts
    return {
        "message": "Item erstellt (Simulation)",
        "item": item
    }


# Beispiel:
# GET /create-item/?name=Stift&price=2.5&description=Blau
#
# Erklärung:
# - name = "Stift"
# - price = 2.5
# - description = "Blau"
#
# Antwort:
# {
#   "message": "Item erstellt (Simulation)",
#   "item": {
#     "name": "Stift",
#     "price": 2.5,
#     "description": "Blau"
#   }
# }


# ============================================================
# HEALTH CHECK
# ============================================================
# Dieser Endpoint wird oft verwendet, um zu prüfen,
# ob der Server noch läuft.
#
# Wird häufig von Monitoring-Tools genutzt.
# ------------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Gibt den Status der API zurück
    """
    return {
        "status": "ok"
    }


# Beispiel:
# GET /health
#
# Antwort:
# {
#   "status": "ok"
# }


# ============================================================
# ZUSAMMENFASSUNG FÜR TEILNEHMER
# ============================================================

"""
Wichtige Konzepte:

1. HTTP-Methoden:
   - GET: Daten abrufen

2. Parameter-Arten:
   - Path Parameter:
     Bestandteil der URL
     Beispiel: /items/5

   - Query Parameter:
     Nach einem "?" in der URL
     Beispiel: ?name=Max&age=20

3. Rückgabewerte:
   - Python-Dictionaries werden automatisch zu JSON

4. Ohne Pydantic:
   - Keine automatische Validierung
   - Wir müssen selbst darauf achten, welche Daten kommen

Merksatz:
Die URL bestimmt, welche Funktion ausgeführt wird.
"""