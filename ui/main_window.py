import tkinter as tk
from config.constants import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH, COLORS, JSON_FILENAME, FONT_FAMILY, FONT_SIZES
from services.storage import load_timetable, save_timetable
from services.notification import NotificationManager
from datetime import datetime
from ui.timetable_view import TimetableView
from ui.edit_dialog import EditDialog
from ui.notification_popup import NotificationPopup

class MainWindow:
    """Verwaltet das Hauptfenster """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.config(bg=COLORS["bg"])

        self.timetable = load_timetable(JSON_FILENAME)
        self.notification_manager = NotificationManager(self.timetable, self._show_notification)
    

        self._create_header()
        self.timetable_view = TimetableView(self.root, self.timetable)

    def _show_notification(self, lesson):
        """ Zeigt Bneachrichtigungs-Popup """
        pass

    def _create_header(self):
        """ Erstellt einen Header mit einer Live-Uhr """

        # Frame erstellen
        self.header_frame = tk.Frame(self.root, bg=COLORS["header_bg"])
        self.header_frame.pack(fill="x", pady=10)

        # Label erstellen
        label = tk.Label(
            self.header_frame,
            text="📅 Stundenplan",
            font=(FONT_FAMILY, FONT_SIZES["title"]),
            fg=COLORS["accent"],
            bg=COLORS["header_bg"]
        )
        label.pack()

        # Label für die Uhr
        self.clock_label = tk.Label(
            self.header_frame,
            text="00:00:00",  # Platzhalter, wird später aktualisiert
            font=(FONT_FAMILY, FONT_SIZES["large"]),
            fg=COLORS["fg"],
            bg=COLORS["header_bg"]
        )
        self.clock_label.pack()

        # Label für das Datum
        self.date_label = tk.Label(
            self.header_frame,
            text="",  # Wird in _update_clock gesetzt
            font=(FONT_FAMILY, FONT_SIZES["normal"]),
            fg=COLORS["fg"],
            bg=COLORS["header_bg"]
        )
        self.date_label.pack()

        # Button für neue Stunde
        add_btn = tk.Button(
            self.header_frame,
            text="+ Neue Stunde",
            command=self._add_lesson,
            bg=COLORS["accent"],
            fg="#000000",
            font=(FONT_FAMILY, FONT_SIZES["normal"])
        )
        add_btn.pack(pady=10)

    def _update_clock(self):
        """ Aktualisiert die Uhrzeit jede Sekunde """
        # Aktuelle zeit holen
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.clock_label.config(
            text=current_time
        )

        # Datum aktualisieren
        # Deutsche Wochentage
        german_days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        weekday = german_days[now.weekday()]
        date_text = f"{weekday}, {now.strftime('%d.%m.%Y')}"
        self.date_label.config(text=date_text)
        
        self.timetable_view.highlight_current()
        self.root.after(1000, self._update_clock)

    def _check_notifications(self):
        """ Prüft alle 10 Sekunden auf Benachrichtigungen """
        self.notification_manager.reset_daily()
        self.notification_manager.check_notifications()
        self.root.after(10000, self._check_notifications)

    def run(self):
        """ Startet die Anwendung """
        self._update_clock()
        self._check_notifications()
        self.root.mainloop()

    def _add_lesson(self):
        """ Öffnet Dialog für neue Lesson. """
        dialog = EditDialog(self.root, self.timetable)
        self.root.wait_window(dialog.dialog) # Warte bis Dialog geschlossen

        if dialog.result: # Wurde gespeichert
            save_timetable(self.timetable, JSON_FILENAME)
            self.timetable_view.refresh()

    def _show_notification(self, lesson):
        """Zeigt Benachrichtigungs-Popup."""
        NotificationPopup(self.root, lesson)