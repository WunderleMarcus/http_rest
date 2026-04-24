"""
====================================================================
PRAXISAUFGABE: TASK MANAGEMENT API (FASTAPI)
====================================================================

PROJEKTZIEL
Du entwickelst eine vollständige REST-API mit FastAPI zur Verwaltung
von Aufgaben (Tasks). Diese API soll typische Backend-Funktionalitäten
abbilden, wie sie in realen Webanwendungen vorkommen.

Die API wird vollständig über Swagger UI (/docs) getestet und
dokumentiert.

====================================================================
LERNZIELE IM DETAIL
====================================================================

Dieses Projekt vermittelt dir praxisnah:

✔ Aufbau einer REST-API mit FastAPI
✔ Arbeiten mit HTTP-Methoden (GET, POST, PUT, PATCH, DELETE)
✔ Strukturierung von JSON-Daten
✔ Validierung von Eingaben mit Pydantic
✔ Automatische API-Dokumentation mit Swagger / OpenAPI
✔ Nutzung von Query Parametern (Filter, Suche, Pagination)
✔ saubere Fehlerbehandlung (HTTP Exceptions)
✔ Statuscodes korrekt einsetzen
✔ Grundlagen von API-Security (JWT + Bearer Token)

====================================================================
DATENMODELL: TASK
====================================================================

Ein Task repräsentiert eine einzelne Aufgabe im System.

Jeder Task besitzt folgende Struktur:

{
    "id": 1,
    "title": "Einkaufen gehen",
    "description": "Milch, Brot und Eier kaufen",
    "priority": 3,
    "completed": false,
    "created_at": "2026-04-24T12:00:00"
}

FELDBESCHREIBUNG:

- id:
  Eindeutige Identifikation eines Tasks (automatisch vergeben)

- title:
  Kurzer Titel der Aufgabe (Pflichtfeld, mindestens 3 Zeichen)

- description:
  Detaillierte Beschreibung (optional)

- priority:
  Wichtigkeit der Aufgabe (1 = niedrig, 5 = sehr hoch)

- completed:
  Status der Aufgabe (erledigt oder offen)

- created_at:
  Zeitstempel der Erstellung (automatisch gesetzt)

====================================================================
TEIL 1 – GRUNDLEGEND (PFLICHT)
====================================================================

Du sollst eine funktionierende REST-API implementieren.

ERFORDERLICHE ENDPOINTS:

1. GET /tasks
   → Gibt ALLE Tasks zurück
   → JSON-Array

2. GET /tasks/{id}
   → Gibt einen einzelnen Task anhand seiner ID zurück
   → Falls nicht gefunden: 404 Fehler

3. POST /tasks
   → Erstellt einen neuen Task
   → ID wird automatisch vergeben
   → created_at wird automatisch gesetzt

4. PUT /tasks/{id}
   → Aktualisiert einen kompletten Task
   → Alle Felder außer ID und created_at können verändert werden

5. DELETE /tasks/{id}
   → Löscht einen Task anhand der ID

WICHTIG:
- Alle Endpunkte müssen in Swagger sichtbar sein
- Nutze sinnvolle HTTP Status Codes:
  - 200 OK
  - 201 Created
  - 204 No Content
  - 404 Not Found

====================================================================
TEIL 2 – ERWEITERUNG (WEITERFÜHREND)
====================================================================

In diesem Teil machst du die API realistischer und leistungsfähiger.

FILTERUNG

GET /tasks/filter

→ Filtere Tasks nach Kriterien:

Parameter:
- completed (true/false)
- min_priority (1–5)

Beispiel:
/ tasks/filter?completed=false&min_priority=3

👉 Ziel:
Nur passende Tasks zurückgeben

------------------------------------------------------------

TEIL-UPDATE (PATCH)

PATCH /tasks/{id}/complete

→ Markiert einen Task als erledigt (completed = true)

👉 Ziel:
Teilweise Aktualisierung eines Objekts

------------------------------------------------------------

VALIDIERUNG

Implementiere strenge Regeln:

- title darf nicht leer sein
- title muss mindestens 3 Zeichen haben
- priority muss zwischen 1 und 5 liegen

Ziel:
Fehlerhafte Eingaben verhindern

------------------------------------------------------------

QUERY PARAMETER LOGIK

Nutze Query Parameter sinnvoll zur Datenfilterung:

- Status Filter
- Prioritätsfilter
- Kombinationen möglich

👉 Ziel:
Flexibler API-Zugriff

------------------------------------------------------------

FEHLERBEHANDLUNG

Falls etwas schiefgeht:

- Task nicht gefunden → 404
- Ungültige Eingabe → 422
- Leere Liste → trotzdem 200 OK mit []

👉 Ziel:
Saubere API-Responses

====================================================================
TEIL 3 – BONUS (FREIWILLIG)
====================================================================

Hier baust du echte Backend-Features ein.

------------------------------------------------------------

PAGINATION

GET /tasks/paginated

Parameter:
- limit (Standard: 10)
- offset (Standard: 0)

👉 Ziel:
Große Datenmengen kontrolliert zurückgeben

------------------------------------------------------------

STATISTIK-ENDPOINT

GET /stats

Gibt zurück:

- Anzahl aller Tasks
- Anzahl erledigter Tasks
- Anzahl offener Tasks
- Prozentuale Fertigstellung

👉 Ziel:
Einfache Analyse-API

------------------------------------------------------------

ERWEITERTE DATENMODELLE

Ergänze optional:

- status:
  "open", "in_progress", "done"

👉 Ziel:
Realistischere Workflow-Logik

------------------------------------------------------------

ZEITSTEMPEL ERWEITERUNG

- created_at automatisch setzen
- optional: updated_at bei Änderungen

====================================================================
TEIL 4 – CHALLENGE: JWT AUTHENTIFIZIERUNG
====================================================================

Jetzt wird es realistisch wie in echten APIs.

------------------------------------------------------------

LOGIN-ENDPOINT

POST /login

→ Benutzer meldet sich mit:
{
    "username": "admin",
    "password": "secret"
}

→ Rückgabe:
JWT Token

------------------------------------------------------------

BEARER AUTHENTIFIZIERUNG

Geschützte Endpunkte:

- POST /tasks
- PUT /tasks/{id}
- DELETE /tasks/{id}
- PATCH /tasks/{id}/complete

👉 Zugriff nur mit gültigem Token

------------------------------------------------------------

SWAGGER INTEGRATION

- Nutze "Authorize" Button in Swagger UI
- Token wird automatisch bei Requests gesendet

------------------------------------------------------------

TECHNISCHE UMSETZUNG

Verwende:

- OAuth2PasswordBearer
- python-jose (JWT Handling)
- Token mit Ablaufzeit (z. B. 30 Minuten)

👉 Ziel:
Verständnis von API-Sicherheit

====================================================================
ALLGEMEINE HINWEISE
====================================================================

✔ Arbeite Schritt für Schritt
✔ Teste jeden Endpoint über /docs
✔ Achte auf sauberen Code
✔ Nutze sinnvolle Variablennamen
✔ Halte JSON konsistent

====================================================================
"""

from fastapi import FastAPI

app = FastAPI(
    title="Task Management API – Praxisprojekt",
    description="REST API Übung mit FastAPI, Swagger und JWT Auth",
    version="1.0.0"
)

# =========================================================
# IMPLEMENTIERUNG BEGINNT HIER
# =========================================================

tasks = []
task_id_counter = 1


@app.get("/")
def root():
    return {
        "message": "Task API aktiv – nutze /docs für Swagger UI"
    }

# TODO:
# - Pydantic Models
# - CRUD Endpoints
# - Filter
# - Pagination
# - JWT Auth