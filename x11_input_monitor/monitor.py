"""
Hauptmodul zur Überwachung von Tastatureingaben und der Zwischenablage in X11.
"""
import time
import pyperclip
import urwid
from datetime import datetime

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
import threading
import signal
import sys

class UI:
    """Benutzeroberfläche für den X11 Input Monitor."""
    
    def __init__(self):
        """Initialisiere die Text-UI."""
        # Farbpalette
        self.palette = [
            ('header', 'black', 'light gray'),
            ('footer', 'black', 'light gray'),
            ('keystrokes', 'yellow', 'black'),
            ('clipboard', 'light green', 'black'),
            ('text', 'white', 'black'),
        ]
        
        # Widgets erstellen
        self.keystrokes_widget = urwid.Text("Warte auf Tastatureingaben...")
        self.clipboard_widget = urwid.Text("Zwischenablage wird überwacht...")
        self.text_widget = urwid.Text("")
        
        # Layout
        keystrokes_box = urwid.LineBox(
            urwid.Filler(self.keystrokes_widget, valign='top'),
            title="Tastatureingaben"
        )
        
        clipboard_box = urwid.LineBox(
            urwid.Filler(self.clipboard_widget, valign='top'),
            title="Zwischenablage"
        )
        
        text_box = urwid.LineBox(
            urwid.Filler(self.text_widget, valign='top'),
            title="Eingegebener Text"
        )
        
        # Hauptlayout
        self.layout = urwid.Pile([
            ('pack', urwid.Text(('header', " X11 Input Monitor - Drücke Q zum Beenden "), align='center')),
            ('weight', 1, keystrokes_box),
            ('weight', 1, clipboard_box),
            ('weight', 2, text_box),
            ('pack', urwid.Text(('footer', " Drücke Q zum Beenden "), align='center'))
        ])
        
        self.loop = None
    
    def update_keystrokes(self, key_info: str):
        """Aktualisiere die Tastatureingaben-Anzeige."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.keystrokes_widget.set_text(f"[{timestamp}] {key_info}")
        self._refresh()
    
    def update_clipboard(self, content: str):
        """Aktualisiere die Zwischenablage-Anzeige."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        wrapped = '\n'.join([content[i:i+60] for i in range(0, min(len(content), 240), 60)])
        if len(content) > 240:
            wrapped += "\n..."
        self.clipboard_widget.set_text(f"[{timestamp}]\n{wrapped}")
        self._refresh()
    
    def update_text(self, text: str):
        """Aktualisiere den eingegebenen Text."""
        self.text_widget.set_text(text or "(noch keine Eingabe)")
        self._refresh()
    
    def _refresh(self):
        """Aktualisiere die Anzeige."""
        if self.loop:
            self.loop.draw_screen()
    
    def start(self):
        """Starte die Benutzeroberfläche."""
        self.loop = urwid.MainLoop(
            urwid.Filler(self.layout, valign='top'),
            self.palette,
            unhandled_input=self._handle_input
        )
        self.loop.run()
    
    def _handle_input(self, key):
        """Beende das Programm bei Q oder Strg+C."""
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

