# HalstuchLernApp

Eine einfache Progressive Web App (PWA) für die Halstuchprüfung / Aufnahmeprüfung im CVJM Stetten.

## Technologien

- Blazor WebAssembly (.NET 8)
- MudBlazor
- PWA mit Service Worker
- GitHub Pages

## Lokale Entwicklung

```bash
cd src/HalstuchLernApp
dotnet run
```

Die App ist dann unter `https://localhost:5001` erreichbar.

## Veröffentlichen

```bash
dotnet publish src/HalstuchLernApp/HalstuchLernApp.csproj -c Release -o release
```

Die veröffentlichten Dateien befinden sich in `release/wwwroot`.

## Deployment

Bei jedem Push auf `main` wird automatisch ein GitHub Pages Deployment über `.github/workflows/deploy.yml` ausgelöst.

## Version

Die aktuelle Version ist **0.1.0-alpha.1**.

Auf der Info-Seite der App werden die Version, der Git-Commit-Hash und weitere Build-Informationen angezeigt.
