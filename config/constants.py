""" Konstanten des Stundenplanes """

# Farben
COLORS = {
    "bg": "#1a1a2e",
    "fg": "#E0E0E0",
    "accent": "#64FFDA",
    "header_bg": "#16213e",
    "cell_border": "#2d3748"
}

SUBJECT_COLORS = {
    "AnwP": "#4CAF50",
    "BGP": "#2196F3",
    "ITT": "#9C24B0",
    "Praxis": "#F5F5DC",
    "Prüfung": "#FF6868",
    "Konsultation": "#F38C05",
    "Zusatzunterricht": "#00CCFF",
    "Mittagspause": "#95A5A6",
    "Frei": "#34495E"
}

# Hauptfenster
WINDOW_TITLE = "Stundenplan"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FONT_FAMILY = "Segoe UI"
JSON_FILENAME = "timetable.json"

FONT_SIZES = {
    "small": 9,
    "normal": 11,
    "large": 14,
    "title": 18
}

NOTIFICATION_MINUTES_BEFORE = 5
NOTIFICATION_TRIGGERS = ["Mittagspause", "Praxis"]