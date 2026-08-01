"""
HalstuchLernApp – Playwright-Exploration-Skript

Startet die App (falls nötig), navigiert durch alle wichtigen Seiten,
macht Screenshots und zeigt eine Zusammenfassung der Bedienung.

Aufruf:
    cd c:\\src\\_p\\CVJM\\HalstuchLernApp
    python tests\\explore_app.py

Das Skript sucht selbst nach einem laufenden lokalen Server auf den Ports
5000-5019. Falls keiner läuft, startet es `dotnet run` selbstständig.
"""

import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

APP_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = APP_ROOT / "src" / "HalstuchLernApp"
SCREENSHOT_DIR = APP_ROOT / "tests" / "screenshots"
BASE_URL = None  # wird ermittelt

ROUTES = [
    ("Startseite", "/"),
    ("Aufnahmeprüfung - Übersicht", "/category/aufnahme"),
    ("Zielsätze", "/topic/aufnahme/zielsaetze"),
    ("10 Gebote", "/topic/aufnahme/gebote"),
    ("Vater Unser", "/topic/aufnahme/vater-unser"),
    ("Losungsworte", "/topic/aufnahme/losungsworte"),
    ("Abzeichen", "/topic/aufnahme/abzeichen"),
    ("Lieder", "/topic/aufnahme/lieder"),
    ("Mädchenschaft / Jungenschaft", "/category/maedchen-jungen"),
    ("Pariser Basis", "/topic/maedchen-jungen/pariser-basis"),
    ("Ziele", "/topic/maedchen-jungen/ziele"),
    ("Glaubensbekenntnis", "/topic/maedchen-jungen/glaubensbekenntnis"),
    ("Einsetzungsworte", "/topic/maedchen-jungen/abendmahl"),
    ("Bibelstellen", "/topic/maedchen-jungen/bibelstellen"),
    ("Liedblatt", "/topic/maedchen-jungen/lieder-mj"),
    ("Info / Version & Updates", "/info"),
    ("Quiz (Platzhalter)", "/quiz"),
]


def find_running_server():
    """Sucht nach einem bereits laufenden Entwicklungsserver."""
    import urllib.request
    for port in range(5000, 5020):
        url = f"http://localhost:{port}"
        try:
            with urllib.request.urlopen(url, timeout=1):
                return url
        except Exception:
            continue
    return None


def start_server():
    """Startet `dotnet run` und wartet, bis der Server bereit ist."""
    print("Kein laufender Server gefunden. Starte dotnet run...")
    proc = subprocess.Popen(
        ["dotnet", "run", "--urls", "http://localhost:5016"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    url = "http://localhost:5016"
    for _ in range(60):
        import urllib.request
        try:
            with urllib.request.urlopen(url, timeout=1):
                print(f"Server läuft unter {url}")
                return proc, url
        except Exception:
            time.sleep(1)
    proc.kill()
    raise RuntimeError("Server konnte nicht gestartet werden.")


def take_screenshot(page, name: str):
    """Erstellt einen Screenshot und speichert ihn ab."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = name.replace(" / ", "_").replace(" ", "_").replace("-", "_")
    path = SCREENSHOT_DIR / f"{safe_name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  📸 Screenshot: {path}")
    return path


def check_service_worker(page) -> dict:
    """Prüft, ob der Service Worker registriert und aktiv ist."""
    return page.evaluate(
        """
        () => {
            if (!('serviceWorker' in navigator)) return { supported: false };
            return navigator.serviceWorker.ready.then(reg => ({
                supported: true,
                scope: reg.scope,
                state: reg.active?.state,
                hasController: !!navigator.serviceWorker.controller
            }));
        }
        """
    )


def main():
    global BASE_URL
    BASE_URL = find_running_server()
    server_proc = None

    if BASE_URL is None:
        server_proc, BASE_URL = start_server()
    else:
        print(f"Verwende laufenden Server: {BASE_URL}")

    print(f"\nScreenshots werden gespeichert in: {SCREENSHOT_DIR}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Startseite
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        print("✅ Startseite geladen")
        take_screenshot(page, "00_Startseite")

        # Logo prüfen
        logo = page.locator('img[alt="CVJM Stetten Logo"]').first
        if logo.is_visible():
            print("✅ Logo ist sichtbar")

        # Navigation prüfen
        nav_links = page.locator("nav a, .mud-drawer a, .mud-nav-link").all()
        print(f"✅ Navigation enthält {len(nav_links)} Links")

        # Service Worker prüfen
        sw = check_service_worker(page)
        print(f"✅ Service Worker: {sw}")

        # Alle Routen durchlaufen
        for idx, (name, route) in enumerate(ROUTES, start=1):
            url = f"{BASE_URL}{route}"
            print(f"\n[{idx}/{len(ROUTES)}] {name} ({route})")
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                take_screenshot(page, f"{idx:02d}_{name}")
                print(f"   Titel: {page.title()}")
            except Exception as ex:
                print(f"   ⚠️ Fehler: {ex}")

        # Mobile Ansicht
        print("\nTeste mobile Ansicht (iPhone-Größe)...")
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        take_screenshot(page, "99_Mobile_Startseite")

        # Menü auf Mobile öffnen
        menu_button = page.locator("header button").first
        if menu_button.is_visible():
            menu_button.click()
            page.wait_for_timeout(300)
            take_screenshot(page, "99_Mobile_Menu")
            print("✅ Mobiles Menü geöffnet")

        browser.close()

    if server_proc is not None:
        print("\nBeende gestarteten Server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    print("\n" + "=" * 60)
    print("FERTIG")
    print("=" * 60)
    print(f"Alle Screenshots befinden sich in: {SCREENSHOT_DIR}")
    print("\nBedienung der App:")
    print("- Startseite zeigt die beiden Lernbereiche.")
    print("- 'Themen anzeigen' öffnet die Kategorie-Übersicht.")
    print("- 'Lernen' öffnet die Detailseite eines Themas.")
    print("- Das Menü (☰) links enthält alle Themen direkt.")
    print("- 'Info' oben rechts zeigt Version, Git-Commit und Update-Funktionen.")
    print("- Auf dem Handy: Browser-Menü → 'Zum Home-Bildschirm hinzufügen' für PWA.")


if __name__ == "__main__":
    main()
