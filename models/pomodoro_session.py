"""
Modèle pour la gestion des sessions Pomodoro
"""
from datetime import datetime
from typing import Optional

class PomodoroSession:
    """Classe représentant une session Pomodoro"""
    
    def __init__(self, id: int = None, project_id: int = None, 
                 session_type: str = "work", duration: int = 25,
                 start_time: datetime = None, end_time: datetime = None,
                 completed: bool = False, created_at: datetime = None):
        self.id = id
        self.project_id = project_id
        self.session_type = session_type  # 'work', 'short_break', 'long_break'
        self.duration = duration  # en minutes
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.completed = completed
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        status = "Terminée" if self.completed else "En cours"
        return f"{self.session_type.title()} - {self.duration}min ({status})"
    
    def get_duration_seconds(self) -> int:
        """Retourne la durée en secondes"""
        return self.duration * 60
    
    def mark_completed(self):
        """Marque la session comme terminée"""
        self.completed = True
        self.end_time = datetime.now()
    
    def get_elapsed_time(self) -> Optional[int]:
        """Calcule le temps écoulé en secondes depuis le début"""
        if not self.start_time:
            return None
        
        end_time = self.end_time or datetime.now()
        elapsed = end_time - self.start_time
        return int(elapsed.total_seconds())
    
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'session_type': self.session_type,
            'duration': self.duration,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'completed': self.completed,
            'created_at': self.created_at
        }