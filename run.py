
import sys
import os

# Ajouter le répertoire racine au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer et lancer l'application
from main import main

if __name__ == "__main__":
    print("=" * 50)
    print("🍅 APPLICATION POMODORO MULTI-PROJETS 🍅")
    print("=" * 50)
    print("Architecture MVC avec PySide6 et MySQL")
    print("Développé pour l'examen")
    print("=" * 50)
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication fermée par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur critique : {e}")
        sys.exit(1)