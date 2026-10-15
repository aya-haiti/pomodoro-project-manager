"""
Modèle pour la gestion des paramètres de l'application
"""

class AppSettings:
    """Classe représentant les paramètres de l'application"""
    
    def __init__(self, id: int = None, work_duration: int = 25, 
                 short_break_duration: int = 5, long_break_duration: int = 15,
                 long_break_interval: int = 4, notifications_enabled: bool = True,
                 daily_pomodoro_goal: int = 8):
        self.id = id
        self.work_duration = work_duration
        self.short_break_duration = short_break_duration
        self.long_break_duration = long_break_duration
        self.long_break_interval = long_break_interval
        self.notifications_enabled = notifications_enabled
        self.daily_pomodoro_goal = daily_pomodoro_goal
    
    def get_duration_for_type(self, session_type: str) -> int:
        """Retourne la durée appropriée selon le type de session"""
        durations = {
            'work': self.work_duration,
            'short_break': self.short_break_duration,
            'long_break': self.long_break_duration
        }
        return durations.get(session_type, self.work_duration)
    
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'work_duration': self.work_duration,
            'short_break_duration': self.short_break_duration,
            'long_break_duration': self.long_break_duration,
            'long_break_interval': self.long_break_interval,
            'notifications_enabled': self.notifications_enabled,
            'daily_pomodoro_goal': self.daily_pomodoro_goal
        }