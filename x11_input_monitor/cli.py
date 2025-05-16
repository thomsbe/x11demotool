"""
Kommandozeilenschnittstelle für den X11 Input Monitor.
"""
import argparse
from x11_input_monitor import __version__

def parse_args():
    """Kommandozeilenargumente parsen."""
    parser = argparse.ArgumentParser(
        description='X11 Input Monitor - Überwacht Tastatureingaben und die Zwischenablage in X11.'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Zeigt die Versionsnummer an und beendet das Programm.'
    )
    
    return parser.parse_args()

def main():
    """Hauptfunktion der CLI."""
    _ = parse_args()  # args werden aktuell nicht benötigt
    from x11_input_monitor.monitor import main as monitor_main
    monitor_main()

if __name__ == '__main__':
    main()
