
from datetime import datetime
from typing import List, Optional

class Project:
    
    def __init__(self, id: int = None, name: str = "", description: str = "", 
                 target_pomodoros: int = 8, completed_pomodoros: int = 0,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.name = name
        self.description = description
        self.target_pomodoros = target_pomodoros
        self.completed_pomodoros = completed_pomodoros
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __str__(self):
        return f"{self.name} ({self.completed_pomodoros}/{self.target_pomodoros})"
    
    def get_progress_percentage(self) -> float:
        """Calcule le pourcentage de progression du projet"""
        if self.target_pomodoros == 0:
            return 0.0
        return (self.completed_pomodoros / self.target_pomodoros) * 100
    
    def is_completed(self) -> bool:
        """Vérifie si le projet est terminé"""
        return self.completed_pomodoros >= self.target_pomodoros
    
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_pomodoros': self.target_pomodoros,
            'completed_pomodoros': self.completed_pomodoros,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }