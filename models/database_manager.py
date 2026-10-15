"""
Gestionnaire de base de données pour l'application Pomodoro
"""
import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict, Any
from config.database import DatabaseConfig
from models.project import Project
from models.pomodoro_session import PomodoroSession
from models.app_settings import AppSettings
from datetime import datetime

class DatabaseManager:
    """Gestionnaire de base de données utilisant le pattern Singleton"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.connect()
    
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self._connection = mysql.connector.connect(**DatabaseConfig.get_connection_params())
            print("Connexion à la base de données établie avec succès")
        except Error as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")
            self._connection = None
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Connexion à la base de données fermée")
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion est active"""
        return self._connection and self._connection.is_connected()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[tuple]]:
        """Exécute une requête SELECT et retourne les résultats"""
        if not self.is_connected():
            self.connect()
        
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Exécute une requête INSERT/UPDATE/DELETE"""
        if not self.is_connected():
            self.connect()
        
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params or ())
            self._connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erreur lors de l'exécution de la mise à jour: {e}")
            return False
    
    def get_last_insert_id(self) -> Optional[int]:
        """Retourne l'ID du dernier enregistrement inséré"""
        if not self.is_connected():
            return None
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            print(f"Erreur lors de la récupération du dernier ID: {e}")
            return None
    
    # Méthodes pour les projets
    def create_project(self, project: Project) -> Optional[int]:
        """Crée un nouveau projet dans la base de données"""
        query = """
        INSERT INTO projects (name, description, target_pomodoros, completed_pomodoros)
        VALUES (%s, %s, %s, %s)
        """
        params = (project.name, project.description, project.target_pomodoros, project.completed_pomodoros)
        
        if self.execute_update(query, params):
            return self.get_last_insert_id()
        return None
    
    def get_all_projects(self) -> List[Project]:
        """Récupère tous les projets de la base de données"""
        query = "SELECT id, name, description, target_pomodoros, completed_pomodoros, created_at, updated_at FROM projects ORDER BY created_at DESC"
        results = self.execute_query(query)
        
        projects = []
        if results:
            for row in results:
                project = Project(
                    id=row[0], name=row[1], description=row[2],
                    target_pomodoros=row[3], completed_pomodoros=row[4],
                    created_at=row[5], updated_at=row[6]
                )
                projects.append(project)
        
        return projects
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Récupère un projet par son ID"""
        query = "SELECT id, name, description, target_pomodoros, completed_pomodoros, created_at, updated_at FROM projects WHERE id = %s"
        results = self.execute_query(query, (project_id,))
        
        if results and len(results) > 0:
            row = results[0]
            return Project(
                id=row[0], name=row[1], description=row[2],
                target_pomodoros=row[3], completed_pomodoros=row[4],
                created_at=row[5], updated_at=row[6]
            )
        return None
    
    def update_project(self, project: Project) -> bool:
        """Met à jour un projet existant"""
        query = """
        UPDATE projects 
        SET name = %s, description = %s, target_pomodoros = %s, 
            completed_pomodoros = %s, updated_at = NOW()
        WHERE id = %s
        """
        params = (project.name, project.description, project.target_pomodoros, 
                 project.completed_pomodoros, project.id)
        
        return self.execute_update(query, params)
    
    def delete_project(self, project_id: int) -> bool:
        """Supprime un projet de la base de données"""
        query = "DELETE FROM projects WHERE id = %s"
        return self.execute_update(query, (project_id,))
    
    # Méthodes pour les sessions Pomodoro
    def create_session(self, session: PomodoroSession) -> Optional[int]:
        """Crée une nouvelle session Pomodoro"""
        query = """
        INSERT INTO pomodoro_sessions (project_id, session_type, duration, start_time, completed)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (session.project_id, session.session_type, session.duration, 
                 session.start_time, session.completed)
        
        if self.execute_update(query, params):
            return self.get_last_insert_id()
        return None
    
    def update_session(self, session: PomodoroSession) -> bool:
        """Met à jour une session existante"""
        query = """
        UPDATE pomodoro_sessions 
        SET end_time = %s, completed = %s
        WHERE id = %s
        """
        params = (session.end_time, session.completed, session.id)
        return self.execute_update(query, params)
    
    def get_sessions_by_project(self, project_id: int) -> List[PomodoroSession]:
        """Récupère toutes les sessions d'un projet"""
        query = """
        SELECT id, project_id, session_type, duration, start_time, end_time, completed, created_at
        FROM pomodoro_sessions 
        WHERE project_id = %s 
        ORDER BY created_at DESC
        """
        results = self.execute_query(query, (project_id,))
        
        sessions = []
        if results:
            for row in results:
                session = PomodoroSession(
                    id=row[0], project_id=row[1], session_type=row[2],
                    duration=row[3], start_time=row[4], end_time=row[5],
                    completed=row[6], created_at=row[7]
                )
                sessions.append(session)
        
        return sessions
    
    def get_completed_work_sessions_count(self, project_id: int) -> int:
        """Compte le nombre de sessions de travail terminées pour un projet"""
        query = """
        SELECT COUNT(*) FROM pomodoro_sessions 
        WHERE project_id = %s AND session_type = 'work' AND completed = TRUE
        """
        results = self.execute_query(query, (project_id,))
        return results[0][0] if results else 0
    
    # Méthodes pour les paramètres
    def get_app_settings(self) -> AppSettings:
        """Récupère les paramètres de l'application"""
        query = "SELECT id, work_duration, short_break_duration, long_break_duration, long_break_interval, notifications_enabled, daily_pomodoro_goal FROM app_settings LIMIT 1"
        results = self.execute_query(query)
        
        if results and len(results) > 0:
            row = results[0]
            return AppSettings(
                id=row[0], work_duration=row[1], short_break_duration=row[2],
                long_break_duration=row[3], long_break_interval=row[4],
                notifications_enabled=row[5], daily_pomodoro_goal=row[6]
            )
        else:
            # Créer des paramètres par défaut si aucun n'existe
            default_settings = AppSettings()
            self.create_app_settings(default_settings)
            return default_settings
    
    def create_app_settings(self, settings: AppSettings) -> bool:
        """Crée les paramètres de l'application"""
        query = """
        INSERT INTO app_settings (work_duration, short_break_duration, long_break_duration, long_break_interval, notifications_enabled, daily_pomodoro_goal)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (settings.work_duration, settings.short_break_duration, 
                 settings.long_break_duration, settings.long_break_interval, 
                 settings.notifications_enabled, settings.daily_pomodoro_goal)
        
        return self.execute_update(query, params)
    
    def update_app_settings(self, settings: AppSettings) -> bool:
        """Met à jour les paramètres de l'application"""
        query = """
        UPDATE app_settings 
        SET work_duration = %s, short_break_duration = %s, long_break_duration = %s,
            long_break_interval = %s, notifications_enabled = %s, daily_pomodoro_goal = %s
        WHERE id = %s
        """
        params = (settings.work_duration, settings.short_break_duration,
                 settings.long_break_duration, settings.long_break_interval,
                 settings.notifications_enabled, settings.daily_pomodoro_goal, settings.id)
        
        return self.execute_update(query, params)
    
    def get_completed_pomodoros_today(self) -> int:
        """Compte le nombre de Pomodoros (sessions de travail) terminés aujourd'hui"""
        query = """
        SELECT COUNT(*)
        FROM pomodoro_sessions
        WHERE session_type = 'work'
        AND completed = TRUE
        AND DATE(start_time) = CURDATE()
        """
        results = self.execute_query(query)
        return results[0][0] if results else 0