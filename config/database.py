"""
Configuration de la base de données MySQL
"""

class DatabaseConfig:
    """Configuration pour la connexion à la base de données MySQL"""
    
    HOST = 'localhost'
    USER = 'root'  # Changez selon votre configuration
    PASSWORD = ''  # Changez selon votre configuration
    DATABASE = 'pomodoro_app'
    PORT = 3306
    
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