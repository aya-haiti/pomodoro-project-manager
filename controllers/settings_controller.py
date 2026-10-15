"""
Contrôleur pour la gestion des paramètres de l'application
"""
from models.database_manager import DatabaseManager
from models.app_settings import AppSettings

class SettingsController:
    """Contrôleur pour gérer les paramètres de l'application"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_settings(self) -> AppSettings:
        """Récupère les paramètres actuels"""
        return self.db_manager.get_app_settings()
    
    def update_settings(self, work_duration: int, short_break_duration: int,
                       long_break_duration: int, long_break_interval: int,
                       notifications_enabled: bool) -> bool:
        """Met à jour les paramètres de l'application"""
        
        # Validation des données
        if work_duration <= 0 or work_duration > 120:
            raise ValueError("La durée de travail doit être entre 1 et 120 minutes")
        
        if short_break_duration <= 0 or short_break_duration > 60:
            raise ValueError("La durée de pause courte doit être entre 1 et 60 minutes")
        
        if long_break_duration <= 0 or long_break_duration > 120:
            raise ValueError("La durée de pause longue doit être entre 1 et 120 minutes")
        
        if long_break_interval <= 0 or long_break_interval > 10:
            raise ValueError("L'intervalle de pause longue doit être entre 1 et 10")
        
        settings = self.get_settings()
        settings.work_duration = work_duration
        settings.short_break_duration = short_break_duration
        settings.long_break_duration = long_break_duration
        settings.long_break_interval = long_break_interval
        settings.notifications_enabled = notifications_enabled
        
        return self.db_manager.update_app_settings(settings)
    
    def reset_to_defaults(self) -> bool:
        """Remet les paramètres aux valeurs par défaut"""
        return self.update_settings(
            work_duration=25,
            short_break_duration=5,
            long_break_duration=15,
            long_break_interval=4,
            notifications_enabled=True
        )