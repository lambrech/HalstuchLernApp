# HalstuchLernApp

Eine einfache Progressive Web App (PWA) für die **Halstuchprüfung / Aufnahmeprüfung** im **CVJM Stetten**. Sie soll Kindern und Jugendlichen helfen, die wichtigsten Inhalte für die Prüfung spielerisch zu lernen und jederzeit griffbereit zu haben.

> **Status:** 0.1.0-alpha.1 – erste Inhalte sind vorhanden, ein Quiz folgt in einem späteren Schritt.

## Inhalte der App

Die App gliedert sich in zwei Lernbereiche:

### Aufnahmeprüfung
- Unsere Zielsätze
- Gottes gute Gebote an sein Volk (10 Gebote)
- Das Vater Unser
- Losungsworte (Jungscharlosung, Weltbundlosung, Jahreslosung)
- Abzeichen und ihre Bedeutung (Ankerkreuz, Eichenkreuz)
- Lieder
- Ich kenne meine Bibel / Berichte

### Mädchenschaft / Jungenschaft
- Pariser Basis
- Ziele der Mädchenschaft / Jungenschaft
- Das Glaubensbekenntnis
- Die Einsetzungsworte zum Abendmahl
- Bibelstellen
- Lieder

## Technologien

- [Blazor WebAssembly](https://dotnet.microsoft.com/apps/aspnet/web-apps/blazor) (.NET 8)
- [MudBlazor](https://mudblazor.com/) für Material-Design-Komponenten
- Progressive Web App (PWA) mit Service Worker
- [GitHub Pages](https://pages.github.com/) für das Hosting
- [Playwright](https://playwright.dev/python/) für UI-Exploration und Screenshots

## Projektstruktur

```
.
├── .github/workflows/deploy.yml     # GitHub Actions Deployment
├── raw/                             # Ausgangsmaterialien (PDFs, Bilder, extrahierte Texte)
├── src/HalstuchLernApp/             # Blazor WASM App
│   ├── wwwroot/data/content.json    # Zentrale Lerninhalte
│   ├── wwwroot/images/              # Logos und Bilder
│   ├── wwwroot/icons/               # PWA Icons
│   ├── Pages/                       # Razor-Seiten
│   ├── Services/                    # ContentService, UpdateService
│   └── Layout/                      # MainLayout, NavMenu
├── tests/
│   ├── explore_app.py               # Playwright-Skript zur UI-Dokumentation
│   └── screenshots/                 # Automatisch erzeugte Screenshots
└── README.md
```

## Lokale Entwicklung

Voraussetzung: [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) ist installiert.

```bash
cd src/HalstuchLernApp
dotnet run
```

Die App ist anschließend unter einer der angezeigten URLs erreichbar, typischerweise `http://localhost:5000` bis `http://localhost:5019`.

### Release-Build lokal testen

```bash
dotnet publish src/HalstuchLernApp/HalstuchLernApp.csproj -c Release -o release
```

Die veröffentlichten Dateien befinden sich in `release/wwwroot` und können mit einem beliebigen Static-File-Server getestet werden.

## Playwright-Tests / UI-Exploration

Das Skript `tests/explore_app.py` startet die App (falls nötig), navigiert durch alle Seiten, prüft Service Worker und Navigation und erstellt Screenshots.

### Voraussetzungen

```bash
python -m pip install playwright pillow
python -m playwright install chromium
```

### Headless (schnell, ohne sichtbaren Browser)

```bash
python tests/explore_app.py
```

### Headed (sichtbarer Browser mit Verzögerungen)

```bash
python tests/explore_app.py --headed
```

Alle Screenshots werden in `tests/screenshots/` gespeichert.

## PWA Installation

Die App kann auf dem Smartphone oder Desktop als App installiert werden:

1. App im Browser öffnen.
2. Im Browser-Menü auf **„Zum Home-Bildschirm hinzufügen“** bzw. **„App installieren“** tippen.
3. Die App erscheint dann mit dem CVJM Stetten Logo auf dem Home-Bildschirm.

Im installierten Zustand prüft die App beim Start auf Updates und bietet an, neue Versionen zu laden.

## Deployment

Das Deployment erfolgt automatisch über GitHub Actions:

- Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
- Auslöser: Push auf den Branch `main` oder manueller Start über `workflow_dispatch`
- Ziel: GitHub Pages

### Einmalige Einrichtung auf GitHub

Bevor der Workflow das erste Mal erfolgreich deployen kann, muss GitHub Pages im Repository aktiviert werden:

1. Im Repository auf GitHub zu **Settings** wechseln.
2. Im linken Menü **Pages** auswählen.
3. Unter **Build and deployment** als **Source** den Wert **GitHub Actions** auswählen.
4. Auf **Save** klicken.

Sobald Pages aktiv ist, wird bei jedem Push auf `main` automatisch deployed.

### Live-URL

Die App ist aktuell hier erreichbar:

```
https://lambrech.github.io/HalstuchLernApp/
```

## Versionierung

Die aktuelle Version ist **0.1.0-alpha.1**.

Version und Git-Commit-Hash werden während des Release-Builds in die Assembly geschrieben und auf der **Info-Seite** der App angezeigt. Dort findest du außerdem:

- Link zum aktuellen Git-Commit auf GitHub
- Service-Worker-Status
- Buttons zum Suchen nach Updates, Neuladen und Leeren des Caches

## Screenshots

Screenshots aller wichtigen Seiten befinden sich im Ordner [`tests/screenshots/`](tests/screenshots/) und werden durch `tests/explore_app.py` aktualisiert.

## Datenquellen

Die Lerninhalte basieren auf den Originalunterlagen des CVJM Stetten im Ordner [`raw/`](raw/):

- `AUFNAHMEPRÜFUNG.doc`
- `Halstuchprüfung .pdf`
- `Mädchenschaftsprüfung 2016 .docx`
- Weitere Bilder und Liedtexte

Die extrahierten Texte liegen unter `raw/_extracted/`.

## Offene Punkte / Roadmap

- [x] Lerninhalte für Aufnahmeprüfung und Mädchenschaft/Jungenschaft
- [x] Info-Seite mit Version, Git-Commit und Update-Funktion
- [x] PWA mit Service Worker und Cache-Verhalten
- [x] Playwright-UI-Exploration und Screenshots
- [ ] Quiz-Funktion (geplant für einen späteren Schritt)
- [ ] GitHub-Repository öffentlich schalten und GitHub Pages aktivieren
- [ ] Echte CVJM-Abzeichen-Bilder (CVJM-Dreieck, Weltbund) integrieren, falls vorhanden

