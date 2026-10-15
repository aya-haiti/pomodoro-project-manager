"""
Dialogue pour afficher les statistiques d'un projet
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QGroupBox, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from controllers.project_controller import ProjectController
from models.database_manager import DatabaseManager
from datetime import datetime

class StatisticsDialog(QDialog):
    """Dialogue pour afficher les statistiques d'un projet"""
    
    def __init__(self, parent=None, project_id: int = None, project_controller: ProjectController = None):
        super().__init__(parent)
        self.project_id = project_id
        self.project_controller = project_controller
        self.db_manager = DatabaseManager()
        
        self.setup_ui()
        self.load_statistics()
        
        # Configuration de la fenêtre
        self.setWindowTitle("Statistiques du projet")
        self.setModal(True)
        self.resize(600, 500)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        self.title_label = QLabel("Statistiques du projet")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Groupe des statistiques générales
        stats_group = QGroupBox("Résumé")
        stats_layout = QGridLayout(stats_group)
        
        # Labels pour les statistiques
        self.project_name_label = QLabel()
        self.project_name_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.total_sessions_label = QLabel()
        self.work_sessions_label = QLabel()
        self.completed_sessions_label = QLabel()
        self.total_time_label = QLabel()
        self.progress_label = QLabel()
        
        # Disposition des statistiques
        stats_layout.addWidget(QLabel("Projet:"), 0, 0)
        stats_layout.addWidget(self.project_name_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Sessions totales:"), 1, 0)
        stats_layout.addWidget(self.total_sessions_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Sessions de travail:"), 2, 0)
        stats_layout.addWidget(self.work_sessions_label, 2, 1)
        
        stats_layout.addWidget(QLabel("Sessions terminées:"), 3, 0)
        stats_layout.addWidget(self.completed_sessions_label, 3, 1)
        
        stats_layout.addWidget(QLabel("Temps total de travail:"), 4, 0)
        stats_layout.addWidget(self.total_time_label, 4, 1)
        
        stats_layout.addWidget(QLabel("Progression:"), 5, 0)
        stats_layout.addWidget(self.progress_label, 5, 1)
        
        layout.addWidget(stats_group)
        
        # Tableau des sessions
        sessions_group = QGroupBox("Historique des sessions")
        sessions_layout = QVBoxLayout(sessions_group)
        
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(5)
        self.sessions_table.setHorizontalHeaderLabels([
            "Type", "Durée", "Date/Heure", "Statut", "Temps écoulé"
        ])
        
        # Configuration du tableau
        header = self.sessions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        sessions_layout.addWidget(self.sessions_table)
        layout.addWidget(sessions_group)
        
        # Bouton de fermeture
        buttons_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Actualiser")
        self.close_button = QPushButton("Fermer")
        
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.close_button)
        
        layout.addLayout(buttons_layout)
        
        # Connexions
        self.refresh_button.clicked.connect(self.load_statistics)
        self.close_button.clicked.connect(self.accept)
        
        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
                gridline-color: #e9ecef;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton[text="Fermer"] {
                background-color: #6c757d;
            }
            
            QPushButton[text="Fermer"]:hover {
                background-color: #545b62;
            }
        """)
    
    def load_statistics(self):
        """Charge les statistiques du projet"""
        if not self.project_id or not self.project_controller:
            return
        
        # Récupérer les statistiques
        stats = self.project_controller.get_project_statistics(self.project_id)
        
        if not stats:
            return
        
        # Mettre à jour les labels
        self.project_name_label.setText(stats['project_name'])
        self.total_sessions_label.setText(str(stats['total_sessions']))
        self.work_sessions_label.setText(str(stats['work_sessions']))
        self.completed_sessions_label.setText(str(stats['completed_work_sessions']))
        
        # Temps total
        hours = stats['total_work_time_hours']
        minutes = stats['total_work_time_minutes']
        if hours >= 1:
            self.total_time_label.setText(f"{hours} heures ({minutes} minutes)")
        else:
            self.total_time_label.setText(f"{minutes} minutes")
        
        # Progression
        progress = stats['progress_percentage']
        status = "Terminé" if stats['is_completed'] else "En cours"
        self.progress_label.setText(f"{progress:.1f}% ({status})")
        
        # Charger l'historique des sessions
        print("StatisticsDialog: Calling load_sessions_history.")
        self.load_sessions_history()
    
    def load_sessions_history(self):
        """Charge l'historique des sessions dans le tableau"""
        print("StatisticsDialog: load_sessions_history called.")
        sessions = self.db_manager.get_sessions_by_project(self.project_id)
        print(f"StatisticsDialog: Retrieved {len(sessions)} sessions from DB.")
        
        self.sessions_table.setRowCount(len(sessions))
        
        for row, session in enumerate(sessions):
            # Type de session
            type_names = {
                'work': 'Travail',
                'short_break': 'Pause courte',
                'long_break': 'Pause longue'
            }
            type_item = QTableWidgetItem(type_names.get(session.session_type, session.session_type))
            self.sessions_table.setItem(row, 0, type_item)
            
            # Durée
            duration_item = QTableWidgetItem(f"{session.duration} min")
            self.sessions_table.setItem(row, 1, duration_item)
            
            # Date et heure
            if session.start_time:
                date_str = session.start_time.strftime("%d/%m/%Y %H:%M")
            else:
                date_str = "N/A"
            date_item = QTableWidgetItem(date_str)
            self.sessions_table.setItem(row, 2, date_item)
            
            # Statut
            status = "Terminée" if session.completed else "Interrompue"
            status_item = QTableWidgetItem(status)
            if session.completed:
                status_item.setBackground(Qt.green)
            else:
                status_item.setBackground(Qt.yellow)
            self.sessions_table.setItem(row, 3, status_item)
            
            # Temps écoulé
            elapsed = session.get_elapsed_time()
            if elapsed is not None:
                elapsed_minutes = elapsed // 60
                elapsed_seconds = elapsed % 60
                elapsed_str = f"{elapsed_minutes}:{elapsed_seconds:02d}"
            else:
                elapsed_str = "N/A"
            elapsed_item = QTableWidgetItem(elapsed_str)
            self.sessions_table.setItem(row, 4, elapsed_item)