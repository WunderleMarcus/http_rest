import requests  # Wir importieren die Bibliothek, die HTTP-Anfragen ermöglicht

# Diese Funktion sendet eine Anfrage an eine API und gibt das Ergebnis aus
def get_data(url):
    try:
        # Hier senden wir eine GET-Anfrage an die angegebene URL
        response = requests.get(url)

        # Wir prüfen, ob die Anfrage erfolgreich war (Statuscode 200 bedeutet "OK")
        if response.status_code == 200:
            print("Anfrage erfolgreich!\n")

            # Wir versuchen, die Antwort als JSON zu lesen (typisch für APIs)
            try:
                data = response.json()  # JSON in Python-Daten umwandeln (z. B. Dictionary)
                print("JSON Antwort:")
                print(data)  # Ausgabe der Daten im Terminal
            except ValueError:
                # Falls die Antwort kein JSON ist (z. B. HTML oder Text)
                print("Antwort (kein JSON):")
                print(response.text)  # Ausgabe als normaler Text

        else:
            # Falls der Server antwortet, aber mit einem Fehlercode (z. B. 404 oder 500)
            print(f"Fehler bei der Anfrage: Statuscode {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Falls ein Problem bei der Verbindung auftritt (z. B. kein Internet)
        print("Anfrage fehlgeschlagen:")
        print(e)


# Dieser Teil wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == "__main__":
    # Das ist eine öffentliche Test-API (liefert Beispiel-Daten)
    api_url = "https://jsonplaceholder.typicode.com/posts/1"

    # Info-Ausgabe im Terminal
    print(f"Sende GET-Request an: {api_url}\n")

    # Aufruf unserer Funktion mit der URL
    get_data(api_url)