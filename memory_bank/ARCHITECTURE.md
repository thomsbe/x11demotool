# Architekturübersicht

## Systemarchitektur

### 1. Hauptkomponenten

#### X11InputMonitor-Klasse
- Zentrale Steuerung der Überwachungsfunktionen
- Initialisiert die X11-Verbindung und UI-Komponenten
- Verwaltet die Threads für Tastatur- und Zwischenablagen-Überwachung

#### UI-Klasse
- Textbasierte Benutzeroberfläche mit `urwid`
- Drei Hauptbereiche:
  - Tastatureingaben
  - Zwischenablageninhalt
  - Eingegebener Text
- Farbige Ausgabe für bessere Lesbarkeit

### 2. Überwachungskomponenten

#### Tastaturüberwachung
- Nutzt X11 Record Extension für Low-Level-Tastaturereignisse
- Erkennt Tastenkombinationen und Sondertasten
- Unterstützt verschiedene Tastaturlayouts

#### Zwischenablagen-Überwachung
- Regelmäßige Abfrage der X11-Zwischenablage
- Erkennung von Änderungen
- Anzeige verschiedener Inhaltstypen

### 3. Threading-Modell

```
Hauptthread (UI) ──┬─ Tastatur-Thread
                  └─ Zwischenablagen-Thread
```

## Technische Abhängigkeiten

### Externe Bibliotheken
- `python-xlib`: Low-Level X11-Zugriff
- `pyperclip`: Plattformübergreifende Zugriff auf die Zwischenablage
- `urwid`: Textbasierte Benutzeroberfläche

### Systemabhängigkeiten
- X11-Server (keine Wayland-Unterstützung)
- X11-Entwicklungsbibliotheken
- Python 3.12+

## Sicherheitsaspekte

### X11-spezifische Risiken
1. **Globale Tastatureingaben**: Jedes Programm kann Tastatureingaben abfangen
2. **Globale Zwischenablage**: Unbeschränkter Lesezugriff auf die Zwischenablage
3. **Keine Sandboxing-Möglichkeiten**: Programme haben vollen Systemzugriff

### Gegenmaßnahmen in der Implementierung
- Klare Kennzeichnung als Demonstrationsprojekt
- Keine dauerhafte Speicherung sensibler Daten
- Ausführliche Dokumentation der Sicherheitsrisiken

## Erweiterbarkeit

### Mögliche Erweiterungen
1. **Unterstützung für Wayland**: Über Portalsysteme
2. **Erweiterte Analyse**: Mustererkennung für sensible Daten
3. **Benachrichtigungen**: Bei bestimmten Ereignissen
4. **Protokollierung**: Optionale Aufzeichnung der Aktivitäten

## Teststrategie

### Unit-Tests
- Testen der Geschäftslogik
- Mocking der X11-Abhängigkeiten

### Integrationstests
- Testen der UI-Komponenten
- Überprüfung der Thread-Sicherheit

### Manuelle Tests
- Funktionsprüfung auf verschiedenen X11-Implementierungen
- Verhalten bei speziellen Tastenkombinationen
