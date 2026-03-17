import customtkinter as ctk
from config.constants import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH, JSON_FILENAME, FONT_FAMILY, FONT_SIZES, CTK_APPEARANCE, CTK_THEME, COLORS, SUBJECTS_FILENAME
from services.notification import NotificationManager
from datetime import datetime, timedelta
from ui.timetable_view import TimetableView
from ui.edit_dialog import EditDialog
from ui.notification_popup import NotificationPopup
from ui.subjects_dialog import SubjectsDialog
from services.storage import load_timetable, save_timetable, load_subjects

class MainWindow:
    """Verwaltet das Hauptfenster """

    def __init__(self):
        ctk.set_appearance_mode(CTK_APPEARANCE)
        ctk.set_default_color_theme(CTK_THEME)
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(fg_color=COLORS["bg"])

        self.timetable = load_timetable(JSON_FILENAME)
        self.notification_manager = NotificationManager(self.timetable, self._show_notification)
    

        self._create_header()
        self.timetable_view = TimetableView(self.root, self.timetable)
        self._create_footer()

    def _create_header(self):
        """ Erstellt einen Header mit einer Live-Uhr """

        # Frame erstellen
        self.header_frame = ctk.CTkFrame(self.root, fg_color=COLORS["bg"])
        self.header_frame.pack(fill="x", pady=10)

        # Label erstellen
        label = ctk.CTkLabel(
            self.header_frame,
            text="📅 Stundenplan",
            font=(FONT_FAMILY, FONT_SIZES["title"]),
            text_color=COLORS["accent"],

        )
        label.pack()

        # Label für die Uhr
        self.clock_label = ctk.CTkLabel(
            self.header_frame,
            text="00:00:00",  # Platzhalter, wird später aktualisiert
            font=(FONT_FAMILY, FONT_SIZES["large"]),
        )
        self.clock_label.pack()

        # Label für das Datum
        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text="",  # Wird in _update_clock gesetzt
            font=(FONT_FAMILY, FONT_SIZES["normal"]),
        )
        self.date_label.pack()

        # Button für neue Stunde
        add_btn = ctk.CTkButton(
            self.header_frame,
            text="+ Neue Stunde",
            command=self._add_lesson,
            fg_color=COLORS["accent"],
            text_color="#000000",
            font=(FONT_FAMILY, FONT_SIZES["normal"])
        )
        add_btn.pack(pady=10)

        # Button für Fächer verwalten
        subjects_btn = ctk.CTkButton(
            self.header_frame,
            text="📚 Fächer verwalten",
            command=self._open_subjects_dialog,
            fg_color="#6B7280",
            font=(FONT_FAMILY, FONT_SIZES["normal"])
        )
        subjects_btn.pack(pady=(0, 10))

    def _update_clock(self):
        """ Aktualisiert die Uhrzeit jede Sekunde """
        # Aktuelle zeit holen
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.clock_label.configure(
            text=current_time
        )

        # Datum aktualisieren
        # Deutsche Wochentage
        german_days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        weekday = german_days[now.weekday()]
        date_text = f"{weekday}, {now.strftime('%d.%m.%Y')}"
        self.date_label.configure(text=date_text)
        
        self.timetable_view.highlight_current()
        self._update_countdown()
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

    def _create_footer(self):
        """Erstellt Footer mit Countdown und Legende."""
        
        # Footer Frame
        self.footer_frame = ctk.CTkFrame(self.root, fg_color=COLORS["bg"])
        self.footer_frame.pack(fill="x", pady=(5, 10), padx=20)
        
        # Zwei Spalten: Countdown links/mitte, Legende rechts
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)
        
        # Countdown Label (GROSS, oben)
        self.countdown_label = ctk.CTkLabel(
            self.footer_frame,
            text="",
            font=(FONT_FAMILY, 48),
            text_color=COLORS["accent"]
        )
        self.countdown_label.grid(row=0, column=0, pady=(0, 5), sticky="n")
        
        # Legende Frame (rechts)
        legend_frame = ctk.CTkFrame(self.footer_frame, fg_color=COLORS["bg"])
        legend_frame.grid(row=0, column=1, sticky="ne", padx=20)
        
        # Fach-Abkürzungen aus JSON laden
        abbreviations = load_subjects(SUBJECTS_FILENAME)
        
        # Legende erstellen (größere Schrift)
        for abbr, full_name in sorted(abbreviations.items()):
            item_frame = ctk.CTkFrame(legend_frame, fg_color=COLORS["bg"])
            item_frame.pack(anchor="w", pady=3)
            
            ctk.CTkLabel(
                item_frame,
                text=f"{abbr}:",
                font=(FONT_FAMILY, FONT_SIZES["large"], "bold"),
                text_color=COLORS["accent"],
                width=110
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame,
                text=full_name,
                font=(FONT_FAMILY, FONT_SIZES["large"])
            ).pack(side="left")

    def _get_next_teaching_lesson(self):
        """Findet die nächste Unterrichtsstunde (keine Praxis/Mittagspause/Frei)."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today_weekday = now.weekday()
        
        days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        
        # Heute noch eine Stunde?
        if today_weekday <= 4:
            day_name = days[today_weekday]
            for lesson in sorted(self.timetable.schedule[day_name], key=lambda x: x["start"]):
                if lesson["start"] > current_time:
                    if lesson["lesson_type"] not in ["Praxis", "Mittagspause", "Frei"]:
                        return lesson, 0  # 0 Tage bis zur Stunde
        
        # Nächste Tage prüfen
        for days_ahead in range(1, 6):
            next_weekday = (today_weekday + days_ahead) % 7
            if next_weekday > 4:
                continue
            day_name = days[next_weekday]
            for lesson in sorted(self.timetable.schedule[day_name], key=lambda x: x["start"]):
                if lesson["lesson_type"] not in ["Praxis", "Mittagspause", "Frei"]:
                    return lesson, days_ahead
        
        return None, None
    
    def _update_countdown(self):
        """Aktualisiert den Countdown zur nächsten Unterrichtsstunde."""
        lesson, days_until = self._get_next_teaching_lesson()
        
        if lesson is None:
            self.countdown_label.configure(text="📚 Kein Unterricht geplant")
            return
        
        now = datetime.now()
        
        # Zeit berechnen
        start_parts = lesson["start"].split(":")
        start_hour = int(start_parts[0])
        start_minute = int(start_parts[1])
        
        # Ziel-Datetime erstellen
        target = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
        target = target + timedelta(days=days_until)
        
        # Differenz berechnen
        diff = target - now
        
        if diff.total_seconds() <= 0:
            self.countdown_label.configure(text=f"📚 {lesson['subject']} beginnt jetzt!")
            return
        
        # Formatieren
        total_seconds = int(diff.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days_until > 0:
            text = f"⏱️ {lesson['subject']} in {days_until}T {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            text = f"⏱️ {lesson['subject']} in {hours:02d}:{minutes:02d}:{seconds:02d}"
        
        self.countdown_label.configure(text=text)

    def _open_subjects_dialog(self):
        """Öffnet den Dialog zum Verwalten der Fächer."""
        dialog = SubjectsDialog(self.root, on_save_callback=self._refresh_footer)
        self.root.wait_window(dialog.dialog)

    def _refresh_footer(self):
        """Aktualisiert den Footer (Legende) nach Fächer-Änderung."""
        self.footer_frame.destroy()
        self._create_footer()

