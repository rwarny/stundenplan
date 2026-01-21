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
        """Prüft ob eine Benachrichtigung fällig ist."""
        next_lesson = self.timetable.get_next_lesson()
        
        if next_lesson is None:
            return
        
        # Hat diese Lesson Benachrichtigung aktiviert?
        if not next_lesson.get("notify", False):
            return
        
        # Zeit berechnen
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute
        
        start_parts = next_lesson["start"].split(":")
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        
        minutes_until = start_minutes - current_minutes
        
        # Benachrichtigung 5 Minuten vorher
        if minutes_until <= NOTIFICATION_MINUTES_BEFORE and minutes_until > 0:
            # Schon benachrichtigt?
            lesson_key = f"{next_lesson['start']}_{next_lesson['subject']}"
            if lesson_key not in self.notified_lessons:
                self.notified_lessons.add(lesson_key)
                self.callback(next_lesson)

    def reset_daily(self):
        """ Setzt die benachrichtigten Lessonst zurück wenn ein neuer Tag beginnt """

        # aktuellen Tag holen
        today = date.today()
        if today != self.last_date:
            self.notified_lessons.clear()
            self.last_date = date.today()

            
