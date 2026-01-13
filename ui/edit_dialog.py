import tkinter as tk
from tkinter import ttk, messagebox
from config.constants import COLORS, FONT_FAMILY, FONT_SIZES, SUBJECT_COLORS
from config.time_config import WEEKDAYS, TIME_SLOTS

class EditDialog:
    """ Dialog zum Erstellen/Bearbeiten einer Lesson """
    def __init__(self, parent, timetable, day=None, lesson_index=None):
        self.timetable = timetable
        self.day = day
        self.lesson_index = lesson_index
        self.result = False # wurde gespeichert?

        # Neue oder bestehende Lesson?
        self.is_new = lesson_index is None

        # Dialog Fenster erstellen
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Neue Stunde" if self.is_new else "Stunde bearbeiten")
        self.dialog.geometry("400x350")
        self.dialog.configure(bg=COLORS["bg"])

        # Modal machen (blockiert Hauptfenster)
        self.dialog.grab_set()

        # Aufrufe
        self._create_form()
        self._create_buttons()

    def _create_form(self):
        """Erstellt die Eingabefelder."""
        
        # Häufige Fächer (kannst du später erweitern)
        self.frequent_subjects = ["NET-IS", "WiSo", "UML-OOP", "Konsultation Sebastian", "ReWe"]
        
        # Tag Auswahl (nur bei neuer Lesson)
        if self.is_new:
            tk.Label(self.dialog, text="Tag:", fg=COLORS["fg"], bg=COLORS["bg"]).pack(pady=(10,0))
            self.day_var = tk.StringVar()
            day_combo = ttk.Combobox(self.dialog, textvariable=self.day_var, values=WEEKDAYS, state="readonly")
            day_combo.pack(pady=5)
            day_combo.current(0)

        # Zeitslot-Auswahl
        tk.Label(self.dialog, text="Zeitslot:", fg=COLORS["fg"], bg=COLORS["bg"]).pack(pady=(10,0))
        self.time_var = tk.StringVar()
        time_options = [f"{start} - {end}" for start, end in TIME_SLOTS]
        time_combo = ttk.Combobox(self.dialog, textvariable=self.time_var, values=time_options, state="readonly")
        time_combo.pack(pady=5)
        time_combo.current(0)

        # === SCHNELLAUSWAHL (NEU!) ===
        quick_frame = tk.Frame(self.dialog, bg=COLORS["bg"])
        quick_frame.pack(pady=10)
        
        self.is_praxis = tk.BooleanVar(value=False)
        self.is_free = tk.BooleanVar(value=False)
        
        praxis_cb = tk.Checkbutton(
            quick_frame,
            text="Praxis",
            variable=self.is_praxis,
            command=self._on_quick_select,
            fg=COLORS["fg"],
            bg=COLORS["bg"],
            selectcolor=COLORS["bg"]
        )
        praxis_cb.pack(side="left", padx=10)
        
        free_cb = tk.Checkbutton(
            quick_frame,
            text="Frei",
            variable=self.is_free,
            command=self._on_quick_select,
            fg=COLORS["fg"],
            bg=COLORS["bg"],
            selectcolor=COLORS["bg"]
        )
        free_cb.pack(side="left", padx=10)

        # Fach Eingabe (mit Vorschlägen)
        tk.Label(self.dialog, text="Fach:", fg=COLORS["fg"], bg=COLORS["bg"]).pack(pady=(10,0))
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(
            self.dialog, 
            textvariable=self.subject_var, 
            values=self.frequent_subjects,
            width=27
        )
        self.subject_combo.pack(pady=5)

        # Typ Auswahl
        tk.Label(self.dialog, text="Typ:", fg=COLORS["fg"], bg=COLORS["bg"]).pack(pady=(10,0))
        self.type_var = tk.StringVar()
        type_options = list(SUBJECT_COLORS.keys())
        self.type_combo = ttk.Combobox(self.dialog, textvariable=self.type_var, values=type_options, state="readonly")
        self.type_combo.pack(pady=5)
        self.type_combo.current(0)
        
        # Wenn Bearbeiten: Werte vorausfüllen
        if not self.is_new:
            self._load_lesson_data()

    def _create_buttons(self):
        """ Erstellt die Buttons """

        # Button Frame
        btn_frame=tk.Frame(self.dialog, bg=COLORS["bg"])
        btn_frame.pack(pady=20)

        # Speichern-Button
        save_btn = tk.Button(
            btn_frame,
            text="Speichern",
            command=self._save,
            bg="#4CAF50",
            fg="white",
            width=10
        )
        save_btn.pack(side="left", padx=5)

        # Löschen-Button (nur beim Bearbeiten)
        if not self.is_new:
            delete_btn = tk.Button(
                btn_frame,
                text="Löschen",
                command=self._delete,
                bg="#FF6B6B",
                fg="white",
                width=10
            )
            delete_btn.pack(side="left", padx=5)

        # Abbrechen-Button
        cancel_btn = tk.Button(
            btn_frame,
            text="Abbrechen",
            command=self.dialog.destroy,
            bg="#95A5A6",
            fg="white",
            width=10
        )
        cancel_btn.pack(side="left", padx=5)

    def _save(self):
        """ Speichert die Lesson """
        # Validierung
        if not self.subject_var.get().strip():
            messagebox.showerror("FEHLER", "Bitte Fach angeben!")
            return
        
        # Zeitslot austeilen
        time_parts = self.time_var.get().split(" - ")
        start = time_parts[0]
        end = time_parts[1]

        # Tag bestimmen
        if self.is_new:
            day = self.day_var.get()
        else:
            day = self.day

        # Lesson-Daten
        subject = self.subject_var.get().strip()
        lesson_type = self.type_var.get()

        # Speichern
        if self.is_new:
            self.timetable.add_lesson(day, start, end, subject, lesson_type)
        else:
            new_data = {
                "start": start,
                "end": end,
                "subject": subject,
                "lesson_type": lesson_type
            }
            self.timetable.edit_lesson(day, self.lesson_index, new_data)

        # Erfolg markieren und schließen
        self.result = True
        self.dialog.destroy()

    def _delete(self):
        """ Löscht die Lesson """
        # Bestätigung
        if not messagebox.askyesno("Löschen", "Stunde wirklich löschen?"):
            return
        # Löschen
        self.timetable.delete_lesson(self.day, self.lesson_index)

        # Erfolg markieren und schließen
        self.result = True
        self.dialog.destroy()

    def _on_quick_select(self):
        """Wird aufgerufen wenn Praxis oder Frei angeklickt wird."""
        if self.is_praxis.get():
            self.is_free.set(False)
            self.subject_var.set("PE")
            self.type_var.set("Praxis")
        elif self.is_free.get():
            self.is_praxis.set(False)
            self.subject_var.set("")
            self.type_var.set("Frei")

    def _load_lesson_data(self):
        """Lädt die Daten der bestehenden Lesson in die Felder."""
        lesson = self.timetable.schedule[self.day][self.lesson_index]
        
        # Zeitslot setzen
        time_str = f"{lesson['start']} - {lesson['end']}"
        self.time_var.set(time_str)
        
        # Fach setzen
        self.subject_var.set(lesson["subject"])
        
        # Typ setzen
        self.type_var.set(lesson["lesson_type"])
        
        # Checkboxen setzen
        if lesson["lesson_type"] == "Praxis":
            self.is_praxis.set(True)
        elif lesson["lesson_type"] == "Frei":
            self.is_free.set(True)