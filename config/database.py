"""
Configuration de la base de données MySQL

Valeurs surchargeables par variables d'environnement :
POMODORO_DB_HOST, POMODORO_DB_USER, POMODORO_DB_PASSWORD, POMODORO_DB_NAME, POMODORO_DB_PORT
(par défaut : MySQL local de XAMPP, utilisateur root sans mot de passe).
"""
import os

class DatabaseConfig:
    """Configuration pour la connexion à la base de données MySQL"""
    
    HOST = os.getenv('POMODORO_DB_HOST', 'localhost')
    USER = os.getenv('POMODORO_DB_USER', 'root')
    PASSWORD = os.getenv('POMODORO_DB_PASSWORD', '')
    DATABASE = os.getenv('POMODORO_DB_NAME', 'pomodoro_app')
    PORT = int(os.getenv('POMODORO_DB_PORT', '3306'))
    
    @classmethod
    def get_connection_params(cls):
        """Retourne les paramètres de connexion sous forme de dictionnaire"""
        return {
            'host': cls.HOST,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'port': cls.PORT,
            'autocommit': True
        }