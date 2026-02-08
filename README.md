Die Readme wird im Laufe der Zeit um weitere auftretende Antworten zu Fragen erweitert 

---
# Arbeiten im Projekt

## Branch Regeln 

Ab der produktiven Arbeit wird nicht auf dem `Main` branch gearbeitet. Stattdessen wird auf dem `DEV` Branch gearbeitet. 

Das heißt für jede eigene Aufgabe, die man bearbeitet erstellt man einen neuen Branch von `DEV`, macht dort die Anpassungen und merged diesen am Ende wieder in `DEV`. Sobald das Projekt am Ende abgeschlossen ist wird der `DEV` Branch in ``Main`` gemerged. 

## Einleitung Datenbank 

Zur gemeinsamen Arbeit wird eine SQLlite Datenbank verwendet, und jeder erstellt sich eigene Migrationen. Hier soll beschrieben werden, wie wir innerhalb des Teams mit Git arbeiten werden und wie wir Migrationen machen. 

### Was verboten ist! 

- Niemals app.db committen. Es soll standardmäßig im .gitignore inbegriffen sein

### Voraussetzungen

- Repository ist geklont
- Migrations/ liegt im Repo
- App.db ist in .gitignore
- Config.py ist lokal vorhanden
- Virtuelles Environment ist aktiv

## Virtuelle Umgebung erstellen und aktivieren

#### Windows 

Starte innerhalb des Projektes die Konsole. Wenn noch keine virtuelle Umgebung exisitert nutzt dort den Befehl 

`python -m venv .venv`

Zum aktivieren nutzt man anschließend 

`..\.venv\Scripts\Activate.ps1`

Nun sollte die virtuelle Umgebung aktiviert sein. Um aus ihr rauszukommen nutzt man 

`deactivate`

#### MAC 

Hier gibt man in der Kommandozeile 

`python3 -m venv .venv`

für das Erstellen und 

`source .venv/bin/activate`

fürs aktivieren ein. Fürs schließen der Umgebung nutzt man auch 

`deactivate`

## Pakete/Abhängigkeiten installieren 

#### Windows

Um alle für das projekt nötigen Abhängigkeiten zu installieren gibt man in der Konsole im geöffneten Projekt 

`pip install -r requirements.txt`

ein. 

#### MAC

Bei Mac nutzt man den selben Befehl wie bei Windows. Falls pip fehlt nutzt man 

`python3 -m pip install -r requirements.txt`

## Migration 

### Die Datenbank aus den Migrationen erstellen 

#### Windows 

In der Konsole gibt man 

`python -m flask --app app db upgrade`

ein. Nun sollte die app.db vollständig ausgefüllt werden. 

#### MAC 

Hier nutzt man 

`python3 -m flask --app app db upgrade`


### Migration erzeugen 

Wenn der Fall auftritt, dass an den Modellen, die die Datenbanktabellen repräsentieren Spalten angepasst werden müssen, muss eine neue Migration erstellt werden, welche dann die app.db updatet. Dazu passt man die Modelle und nutzt anschließend den Befehl 

#### Windows 

`python -m flask --app app db migrate -m "add xyz"`

#### MAC

`python3 -m flask --app app db migrate -m "add xyz"`

Dadurch sollte eine neue Migrationsdatei mit dem im Befehl eingegebenem Namen erstellt worden sein. Diese findet man dann im 

`migrations/versions/xxxxxxxxx_add xyz.py`

Um nun die neue app.db zu erstellen gibt man wieder den db upgrade Befehl von vorher ein 

### Committen

Die neu erstellten Migrationen sollen ins Git Hub committed werden. 

---



