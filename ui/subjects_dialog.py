import customtkinter as ctk
from config.constants import COLORS, FONT_FAMILY, FONT_SIZES, SUBJECTS_FILENAME
from services.storage import load_subjects, save_subjects

class SubjectsDialog:
    """Dialog zum Verwalten der Fächer."""
    
    def __init__(self, parent, on_save_callback=None):
        self.subjects = load_subjects(SUBJECTS_FILENAME)
        self.on_save_callback = on_save_callback
        self.result = False
        
        # Dialog erstellen
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Fächer verwalten")
        self.dialog.geometry("500x500")
        self.dialog.grab_set()
        
        # UI erstellen
        self._create_list()
        self._create_add_form()
        self._create_buttons()
    
    def _create_list(self):
        """Erstellt die Liste der Fächer."""
        # Überschrift
        ctk.CTkLabel(
            self.dialog,
            text="Aktuelle Fächer:",
            font=(FONT_FAMILY, FONT_SIZES["large"], "bold")
        ).pack(pady=(15, 5))
        
        # Frame für Liste
        self.list_frame = ctk.CTkScrollableFrame(self.dialog, height=150)
        self.list_frame.pack(fill="x", padx=20, pady=5)
        
        self._refresh_list()
    
    def _refresh_list(self):
        """Aktualisiert die Fächer-Liste."""
        # Alte Einträge löschen
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Fächer anzeigen
        for abbr, name in self.subjects.items():
            row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row,
                text=f"{abbr}:",
                font=(FONT_FAMILY, FONT_SIZES["normal"], "bold"),
                text_color=COLORS["accent"],
                width=80
            ).pack(side="left")
            
            ctk.CTkLabel(
                row,
                text=name,
                font=(FONT_FAMILY, FONT_SIZES["normal"])
            ).pack(side="left", fill="x", expand=True)
            
            # Löschen-Button
            ctk.CTkButton(
                row,
                text="✕",
                width=30,
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                command=lambda a=abbr: self._delete_subject(a)
            ).pack(side="right")
    
    def _create_add_form(self):
        """Erstellt das Formular zum Hinzufügen."""
        ctk.CTkLabel(
            self.dialog,
            text="Neues Fach hinzufügen:",
            font=(FONT_FAMILY, FONT_SIZES["large"], "bold")
        ).pack(pady=(20, 5))
        
        form_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form_frame.pack(fill="x", padx=20)
        
        # Abkürzung
        ctk.CTkLabel(form_frame, text="Abkürzung:").pack(side="left")
        self.abbr_entry = ctk.CTkEntry(form_frame, width=80)
        self.abbr_entry.pack(side="left", padx=5)
        
        # Name
        ctk.CTkLabel(form_frame, text="Name:").pack(side="left", padx=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=200)
        self.name_entry.pack(side="left", padx=5)
        
        # Hinzufügen-Button
        ctk.CTkButton(
            form_frame,
            text="+",
            width=30,
            command=self._add_subject
        ).pack(side="left", padx=5)
    
    def _create_buttons(self):
        """Erstellt die Buttons unten."""
        btn_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Speichern & Schließen",
            fg_color="#4CAF50",
            command=self._save_and_close
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Abbrechen",
            fg_color="#95A5A6",
            command=self.dialog.destroy
        ).pack(side="left", padx=5)
    
    def _add_subject(self):
        """Fügt ein neues Fach hinzu."""
        abbr = self.abbr_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if abbr and name:
            self.subjects[abbr] = name
            self.abbr_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
            self._refresh_list()
    
    def _delete_subject(self, abbr):
        """Löscht ein Fach."""
        if abbr in self.subjects:
            del self.subjects[abbr]
            self._refresh_list()
    
    def _save_and_close(self):
        """Speichert und schließt den Dialog."""
        save_subjects(self.subjects, SUBJECTS_FILENAME)
        self.result = True
        if self.on_save_callback:
            self.on_save_callback()
        self.dialog.destroy()