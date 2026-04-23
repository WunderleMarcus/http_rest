from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List

app = FastAPI(
    title="Pydantic Lern-API",
    description="Diese API zeigt anschaulich, wie Pydantic Daten validiert, konvertiert und verarbeitet."
)

# ----------------------------------------
# 1. MODELS (Datenstrukturen)
# ----------------------------------------

class User(BaseModel):
    """
    Pydantic Model = Bauplan für Daten

    👉 Was passiert hier?
    - Definiert, wie Daten aussehen müssen
    - Prüft automatisch Datentypen (Validierung)
    - Wandelt Daten ggf. um (z.B. String → int)
    """

    id: int
    name: str = Field(..., min_length=3, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

    @validator("name")
    def name_no_numbers(cls, value):
        """
        Custom Validator = eigene Regel

        👉 Validierung:
        Bedeutet: Daten werden geprüft, bevor sie verwendet werden.
        """
        if any(char.isdigit() for char in value):
            raise ValueError("Name darf keine Zahlen enthalten")
        return value


class UserCreate(BaseModel):
    """
    Input Model (für POST Requests)

    👉 Warum eigenes Model?
    - User erstellt → hat noch keine ID
    - Saubere Trennung von Input & Output
    """
    name: str = Field(..., min_length=3)
    age: Optional[int] = Field(None, ge=0, le=120)


class UserResponse(BaseModel):
    """
    Response Model (Output)

    👉 Serialisierung:
    Bedeutet: Python-Objekt → JSON (API Antwort)

    Pydantic sorgt dafür, dass:
    - nur definierte Felder zurückgegeben werden
    - Daten korrekt formatiert sind
    """
    id: int
    name: str
    age: Optional[int]
    is_active: bool


class UserUpdate(BaseModel):
    """
    Update Model (PATCH)

    👉 Optional Felder:
    Bedeutet: Nur übergebene Werte werden geändert
    """
    name: Optional[str] = Field(None, min_length=3)
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: Optional[bool] = None


# Fake Datenbank
db: List[User] = []


# ----------------------------------------
# 2. POST
# ----------------------------------------

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    POST = Daten erstellen

    👉 Ablauf im Hintergrund:

    1. Client sendet JSON:
       Beispiel:
       {
         "name": "Max",
         "age": "25"
       }

    2. Deserialisierung:
       JSON → Python dict

    3. Pydantic greift ein:
       - Validierung = prüft Daten (z.B. min_length, Zahlenbereich)
       - Typkonvertierung = "25" → 25 (String → int)

    4. Fehler?
       → automatische Fehlermeldung von FastAPI

    5. Erfolgreich:
       → User Objekt wird erstellt

    6. Serialisierung:
       Python Objekt → JSON Response

    👉 Wichtige Begriffe:
    - Validierung = Daten prüfen
    - Deserialisierung = JSON → Python
    - Serialisierung = Python → JSON
    """

    new_user = User(
        id=len(db) + 1,
        name=user.name,
        age=user.age
    )

    db.append(new_user)
    return new_user


@app.post("/users/bulk", response_model=List[UserResponse])
def create_multiple_users(users: List[UserCreate]):
    """
    Mehrere User erstellen

    👉 Wichtig:
    - Jeder Eintrag wird einzeln validiert
    - Fehler in einem Element → ganze Anfrage schlägt fehl

    👉 Beispiel:
    [
      {"name": "Max"},
      {"name": "A"}  ❌ zu kurz
    ]
    """

    created_users = []

    for user in users:
        new_user = User(
            id=len(db) + 1,
            name=user.name,
            age=user.age
        )
        db.append(new_user)
        created_users.append(new_user)

    return created_users


# ----------------------------------------
# 3. GET
# ----------------------------------------

@app.get("/users/", response_model=List[UserResponse])
def get_all_users():
    """
    Alle User abrufen

    👉 Was passiert:
    - Daten aus "DB" werden geladen
    - Pydantic serialisiert sie automatisch

    👉 Serialisierung:
    Python Objekt → JSON
    """

    return db


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Einzelnen User abrufen

    👉 Path Parameter:
    Teil der URL:
    /users/1

    👉 Pydantic Validierung:
    - user_id MUSS int sein
    - falscher Typ → Fehler

    Beispiel:
    /users/abc → ❌ Fehler
    """

    for user in db:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User nicht gefunden")


@app.get("/users/search/", response_model=List[UserResponse])
def search_users(
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None, le=120),
    active: Optional[bool] = None
):
    """
    Suche mit Query Parametern

    👉 Query Parameter:
    Werte in der URL nach ?

    Beispiel:
    /users/search?min_age=18&active=true

    👉 Pydantic prüft:
    - min_age >= 0
    - max_age <= 120

    👉 Vorteil:
    - Fehler werden automatisch erzeugt
    - Keine manuelle Prüfung nötig

    👉 Datenfluss:
    URL → Parameter → validiert → Funktion
    """

    results = db

    if min_age is not None:
        results = [u for u in results if u.age is not None and u.age >= min_age]

    if max_age is not None:
        results = [u for u in results if u.age is not None and u.age <= max_age]

    if active is not None:
        results = [u for u in results if u.is_active == active]

    return results


# ----------------------------------------
# 4. PATCH
# ----------------------------------------

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update: UserUpdate):
    """
    Daten teilweise ändern

    👉 PATCH:
    - nur einzelne Felder werden aktualisiert

    👉 Beispiel:
    {
      "age": 30
    }

    👉 Pydantic:
    - validiert NUR übergebene Felder
    - ignoriert fehlende Felder

    👉 Vorteil:
    - flexible Updates
    """

    for user in db:
        if user.id == user_id:

            if update.name is not None:
                user.name = update.name

            if update.age is not None:
                user.age = update.age

            if update.is_active is not None:
                user.is_active = update.is_active

            return user

    raise HTTPException(status_code=404, detail="User nicht gefunden")


# ----------------------------------------
# 5. DELETE
# ----------------------------------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    User löschen

    👉 Ablauf:
    - Path Parameter validiert
    - User wird entfernt

    👉 Rückgabe:
    einfache JSON Nachricht

    👉 Wichtig:
    Auch hier schützt Pydantic indirekt:
    - user_id ist garantiert int
    """

    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)
            return {"message": "User gelöscht"}

    raise HTTPException(status_code=404, detail="User nicht gefunden")