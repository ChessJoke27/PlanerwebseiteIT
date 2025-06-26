# PlanerwebseiteIT

Dies ist ein einfaches Grundgerüst für eine persönliche Planer-Webseite. Die Anwendung basiert auf [Flask](https://palletsprojects.com/p/flask/) und verwendet SQLite als lokale Datenbank. Sie bietet Platzhalter für ein Ticketsystem, einen Kalender und ein kleines Inventar.

## Installation

1. Python 3 installieren.
2. Abhängigkeiten mit `pip install -r requirements.txt` installieren.
3. Optional: die Umgebungsvariablen `PLANNER_SECRET_KEY` und `PLANNER_ADMIN_PASSWORD` setzen.

## Starten der Anwendung

```
python app.py
```

Beim ersten Start wird automatisch ein Benutzer `admin` angelegt. Nach dem Login können die vorbereiteten Seiten für Tickets, Kalender und Inventar aufgerufen werden.
