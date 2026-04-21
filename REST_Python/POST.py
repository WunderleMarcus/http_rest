import requests  # Bibliothek für HTTP-Anfragen

# Diese Funktion sendet Daten an eine API (z. B. um etwas zu erstellen)
def post_data(url, payload):
    try:
        # Wir senden eine POST-Anfrage mit Daten (payload)
        # "json=payload" sorgt dafür, dass die Daten als JSON gesendet werden
        response = requests.post(url, json=payload)

        # Erfolgreich, wenn Statuscode 200 (OK) oder 201 (Created)
        if response.status_code in (200, 201):
            print("POST erfolgreich!\n")
            print(response.json())  # Antwort als JSON ausgeben
        else:
            print(f"Fehler: Statuscode {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Fehler z. B. bei Netzwerkproblemen
        print("Anfrage fehlgeschlagen:")
        print(e)


if __name__ == "__main__":
    # API-Endpunkt (hier werden neue Einträge simuliert)
    api_url = "https://jsonplaceholder.typicode.com/posts"

    # Das sind die Daten, die wir senden wollen
    data = {
        "title": "Test",
        "body": "Das ist ein Beispiel",
        "userId": 1
    }

    print(f"Sende POST-Request an: {api_url}\n")

    # Funktion aufrufen und Daten senden
    post_data(api_url, data)