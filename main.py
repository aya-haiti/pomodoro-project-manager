

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from views.main_window import MainWindow
from models.database_manager import DatabaseManager

def check_database_connection():
    """Vérifie la connexion à la base de données"""
    try:
        db = DatabaseManager()
        if not db.is_connected():
            QMessageBox.critical(
                None, "Erreur de base de données",
                "Impossible de se connecter à la base de données MySQL.\n\n"
                "Vérifiez que :\n"
                "• MySQL est démarré\n"
                "• La base de données 'pomodoro_app' existe\n"
                "• Les paramètres de connexion sont corrects dans config/database.py\n"
                "• Vous avez exécuté le script database_setup.sql dans PHPMyAdmin"
            )
            return False
        return True
    except Exception as e:
        QMessageBox.critical(
            None, "Erreur",
            f"Erreur lors de la vérification de la base de données :\n{str(e)}"
        )
        return False

def main():
    """Fonction principale de l'application"""
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("Pomodoro Timer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Pomodoro App")
    
    # Style global de l'application
    app.setStyle('Fusion')
    
    # Vérifier la connexion à la base de données
    if not check_database_connection():
        sys.exit(1)
    
    try:
        # Créer et afficher la fenêtre principale
        window = MainWindow()
        window.show()
        
        # Démarrer la boucle d'événements
        sys.exit(app.exec())
        
    except Exception as e:
        QMessageBox.critical(
            None, "Erreur critique",
            f"Une erreur critique s'est produite :\n{str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()