"""
Contrôleur pour la gestion des sons
"""
from models.sound_manager import SoundManager

class SoundController:
    def __init__(self):
        self.sound_manager = SoundManager()
    
    def play_session_start(self):
        """Joue le son de début de session"""
        self.sound_manager.play_sound('session_start')
    
    def play_session_end(self):
        """Joue le son de fin de session"""
        self.sound_manager.play_sound('session_end')
    
    def play_break_start(self):
        """Joue le son de début de pause"""
        self.sound_manager.play_sound('break_start')
    
    def play_break_end(self):
        """Joue le son de fin de pause"""
        self.sound_manager.play_sound('break_end')
    
    def set_custom_sound(self, sound_name, sound_path):
        """Définit un son personnalisé"""
        return self.sound_manager.set_sound(sound_name, sound_path)
    
    def get_available_sounds(self):
        """Retourne la liste des sons disponibles"""
        return self.sound_manager.get_available_sounds() 