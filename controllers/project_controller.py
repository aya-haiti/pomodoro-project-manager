"""
Contrôleur pour la gestion des projets
"""
from typing import List, Optional
from models.database_manager import DatabaseManager
from models.project import Project

class ProjectController:
    """Contrôleur pour gérer les opérations sur les projets"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def create_project(self, name: str, description: str = "", target_pomodoros: int = 8) -> Optional[Project]:
        """Crée un nouveau projet"""
        if not name.strip():
            raise ValueError("Le nom du projet ne peut pas être vide")
        
        if target_pomodoros <= 0:
            raise ValueError("Le nombre cible de Pomodoros doit être positif")
        
        project = Project(
            name=name.strip(),
            description=description.strip(),
            target_pomodoros=target_pomodoros
        )
        
        project_id = self.db_manager.create_project(project)
        if project_id:
            project.id = project_id
            return project
        
        return None
    
    def get_all_projects(self) -> List[Project]:
        """Récupère tous les projets"""
        return self.db_manager.get_all_projects()
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Récupère un projet par son ID"""
        return self.db_manager.get_project_by_id(project_id)
    
    def update_project(self, project: Project) -> bool:
        """Met à jour un projet existant"""
        if not project.name.strip():
            raise ValueError("Le nom du projet ne peut pas être vide")
        
        if project.target_pomodoros <= 0:
            raise ValueError("Le nombre cible de Pomodoros doit être positif")
        
        return self.db_manager.update_project(project)
    
    def delete_project(self, project_id: int) -> bool:
        """Supprime un projet"""
        return self.db_manager.delete_project(project_id)
    
    def update_completed_pomodoros(self, project_id: int) -> bool:
        """Met à jour le nombre de Pomodoros terminés pour un projet"""
        project = self.get_project_by_id(project_id)
        if not project:
            return False
        
        # Compter les sessions de travail terminées
        completed_count = self.db_manager.get_completed_work_sessions_count(project_id)
        project.completed_pomodoros = completed_count
        
        return self.update_project(project)
    
    def get_project_statistics(self, project_id: int) -> dict:
        """Récupère les statistiques d'un projet"""
        project = self.get_project_by_id(project_id)
        if not project:
            return {}
        
        sessions = self.db_manager.get_sessions_by_project(project_id)
        
        work_sessions = [s for s in sessions if s.session_type == 'work']
        completed_work_sessions = [s for s in work_sessions if s.completed]
        
        total_work_time = sum(s.duration for s in completed_work_sessions)
        
        return {
            'project_name': project.name,
            'total_sessions': len(sessions),
            'work_sessions': len(work_sessions),
            'completed_work_sessions': len(completed_work_sessions),
            'total_work_time_minutes': total_work_time,
            'total_work_time_hours': round(total_work_time / 60, 2),
            'progress_percentage': project.get_progress_percentage(),
            'is_completed': project.is_completed()
        }