"""
Contrôleur pour la gestion des sessions Pomodoro
"""
from typing import List, Optional
from datetime import datetime
from models.database_manager import DatabaseManager
from models.pomodoro_session import PomodoroSession
from models.app_settings import AppSettings
from controllers.project_controller import ProjectController
from controllers.sound_controller import SoundController

class PomodoroController:
    """Contrôleur pour gérer les sessions Pomodoro"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.project_controller = ProjectController()
        self.sound_controller = SoundController()
        self.current_session: Optional[PomodoroSession] = None
    
    def start_work_session(self, project_id: int) -> Optional[PomodoroSession]:
        """Démarre une nouvelle session de travail"""
        if self.current_session and not self.current_session.completed:
            raise RuntimeError("Une session est déjà en cours")
        
        project = self.project_controller.get_project_by_id(project_id)
        if not project:
            raise ValueError("Projet introuvable")
        
        settings = self.db_manager.get_app_settings()
        
        session = PomodoroSession(
            project_id=project_id,
            session_type='work',
            duration=settings.work_duration,
            start_time=datetime.now()
        )
        
        session_id = self.db_manager.create_session(session)
        if session_id:
            session.id = session_id
            self.current_session = session
            self.sound_controller.play_session_start()
            return session
        
        return None
    
    def start_break_session(self, project_id: int, is_long_break: bool = False) -> Optional[PomodoroSession]:
        """Démarre une session de pause"""
        if self.current_session and not self.current_session.completed:
            raise RuntimeError("Une session est déjà en cours")
        
        settings = self.db_manager.get_app_settings()
        session_type = 'long_break' if is_long_break else 'short_break'
        duration = settings.long_break_duration if is_long_break else settings.short_break_duration
        
        session = PomodoroSession(
            project_id=project_id,
            session_type=session_type,
            duration=duration,
            start_time=datetime.now()
        )
        
        session_id = self.db_manager.create_session(session)
        if session_id:
            session.id = session_id
            self.current_session = session
            self.sound_controller.play_break_start()
            return session
        
        return None
    
    def complete_current_session(self) -> bool:
        """Termine la session en cours et démarre la suivante automatiquement"""
        print("PomodoroController: complete_current_session called.")
        if not self.current_session:
            print("PomodoroController: No current session to complete.")
            return False

        print(f"PomodoroController: Marking session {self.current_session.id} as completed.")
        self.current_session.mark_completed()
        success = self.db_manager.update_session(self.current_session)

        if success:
            print(f"PomodoroController: Session {self.current_session.id} updated in DB successfully.")
            if self.current_session.session_type == 'work':
                # Mettre à jour le compteur de Pomodoros du projet
                self.project_controller.update_completed_pomodoros(self.current_session.project_id)
                self.sound_controller.play_session_end()

                # Démarrer automatiquement une pause
                is_long_break = self.should_take_long_break(self.current_session.project_id)
                self.start_break_session(self.current_session.project_id, is_long_break)
            else:
                self.sound_controller.play_break_end()

                # Démarrer automatiquement une session de travail
                self.start_work_session(self.current_session.project_id)

            self.current_session = None # Clear current session only after successful update and sound played
            print("PomodoroController: current_session set to None.")
        else:
            print(f"PomodoroController: Failed to update session {self.current_session.id} in DB.")
        return success
    
    def cancel_current_session(self) -> bool:
        """Annule la session en cours"""
        if not self.current_session:
            return False
        
        # Marquer comme non terminée et mettre à jour
        self.current_session.completed = False
        self.current_session.end_time = datetime.now()
        success = self.db_manager.update_session(self.current_session)
        
        self.current_session = None
        return success
    
    def get_current_session(self) -> Optional[PomodoroSession]:
        """Retourne la session en cours"""
        return self.current_session
    
    def get_sessions_by_project(self, project_id: int) -> List[PomodoroSession]:
        """Récupère toutes les sessions d'un projet"""
        return self.db_manager.get_sessions_by_project(project_id)
    
    def should_take_long_break(self, project_id: int) -> bool:
        """Détermine s'il faut prendre une pause longue"""
        settings = self.db_manager.get_app_settings()
        completed_work_sessions = self.db_manager.get_completed_work_sessions_count(project_id)
        
        return (completed_work_sessions > 0 and 
                completed_work_sessions % settings.long_break_interval == 0)
    
    def get_next_session_type(self, project_id: int, last_completed_session_type: Optional[str] = None) -> str:
        """Détermine le type de la prochaine session"""
        print(f"PomodoroController: get_next_session_type called. last_completed_session_type: {last_completed_session_type}")

        if last_completed_session_type == 'work':
            if self.should_take_long_break(project_id):
                print("PomodoroController: Next session is long_break.")
                return 'long_break'
            else:
                print("PomodoroController: Next session is short_break.")
                return 'short_break'
        elif last_completed_session_type in ['short_break', 'long_break']:
            print("PomodoroController: Next session is work.")
            return 'work'
        else:
            # Cas initial ou si la dernière session n'est pas claire
            print("PomodoroController: Defaulting to work session.")
            return 'work'
    
    def get_session_duration(self, session_type: str) -> int:
        """Retourne la durée d'une session selon son type"""
        settings = self.db_manager.get_app_settings()
        return settings.get_duration_for_type(session_type)

    def get_daily_pomodoro_progress(self) -> dict:
        """Retourne le nombre de Pomodoros terminés aujourd'hui et l'objectif quotidien"""
        settings = self.db_manager.get_app_settings()
        completed_today = self.db_manager.get_completed_pomodoros_today()
        return {
            "completed_today": completed_today,
            "goal": settings.daily_pomodoro_goal
        }