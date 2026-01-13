import tkinter as tk
from config.constants import COLORS, FONT_FAMILY, FONT_SIZES, SUBJECT_COLORS

class NotificationPopup:
    """Popup-Fenster für Benachrichtigungen."""
    
    def __init__(self, parent, lesson):
        self.popup = tk.Toplevel(parent)
        self.popup.title("⏰ Erinnerung")
        self.popup.geometry("400x200")
        self.popup.configure(bg=COLORS["bg"])
        
        # Immer im Vordergrund
        self.popup.attributes("-topmost", True)
        
        # Inhalt erstellen
        self._create_content(lesson)
        
        # Piepton
        self.popup.bell()
    
    def _create_content(self, lesson):
        """Erstellt den Popup-Inhalt."""
        # Überschrift
        tk.Label(
            self.popup,
            text="⏰ Unterricht beginnt in 5 Minuten!",
            font=(FONT_FAMILY, FONT_SIZES["large"], "bold"),
            fg=COLORS["accent"],
            bg=COLORS["bg"]
        ).pack(pady=(20, 10))
        
        # Fach (groß)
        bg_color = SUBJECT_COLORS.get(lesson["lesson_type"], COLORS["bg"])
        tk.Label(
            self.popup,
            text=lesson["subject"],
            font=(FONT_FAMILY, FONT_SIZES["title"], "bold"),
            fg="white",
            bg=bg_color,
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Zeit
        tk.Label(
            self.popup,
            text=f"Beginn: {lesson['start']}",
            font=(FONT_FAMILY, FONT_SIZES["normal"]),
            fg=COLORS["fg"],
            bg=COLORS["bg"]
        ).pack(pady=5)
        
        # OK-Button
        tk.Button(
            self.popup,
            text="OK",
            command=self.popup.destroy,
            bg=COLORS["accent"],
            fg="#000000",
            width=15
        ).pack(pady=15)