from config.time_config import WEEKDAYS
from datetime import datetime

class Timetable:
    """ Das Zeitfenster des Stundesplans """
    def __init__(self):
        self.schedule = {}
        for day in WEEKDAYS:
            self.schedule[day] = []

    def add_lesson(self, day, start, end, subject, lesson_type):
        """ Fügt eine neue Stunde, an entsprechenden Tag, zur Passenden Stunde zum Stundeplan hinzu """
        lesson = {"start": start, "end": end, "subject": subject, "lesson_type": lesson_type}
        self.schedule[day].append(lesson)
    
    def edit_lesson(self, day, index, new_data):
        """ Bearbeitet eine existierende Stunde anhand des Indexes """
        self.schedule[day][index].update(new_data)
    
    def delete_lesson(self, day, index):
        """Löscht eine existierende Stunde anhand des Indexes """
        del self.schedule[day][index]

    def get_current_lesson(self):
        """ Findet heraus welche Stunde JETZT läuft """

        # Tag finden
        now = datetime.now()
        weekday_index = now.weekday()
        if weekday_index > 4:
            return None
        
        day_name = WEEKDAYS[weekday_index]
        current_time = now.strftime("%H:%M")
        
        # Zeit finden
        for lesson in self.schedule[day_name]:
            # Prüfe ob current_time zwischen start und en liegt
            if lesson["start"] <= current_time < lesson["end"]:
                return lesson
            
        # Falls keine Lesson gefunden
        return None
    
    def get_next_lesson(self):
        """ Findet die nächste Stunde des Tages """
        # Tag finden
        now = datetime.now()
        weekday_index = now.weekday()
        if weekday_index > 4:
            return None
        
        day_name = WEEKDAYS[weekday_index]
        current_time = now.strftime("%H:%M")
        
        # Zeit finden
        for lesson in self.schedule[day_name]:
            # Prüfe ob current_time zwischen start und end liegt
            if lesson["start"] > current_time:
                return lesson
            
        # Falls keine Lesson gefunden
        return None
    
    def get_previous_lesson(self):
        """ Findet die Stunde VOR der aktuellen/nächsten für eventuelle Benachrichtigung """
         # Tag finden
        now = datetime.now()
        weekday_index = now.weekday()
        if weekday_index > 4:
            return None
        
        day_name = WEEKDAYS[weekday_index]
        current_time = now.strftime("%H:%M")
        
        # lesson finden
        for index, lesson in enumerate(self.schedule[day_name]):
            # Wenn diese Lesson jetzt läuft oder als nöchstes kommt
            if lesson["end"] > current_time:
                # Gibt es eine davor?
                if index > 0:
                    return self.schedule[day_name][index-1]
                else:
                    return None

        # Falls keine Lesson gefunden
        return None
    
    def to_dict(self):
        """ Wandelt Timetable in Dictionary """
        return{"schedule": self.schedule}
    
    @classmethod
    def from_dict(cls, data):
        """ Erstellt Timetable aus Dictionary """
        timetable = cls()
        timetable.schedule = data["schedule"]
        return timetable
    