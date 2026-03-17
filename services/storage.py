import json
import os
from models.timetable import Timetable

def save_timetable(timetable, filename):
    """ Speichert einen Stundenplan als json"""
    data = timetable.to_dict()

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_timetable(filename):
    """ Lädt einen Stundenplan """
    # Prüfen ob Datei existiert

    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
        return Timetable.from_dict(data)

    else:
        return Timetable()

def load_subjects(filename):
    """Lädt die Fächer aus JSON."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Standard-Fächer wenn Datei nicht existiert
        default = {
            "NET-IS": "Netzwerke & IT-Sicherheit",
            "PE": "Praxiseinheit"
        }
        # Sofort speichern damit die Datei existiert
        save_subjects(default, filename)
        return default

def save_subjects(subjects, filename):
    """Speichert die Fächer als JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(subjects, file, indent=4, ensure_ascii=False)
