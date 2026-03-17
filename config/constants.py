""" Konstanten des Stundenplanes """

CTK_APPEARANCE = "dark"
CTK_THEME = "dark-blue"

# Farben
COLORS = {
    "accent": "#64FFDA",
    "cell_border": "#2d3748",
    "bg": '#1a1a2e'
}

SUBJECT_COLORS = {
    "AnwP": "#4CAF50",
    "BGP": "#2196F3",
    "ITT": "#9C24B0",
    "Praxis": "#F5F5DC",
    "Prüfung": "#FF6868",
    "Konsultation": "#F38C05",
    "Zusatzunterricht": "#1B042E",
    "Mittagspause": "#95A5A6",
    "Frei": "#34495E"
}

# Hauptfenster
WINDOW_TITLE = "Stundenplan"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FONT_FAMILY = "Segoe UI"
JSON_FILENAME = "timetable.json"
SUBJECTS_FILENAME = "subjects.json"

FONT_SIZES = {
    "small": 9,
    "normal": 11,
    "large": 14,
    "title": 18
}

NOTIFICATION_MINUTES_BEFORE = 5
NOTIFICATION_TRIGGERS = ["Mittagspause", "Praxis"]
