# X11 Input Monitor

**⚠️ WICHTIGER HINWEIS ZUR SICHERHEIT**  
Dieses Projekt dient ausschließlich Demonstrations- und Bildungszwecken. Die Überwachung von Benutzereingaben ohne ausdrückliche Zustimmung kann gegen geltende Gesetze verstoßen. Verwenden Sie dieses Tool nur in kontrollierten Umgebungen und mit ausdrücklicher Erlaubnis aller beteiligten Parteien.

## Überblick

Dieses Projekt demonstriert die inhärenten Sicherheitslücken im X11-Window-System, insbesondere im Zusammenhang mit der globalen Zwischenablage und Tastatureingaben. Es zeigt auf, wie einfach es für jedes Programm ist, ohne besondere Berechtigungen auf diese sensiblen Daten zuzugreifen.

## Sicherheitsrisiko X11

X11, das seit 1984 existiert (letztes Major-Release X11R7.7 war 2012), wurde in einer Zeit entworfen, in der Sicherheit nicht die höchste Priorität hatte. Dies führt zu mehreren kritischen Sicherheitsproblemen:

1. **Globale Tastatureingaben**: Jedes Programm kann Tastatureingaben abfangen, die in anderen Fenstern getätigt werden.
2. **Globale Zwischenablage**: Die X11-Zwischenablage ist für alle Anwendungen zugänglich, ohne dass der Benutzer darüber informiert wird.
3. **Keine Sandboxing-Möglichkeiten**: Programme haben standardmäßig vollen Zugriff auf alle Eingabegeräte.

### X11 vs. Wayland

Im Gegensatz zu X11 wurde Wayland (erste stabile Version 2012) mit Fokus auf Sicherheit entwickelt:
- Programme können nur auf eigene Fensterinhalte zugreifen
- Kein globaler Zugriff auf Tastatureingaben anderer Anwendungen
- Eingeschränkter Zugriff auf die Zwischenablage
- Sandboxing durch Portalsysteme

## Funktionen

- [x] Echtzeit-Überwachung der X11-Zwischenablage
- [x] Aufzeichnung von Tastatureingaben inkl. Tastenkombinationen
- [x] Benutzerfreundliche Terminal-UI mit farbiger Ausgabe
- [x] Anzeige des eingegebenen Texts in Echtzeit
- [x] Plattformübergreifende Kompatibilität (nur X11-basierte Systeme)

## Technische Voraussetzungen

- Python 3.12 oder höher
- X11-Server (nicht kompatibel mit Wayland)
- Python-Paketmanager `uv` (empfohlen) oder `pip`
- X11-Entwicklungsbibliotheken (libx11-dev, libxtst-dev, etc.)

## Installation

### Voraussetzungen

#### Ubuntu/Debian
```bash
sudo apt-get install python3-dev libx11-dev libxtst-dev
```

#### Fedora/RHEL
```bash
sudo dnf install python3-devel libX11-devel libXtst-devel
```

#### Arch Linux
```bash
sudo pacman -S python xorg-xprop xorg-xwininfo
```

### Installation mit uv (empfohlen)

```bash
# Repository klonen
git clone https://github.com/yourusername/x11-input-monitor.git
cd x11-input-monitor

# Abhängigkeiten installieren
uv sync
```

### Installation mit pip

```bash
pip install -e .
```

```bash
pip install git+https://github.com/yourusername/x11-input-monitor.git
```

## Verwendung

### Grundlegende Verwendung

Starten Sie das Programm mit:

```bash
uv run python -m x11_input_monitor
```

### Tastaturkürzel
- `Q` - Programm beenden
- `STRG+C` - Programm beenden (im Terminal)

## Sicherheitshinweise

1. **Nur für Bildungszwecke**: Dieses Tool dient der Veranschaulichung von Sicherheitslücken.
2. **Verantwortungsvolle Nutzung**: Verwenden Sie das Tool nur auf Systemen, für die Sie die Berechtigung haben.
3. **Keine bösartige Nutzung**: Das Abfangen von Benutzereingaben ohne Zustimmung ist in den meisten Ländern illegal.

## Technische Details
x11-input-monitor --help
```

### Ausgabe

- Tastatureingaben werden in Echtzeit in der Konsole ausgegeben.
- Änderungen an der Zwischenablage werden mit dem Inhalt in der Konsole protokolliert.

## Sicherheitshinweis

**WICHTIG**: Dieses Tool demonstriert Sicherheitslücken in X11. Verwenden Sie es nur in kontrollierten Umgebungen und niemals, um ohne ausdrückliche Erlaubnis auf die Eingaben anderer Benutzer zuzugreifen.

## Lizenz

MIT License

## Sicherheitshinweis

Dieses Projekt dient ausschließlich Bildungszwecken und zur Sensibilisierung für Sicherheitsthemen. Der Einsatz für böswillige Zwecke ist untersagt.
