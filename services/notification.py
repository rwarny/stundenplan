from datetime import datetime, date
from config.constants import NOTIFICATION_MINUTES_BEFORE, NOTIFICATION_TRIGGERS

class NotificationManager:
    """ Verwaltet die Benachrichtigungen """
    def __init__(self, timetable, callback):
        self.timetable = timetable
        self.callback = callback
        self.notified_lessons = set()
        self.last_date = date.today()

    def check_notifications(self):
        """ Prüft ob eine Benachrichtigung ausgelöst werden soll """
        # Nächste Stunde holen:
        next_lesson = self.timetable.get_next_lesson()
        if next_lesson is None:
            return
        
        # Aktuelle Zeit in Minuten
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute

        # Startzeit der nächsten Lesson in Minuten
        start_time = next_lesson["start"]
        hours, minutes = start_time.split(":")
        start_minutes = int(hours) * 60 + int(minutes)

        # Differenz berechnen
        minutes_until_start = start_minutes - current_minutes

        # Is es 5 Minuten oder weniger bis zum Start
        if minutes_until_start > NOTIFICATION_MINUTES_BEFORE:
            return # Zu Früh
        
        # Wurde diese Lesson schon benachrichtigt?
        if next_lesson["start"] in self.notified_lessons:
            return # Schon benachrichtigt
        
        # Vorherige Lesson prüfen (Benachrichtigungen nur wenn vohrer Praxis oder Mittagspause)
        # Hole vorherige Lesson
        previous_lesson = self.timetable.get_previous_lesson()

        # Keine vorherige? Dann keine Benachrichtigung
        if previous_lesson is None:
            return
        # War vorherige lesson Mittagspause oder Praxis?
        if previous_lesson["lesson_type"] not in NOTIFICATION_TRIGGERS:
            return # Keine Benachrichtigung
        
        # Benachrichtigung auslosen
        self.notified_lessons.add(next_lesson["start"])
        self.callback(next_lesson)

    def reset_daily(self):
        """ Setzt die benachrichtigten Lessonst zurück wenn ein neuer Tag beginnt """

        # aktuellen Tag holen
        today = date.today()
        if today != self.last_date:
            self.notified_lessons.clear()
            self.last_date = date.today()

            