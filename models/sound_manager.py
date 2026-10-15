"""
Gestionnaire de sons pour l'application Pomodoro
"""
import os
import pygame
import subprocess
import sys
from pathlib import Path

class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        print("SoundManager: Initializing pygame mixer...")
        try:
            pygame.mixer.init()
            print("SoundManager: Pygame mixer initialized successfully.")
        except Exception as e:
            print(f"SoundManager: Error initializing pygame mixer: {e}")
            self._initialized = True # Mark as initialized to prevent re-attempts if it keeps failing
            return
        
        # Chemin vers le dossier des sons
        self.sounds_dir = Path("assets/sounds")
        self.sounds_dir.mkdir(parents=True, exist_ok=True)
        
        # Sons par défaut
        self.sounds = {
            'session_start': None,
            'session_end': None,
            'break_start': None,
            'break_end': None
        }
        
        # Charger les sons
        self._load_default_sounds()
        self._initialized = True
    
    def _load_default_sounds(self):
        """Charge les sons par défaut"""
        # Créer les sons par défaut si ils n'existent pas
        self._create_default_sounds()
        
        # Charger les sons
        for sound_name in self.sounds.keys():
            sound_path = self.sounds_dir / f"{sound_name}.wav"
            if sound_path.exists():
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(str(sound_path))
                    print(f"SoundManager: Loaded {sound_name}.wav successfully.")
                except Exception as e:
                    print(f"SoundManager: Error loading {sound_name}.wav: {e}")
            else:
                print(f"SoundManager: {sound_name}.wav not found at {sound_path}")
    
    def _create_default_sounds(self):
        """Crée les sons par défaut si ils n'existent pas"""
        # Vérifier si tous les sons existent
        all_sounds_exist = all(
            (self.sounds_dir / f"{name}.wav").exists()
            for name in self.sounds.keys()
        )
        
        if not all_sounds_exist:
            # Exécuter le script de génération des sons
            script_path = Path("scripts/generate_default_sounds.py")
            if script_path.exists():
                try:
                    subprocess.run([sys.executable, str(script_path)], check=True)
                except subprocess.CalledProcessError:
                    print("Erreur lors de la génération des sons par défaut")
    
    def play_sound(self, sound_name):
        """Joue un son spécifique"""
        print(f"SoundManager: Attempting to play sound: {sound_name}")
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
                print(f"SoundManager: Successfully played sound: {sound_name}")
            except Exception as e:
                print(f"SoundManager: Error playing sound {sound_name}: {e}")
        else:
            print(f"SoundManager: Sound {sound_name} not loaded or does not exist.")
    
    def set_sound(self, sound_name, sound_path):
        """Définit un nouveau son"""
        if sound_name in self.sounds:
            if os.path.exists(sound_path):
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                return True
        return False
    
    def get_available_sounds(self):
        """Retourne la liste des sons disponibles"""
        return list(self.sounds.keys()) 