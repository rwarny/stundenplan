import tkinter as tk
from config.constants import COLORS, FONT_FAMILY, FONT_SIZES, SUBJECT_COLORS, JSON_FILENAME
from config.time_config import WEEKDAYS, TIME_SLOTS
from datetime import datetime, timedelta
from ui.edit_dialog import EditDialog
from services.storage import save_timetable

class TimetableView:
    """ Verwaltet die Stundenplan-Ansicht """
    def __init__(self, parent, timetable):
        self.parent = parent
        self.timetable = timetable
        self.cells = {}

        # Frame erstellen
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Aufrufe
        self._create_header()
        self._create_time_column()
        self.populate()

        # Spaltenbreite konfigurieren
        self.frame.columnconfigure(0, minsize=120)  # Zeit-Spalte
        for i in range(1, 6):  # Spalten 1-5 (Wochentage)
            self.frame.columnconfigure(i, minsize=150, weight=1)

        # Zeilenhöhe konfigurieren
        for i in range(11):  # Zeilen 0-10 (Header + 10 Slots)
            self.frame.rowconfigure(i, minsize=40)

    def _create_header(self):
        """Erstellt die erste Zeile der Tabelle"""
        # Zeit Label erstellen
        time_label = tk.Label(
            self.frame,
            text="Zeit",
            font=(FONT_FAMILY, FONT_SIZES["normal"], "bold"),
            fg=COLORS["fg"],
            bg=COLORS["header_bg"]
        )
        time_label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        # Aktuellen Montag berechnen
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())  # Montag dieser Woche

        # Wochentage in Schleife erstellen
        for col, day in enumerate(WEEKDAYS):
            # Datum für diesen Tag berechnen
            day_date = monday + timedelta(days=col)
            date_str = day_date.strftime("%d.%m.")  # z.B. "07.01."
            
            # Ist heute dieser Tag?
            is_today = (col == today.weekday())
            
            # Farbe wählen
            if is_today:
                bg_color = COLORS["accent"]
                fg_color = "#000000"
            else:
                bg_color = COLORS["header_bg"]
                fg_color = COLORS["fg"]
            
            day_label = tk.Label(
                self.frame,
                text=f"{day}\n{date_str}",
                font=(FONT_FAMILY, FONT_SIZES["normal"], "bold"),
                fg=fg_color,
                bg=bg_color
            )
            day_label.grid(row=0, column=col + 1, sticky="nsew", padx=1, pady=1)

    def _create_time_column(self):
        """ Erstellt die Zeit-Spalte """
        for row, (start, end) in enumerate(TIME_SLOTS):
            tk.Label(self.frame,
                     text=f"{start} - {end}",
                     font=(FONT_FAMILY, FONT_SIZES["normal"]),
                     fg=COLORS["fg"],
                     bg=COLORS["bg"]).grid(row=row + 1, column=0, sticky="nsew", padx=1, pady=1)
            
    def _create_cell(self, lesson, row, col, day, lesson_index):
        """ Erstellt eine einzelne Zelle für eine Lesson """

        # Farbe basierend auf Fach holen
        bg_color = SUBJECT_COLORS.get(lesson["lesson_type"], COLORS["bg"])

        # Bei hellen Hintergründen = Dunkle Schrift
        if lesson["lesson_type"] == "Praxis":
            fg_color = "#000000"
        else:
            fg_color = COLORS["fg"]

             # Label erstellen
        cell = tk.Label(
            self.frame,
            text=lesson["subject"],
            font=(FONT_FAMILY, FONT_SIZES["normal"]),
            fg=fg_color,
            bg=bg_color
        )
        cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Click Event binden
        cell.bind("<Button-1>", lambda e, d=day, i=lesson_index: self._on_cell_click(d, i))
        
        # Zelle speichern für spätere Referenz
        self.cells[(row, col)] = cell

    def populate(self):
        """Trägt alle Lessons in die Tabelle ein."""
        
        for col, day in enumerate(WEEKDAYS):
            for row, time_slot in enumerate(TIME_SLOTS):
                
                # Feste Mittagspause?
                if time_slot[0] == "12:40":
                    fixed_lesson = {
                        "subject": "Mittagspause",
                        "start": time_slot[0],
                        "end": time_slot[1],
                        "lesson_type": "Mittagspause"
                    }
                    self._create_cell(fixed_lesson, row + 1, col + 1, day, None)
                    continue
                
                # Feste Praxisstunde?
                if time_slot[0] == "15:00":
                    fixed_lesson = {
                        "subject": "PE",
                        "start": time_slot[0],
                        "end": time_slot[1],
                        "lesson_type": "Praxis"
                    }
                    self._create_cell(fixed_lesson, row + 1, col + 1, day, None)
                    continue
                
                # Suche Lesson für diesen Slot
                found_lesson = None
                lesson_index = None
                for idx, lesson in enumerate(self.timetable.schedule[day]):
                    if lesson["start"] == time_slot[0]:
                        found_lesson = lesson
                        lesson_index = idx
                        break
                
                if found_lesson:
                    self._create_cell(found_lesson, row + 1, col + 1, day, lesson_index)
                else:
                    self._create_empty_cell(row + 1, col + 1, day, time_slot)

    def highlight_current(self):
        """ Hebt die aktuell laufende Stunde visuell hervor"""
        # Aktuelle Lesson holen
        current =self.timetable.get_current_lesson()
        if current is None:
            return
        
        # Wochentag bestimmen
        weekday_index = datetime.now().weekday()
        if weekday_index > 4:
            return
        col = weekday_index + 1

        # Zeile finden
        for row, (start, _) in enumerate(TIME_SLOTS):
            if start == current["start"]:
                # Zeile aus self.cells holen und markeiren
                cell = self.cells.get((row + 1, col))
                if cell:
                    cell.config(relief="solid", borderwidth=3)
                break

    def refresh(self):
        """ Baut die Tabelle neu auf (z.B. nach dem Bearbeiten einer Lesson) """
        # Alle Zeilen zerstören
        for cell in self.cells.values():
            cell.destroy()

        # Dictionary leeren
        self.cells.clear()

        # Neu befüllen
        self.populate()

    def _on_cell_click(self, day, lesson_index):
        """ Öffnet Edit-Dialog für angeklickte Lesson. """

        # Feste Slots nicht bearbeitbar
        if lesson_index is None:
            return
    
        dialog = EditDialog(self.parent, self.timetable, day, lesson_index)
        self.parent.wait_window(dialog.dialog)

        if dialog.result:
            save_timetable(self.timetable, JSON_FILENAME)
            self.refresh()

    def _create_empty_cell(self, row, col, day, time_slot):
        cell = tk.Label(
            self.frame,
            text="",
            bg=COLORS["bg"],
            relief="flat"
        )
        cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Click Event für neue Lesson
        cell.bind("<Button-1>", lambda e, d=day, t=time_slot: self._on_empty_cell_click(d, t))

        # Speichern
        self.cells[(row, col)] = cell 

    def _on_empty_cell_click(self, day, time_slot):
        """ Öffnet Edit-Dialog für neue Lesson an diesem Slot. """
        dialog = EditDialog(self.parent, self.timetable, day=day)

        # Zeitslot vorauswählen
        time_str = f"{time_slot[0]} - {time_slot[1]}"
        dialog.time_var.set(time_str)
        dialog.day_var.set(day)

        self.parent.wait_window(dialog.dialog)

        if dialog.result:
            save_timetable(self.timetable, JSON_FILENAME)
            self.refresh()