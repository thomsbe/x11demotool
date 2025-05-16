# Projektübersicht

## Ziel
Entwicklung eines Demonstrationsprojekts zum Monitoring von Zwischenablageninhalten und Tastendrücken in einem X-Windows System. Das Projekt zeigt die Sicherheitsimplikationen auf, die sich aus der Architektur des X11-Protokolls ergeben.

## Implementierte Funktionalität

### Tastaturüberwachung
- Echtzeit-Erfassung aller Tastatureingaben
- Anzeige von Tastenkombinationen (inkl. Modifier-Tasten wie Strg, Alt, Shift)
- Spezielle Tastenbehandlung (Pfeiltasten, Funktionstasten, etc.)

### Zwischenablagen-Überwachung
- Automatische Erkennung von Änderungen in der Zwischenablage
- Anzeige des aktuellen Inhalts in Echtzeit
- Unterstützung für verschiedene Datentypen in der Zwischenablage

### Benutzeroberfläche
- Übersichtliche Text-UI mit getrennten Bereichen für Tastatureingaben, Zwischenablage und eingegebenen Text
- Farbige Hervorhebungen für bessere Lesbarkeit
- Einfache Steuerung (Q zum Beenden)

## Technische Details

### X11-spezifische Implementierung
Das Programm nutzt das X11-Protokoll über die `python-xlib`-Bibliothek, was folgende Implikation hat:

1. **Sicherheitsrisiken**:
   - X11 erlaubt es jedem Programm, Tastatureingaben abzufangen, die in anderen Fenstern getätigt werden
   - Die Zwischenablage ist global und für alle Anwendungen zugänglich
   - Keine Berechtigungsabfrage für den Zugriff auf diese Funktionen

2. **Technische Umsetzung**:
   - Verwendung der X11 Record Extension für Tastaturereignisse
   - Regelmäßige Abfrage der Zwischenablage über `pyperclip`
   - Thread-basierte Architektur für gleichzeitige Überwachung von Tastatur und Zwischenablage

### Wayland-Kompatibilität

Das Programm funktioniert **nicht** unter Wayland, dem moderneren Nachfolger von X11, aus folgenden Gründen:

1. **Sicherheitskonzept**:
   - Wayland hat ein strikteres Sicherheitsmodell
   - Programme können nur auf eigene Fensterinhalte zugreifen
   - Kein globaler Zugriff auf Tastatureingaben oder die Zwischenablage anderer Anwendungen

2. **Technische Einschränkungen**:
   - Die X11 Record Extension existiert in Wayland nicht
   - Der Zugriff auf die Zwischenablage ist eingeschränkt
   - Wayland erfordert spezielle APIs und Berechtigungen für Eingabeüberwachung

3. **Mögliche Alternativen für Wayland**:
   - Verwendung von `libinput` für eingeschränkte Eingabeüberwachung
   - Wayland-Protokolle wie `zwlr_foreign_toplevel_management` für Fensterverwaltung
   - Spezielle Berechtigungen über Portale (z.B. `xdg-desktop-portal`)
   - Installation als systemweiter Input-Method-Editor (IME)

## Technische Anforderungen

### Abhängigkeiten
- Python 3.12+
- `python-xlib` (X11-spezifisch)
- `pyperclip` (plattformunabhängige Zwischenablage)
- `urwid` (Terminal-UI)

### Installation
```bash
uv sync  # Installiert alle Abhängigkeiten
```

### Ausführung
```bash
uv run python -m x11_input_monitor
```

## Sicherheitshinweis

Dieses Projekt dient ausschließlich Demonstrations- und Bildungszwecken. Die Überwachung von Benutzereingaben ohne ausdrückliche Zustimmung kann gegen geltende Gesetze verstoßen. Verwenden Sie dieses Tool nur in kontrollierten Umgebungen und mit ausdrücklicher Erlaubnis aller beteiligten Parteien.