class X11InputMonitor:
    """Klasse zur Überwachung von X11-Eingaben mit Text-UI."""

    def __init__(self):
        """Initialisiere den X11-Monitor mit UI."""
        self.display = display.Display()
        self.root = self.display.screen().root
        self.record_display = display.Display()
        self.last_clipboard_content = pyperclip.paste()
        self.running = True
        self.typed_text = []
        
        # UI initialisieren
        self.ui = UI()

    def on_key_press(self, event):
        """Verarbeite Tastendruck-Ereignisse."""
        # Tastencode in Keysym umwandeln
        keysym = self.record_display.keycode_to_keysym(event.detail, 0)
        
        # Versuche, den Tastennamen zu bekommen
        key_name = XK.keysym_to_string(keysym)
        
        # Wenn kein Name gefunden wurde, versuche es mit dem Keysym-Namen
        if not key_name:
            try:
                key_name = XK.keysym_name(keysym).lower()
            except (AttributeError, TypeError):
                key_name = f"keycode_{event.detail}"
        else:
            # Konvertiere zu Kleinbuchstaben für die Konsistenz
            key_name = key_name.lower()
        
        # Spezielle Tasten behandeln
        special_keys = {
            ' ': 'space',
            '\n': 'return',
            '\t': 'tab',
            'escape': 'esc',
            'backspace': 'backspace',
            'delete': 'del',
            'left': '←',
            'right': '→',
            'up': '↑',
            'down': '↓',
            'home': 'home',
            'end': 'end',
            'page_up': 'pgup',
            'page_down': 'pgdn',
        }
        
        # Modifier-Tasten abfragen
        modifiers = []
        if event.state & X.ShiftMask:
            modifiers.append("SHIFT")
        if event.state & X.ControlMask:
            modifiers.append("STRG")
        if event.state & X.Mod1Mask:  # Alt-Taste
            modifiers.append("ALT")
        
        # Tastenkombination erstellen
        display_key = special_keys.get(key_name, key_name.upper())
        if modifiers:
            display_key = "+".join(modifiers + [display_key])
        
        # UI aktualisieren
        self.ui.update_keystrokes(display_key)
        
        # Text aktualisieren (nur für druckbare Zeichen)
        if len(key_name) == 1 or key_name in special_keys:
            self._update_typed_text(key_name, modifiers)

    def _update_typed_text(self, key_name: str, modifiers: list):
        """Aktualisiere den eingegebenen Text basierend auf der Taste."""
        # Spezielle Tasten behandeln
        if key_name == 'backspace':
            if self.typed_text:
                self.typed_text.pop()
        elif key_name == 'return':
            self.typed_text.append('\n')
        elif key_name == 'tab':
            self.typed_text.append('    ')
        elif key_name == 'space':
            self.typed_text.append(' ')
        elif len(key_name) == 1 and 'SHIFT' in modifiers:
            # Großbuchstaben für Shift + Buchstabe
            self.typed_text.append(key_name.upper())
        elif len(key_name) == 1 and key_name.isprintable():
            # Normale druckbare Zeichen
            self.typed_text.append(key_name)
        
        # UI aktualisieren
        self.ui.update_text(''.join(self.typed_text))

    def check_clipboard(self):
        """Überprüfe regelmäßig die Zwischenablage auf Änderungen."""
        while self.running:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard_content:
                    self.last_clipboard_content = current_clipboard
                    self.ui.update_clipboard(current_clipboard)
            except Exception as e:
                self.ui.update_clipboard(f"Fehler beim Lesen der Zwischenablage: {e}")
            time.sleep(0.5)  # Pause zwischen den Prüfungen

    def start_monitoring(self):
        """Starte die Überwachung der Tastatureingaben."""
        # Starte den Clipboard-Thread
        clipboard_thread = threading.Thread(target=self.check_clipboard, daemon=True)
        clipboard_thread.start()
        
        # Konfiguriere den Record-Client
        self.ctx = self.record_display.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyRelease),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])

        # Starte die UI
        try:
            # Starte den Record-Client in einem separaten Thread
            record_thread = threading.Thread(
                target=self.record_display.record_enable_context,
                args=(self.ctx, self.record_callback),
                daemon=True
            )
            record_thread.start()
            
            # Starte die UI (blockierend)
            self.ui.start()
            
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            if hasattr(self, 'ctx'):
                self.record_display.record_disable_context(self.ctx)
                self.record_display.flush()

    def record_callback(self, reply):
        """Callback für Record-Ereignisse."""
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or reply.data[0] < 2:
            # Nicht interessantes Event
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(
                data, self.record_display.display, None, None)

            if event.type == X.KeyPress:
                self.on_key_press(event)

def signal_handler(sig, frame, monitor=None):
    """Behandelt Signale zum sauberen Beenden."""
    print("\nBeende X11 Input Monitor...")
    if monitor:
        monitor.running = False
    sys.exit(0)

def main():
    """Hauptfunktion zum Starten der Überwachung."""
    monitor = None
    try:
        monitor = X11InputMonitor()
        
        # Signal-Handler für sauberes Beenden
        def signal_handler(sig, frame):
            print("\nBeende X11 Input Monitor...")
            if monitor:
                monitor.running = False
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print("X11 Input Monitor gestartet. Drücke Q oder STRG+C zum Beenden.")
        print("Aktiviere ein anderes Fenster und beginne mit der Eingabe...")
        monitor.start_monitoring()
        
    except KeyboardInterrupt:
        print("\nBeendet durch Benutzer.")
    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        if monitor:
            monitor.running = False

if __name__ == "__main__":
    main()
