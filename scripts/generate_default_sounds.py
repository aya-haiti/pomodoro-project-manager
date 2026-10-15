"""
Script pour générer les sons par défaut de l'application
"""
import os
import numpy as np
from scipy.io import wavfile
from pathlib import Path

def generate_sine_wave(frequency, duration, sample_rate=44100):
    """Génère une onde sinusoïdale"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * frequency * t)

def generate_sound(filename, frequency, duration, volume=0.5):
    """Génère un son et le sauvegarde en WAV"""
    # Générer l'onde
    wave = generate_sine_wave(frequency, duration)
    
    # Appliquer l'enveloppe
    envelope = np.exp(-np.linspace(0, 5, len(wave)))
    wave = wave * envelope
    
    # Normaliser et appliquer le volume
    wave = wave * volume
    
    # Convertir en 16-bit PCM
    wave = np.int16(wave * 32767)
    
    # Sauvegarder le fichier
    wavfile.write(filename, 44100, wave)

def main():
    # Créer le dossier des sons s'il n'existe pas
    sounds_dir = Path("assets/sounds")
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    # Générer les sons par défaut
    sounds = {
        'session_start': (440, 0.5),  # La4, 0.5 secondes
        'session_end': (880, 0.5),    # La5, 0.5 secondes
        'break_start': (660, 0.5),    # Mi5, 0.5 secondes
        'break_end': (550, 0.5)       # Do#5, 0.5 secondes
    }
    
    for name, (freq, duration) in sounds.items():
        filename = sounds_dir / f"{name}.wav"
        generate_sound(str(filename), freq, duration)

if __name__ == "__main__":
    main() 