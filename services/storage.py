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


