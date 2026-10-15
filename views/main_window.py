"""
Fenêtre principale de l'application Pomodoro
"""
import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QListWidget, QListWidgetItem,
                              QProgressBar, QSpinBox, QTextEdit, QLineEdit,
                              QDialog, QFormLayout, QCheckBox, QMessageBox,
                              QTabWidget, QTableWidget, QTableWidgetItem,
                              QHeaderView, QGroupBox, QGridLayout)
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QFont, QPalette, QColor
from controllers.project_controller import ProjectController
from controllers.pomodoro_controller import PomodoroController
from controllers.settings_controller import SettingsController
from views.project_dialog import ProjectDialog
from views.settings_dialog import SettingsDialog
from views.statistics_dialog import StatisticsDialog
from models.project import Project
import plyer
from typing import Optional

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    # Signaux personnalisés
    timer_updated = Signal(int)  # Signal émis quand le timer est mis à jour
    session_completed = Signal()  # Signal émis quand une session est terminée
    
    def __init__(self):
        super().__init__()
        
        # Contrôleurs
        self.project_controller = ProjectController()
        self.pomodoro_controller = PomodoroController()
        self.settings_controller = SettingsController()
        
        # Variables d'état
        self.current_project_id = None
        self.time_left = 0  # en secondes
        self.is_running = False
        
        # Timer Qt
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # Configuration de l'interface
        self.setup_ui()
        self.setup_connections()
        self.load_app_settings()
        self.load_projects()
        self.update_daily_progress_display()
        
        # Configuration de la fenêtre
        self.setWindowTitle("Pomodoro Timer - Gestion Multi-Projets")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Appliquer le style
        self.apply_styles()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Panneau gauche - Liste des projets
        left_panel = self.create_projects_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Panneau droit - Timer et contrôles
        right_panel = self.create_timer_panel()
        main_layout.addWidget(right_panel, 2)
    
    def create_projects_panel(self) -> QWidget:
        """Crée le panneau de gestion des projets"""
        panel = QGroupBox("Projets")
        layout = QVBoxLayout(panel)
        
        # Boutons de gestion des projets
        buttons_layout = QHBoxLayout()
        
        self.add_project_btn = QPushButton("Nouveau Projet")
        self.edit_project_btn = QPushButton("Modifier")
        self.delete_project_btn = QPushButton("Supprimer")
        self.stats_btn = QPushButton("Statistiques")
        
        buttons_layout.addWidget(self.add_project_btn)
        buttons_layout.addWidget(self.edit_project_btn)
        buttons_layout.addWidget(self.delete_project_btn)
        buttons_layout.addWidget(self.stats_btn)
        
        layout.addLayout(buttons_layout)
        
        # Liste des projets
        self.projects_list = QListWidget()
        self.projects_list.setMinimumHeight(200)
        layout.addWidget(self.projects_list)
        
        # Informations du projet sélectionné
        info_group = QGroupBox("Informations du projet")
        info_layout = QVBoxLayout(info_group)
        
        self.project_name_label = QLabel("Aucun projet sélectionné")
        self.project_name_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.project_description_label = QLabel("")
        self.project_description_label.setWordWrap(True)
        
        self.project_progress_label = QLabel("")
        self.project_progress_bar = QProgressBar()
        
        info_layout.addWidget(self.project_name_label)
        info_layout.addWidget(self.project_description_label)
        info_layout.addWidget(self.project_progress_label)
        info_layout.addWidget(self.project_progress_bar)
        
        layout.addWidget(info_group)
        
        return panel
    
    def create_timer_panel(self) -> QWidget:
        """Crée le panneau du timer Pomodoro"""
        panel = QGroupBox("Timer Pomodoro")
        layout = QVBoxLayout(panel)
        
        # Affichage du timer
        timer_layout = QVBoxLayout()
        
        self.session_type_label = QLabel("Prêt à commencer")
        self.session_type_label.setAlignment(Qt.AlignCenter)
        self.session_type_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        self.time_display = QLabel("25:00")
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setFont(QFont("Arial", 48, QFont.Bold))
        self.time_display.setStyleSheet("color: #e74c3c; background-color: #f8f9fa; border: 2px solid #dee2e6; border-radius: 10px; padding: 20px;")
        
        timer_layout.addWidget(self.session_type_label)
        timer_layout.addWidget(self.time_display)
        
        layout.addLayout(timer_layout)
        
        # Barre de progression
        self.timer_progress = QProgressBar()
        self.timer_progress.setMinimum(0)
        self.timer_progress.setMaximum(100)
        self.timer_progress.setValue(0)
        layout.addWidget(self.timer_progress)
        
        # Barre de progression quotidienne
        daily_progress_group = QGroupBox("Progression Quotidienne")
        daily_progress_layout = QVBoxLayout(daily_progress_group)
        
        self.daily_pomodoro_label = QLabel("Pomodoros aujourd'hui : 0 / 8")
        self.daily_pomodoro_label.setAlignment(Qt.AlignCenter)
        self.daily_pomodoro_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.daily_pomodoro_progress_bar = QProgressBar()
        self.daily_pomodoro_progress_bar.setMinimum(0)
        self.daily_pomodoro_progress_bar.setMaximum(8) # Valeur par défaut, sera mise à jour
        self.daily_pomodoro_progress_bar.setValue(0)
        self.daily_pomodoro_progress_bar.setTextVisible(True)
        
        daily_progress_layout.addWidget(self.daily_pomodoro_label)
        daily_progress_layout.addWidget(self.daily_pomodoro_progress_bar)
        
        layout.addWidget(daily_progress_group)
        
        # Boutons de contrôle
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Démarrer")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Arrêter")
        self.skip_btn = QPushButton("Passer")
        
        self.start_btn.setMinimumHeight(40)
        self.pause_btn.setMinimumHeight(40)
        self.stop_btn.setMinimumHeight(40)
        self.skip_btn.setMinimumHeight(40)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.pause_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.skip_btn)
        
        layout.addLayout(controls_layout)
        
        # Paramètres rapides
        settings_group = QGroupBox("Paramètres rapides")
        settings_layout = QGridLayout(settings_group)
        
        settings_layout.addWidget(QLabel("Travail (min):"), 0, 0)
        self.work_duration_spin = QSpinBox()
        self.work_duration_spin.setRange(1, 120)
        self.work_duration_spin.setValue(25)
        settings_layout.addWidget(self.work_duration_spin, 0, 1)
        
        settings_layout.addWidget(QLabel("Pause courte (min):"), 0, 2)
        self.short_break_spin = QSpinBox()
        self.short_break_spin.setRange(1, 60)
        self.short_break_spin.setValue(5)
        settings_layout.addWidget(self.short_break_spin, 0, 3)
        
        settings_layout.addWidget(QLabel("Pause longue (min):"), 1, 0)
        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 120)
        self.long_break_spin.setValue(15)
        settings_layout.addWidget(self.long_break_spin, 1, 1)
        
        self.settings_btn = QPushButton("Paramètres avancés")
        settings_layout.addWidget(self.settings_btn, 1, 2, 1, 2)
        
        layout.addWidget(settings_group)
        
        # État initial des boutons
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.skip_btn.setEnabled(False)
        
        return panel
    
    def setup_connections(self):
        """Configure les connexions des signaux et slots"""
        # Boutons de projets
        self.add_project_btn.clicked.connect(self.add_project)
        self.edit_project_btn.clicked.connect(self.edit_project)
        self.delete_project_btn.clicked.connect(self.delete_project)
        self.stats_btn.clicked.connect(self.show_statistics)
        
        # Liste des projets
        self.projects_list.currentItemChanged.connect(self.on_project_selected)
        
        # Boutons de contrôle du timer
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.skip_btn.clicked.connect(self.skip_session)
        
        # Paramètres
        self.settings_btn.clicked.connect(self.show_settings)
        
        # Signaux personnalisés
        self.timer_updated.connect(self.on_timer_updated)
        self.session_completed.connect(self.on_session_completed)
    
    def apply_styles(self):
        """Applique les styles CSS à l'interface"""
        self.setStyleSheet("""
            QMainWindow {
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
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
            }
            
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 4px;
            }
        """)
    
    def load_projects(self):
        """Charge les projets depuis la base de données et les affiche"""
        self.projects_list.clear()
        projects = self.project_controller.get_all_projects()
        for project in projects:
            item = QListWidgetItem(project.name)
            item.setData(Qt.UserRole, project.id) # Stocker l'ID du projet
            self.projects_list.addItem(item)
            
        if projects:
            self.projects_list.setCurrentRow(0) # Sélectionner le premier projet par défaut
    
    def load_app_settings(self):
        """Charge les paramètres de l'application et met à jour les spinbox"""
        settings = self.settings_controller.get_settings()
        self.work_duration_spin.setValue(settings.work_duration)
        self.short_break_spin.setValue(settings.short_break_duration)
        self.long_break_spin.setValue(settings.long_break_duration)
        self.daily_pomodoro_progress_bar.setMaximum(settings.daily_pomodoro_goal)
    
    def on_project_selected(self, current, previous):
        """Gère la sélection d'un projet"""
        if current is None:
            self.current_project_id = None
            self.project_name_label.setText("Aucun projet sélectionné")
            self.project_description_label.setText("")
            self.project_progress_label.setText("")
            self.project_progress_bar.setValue(0)
            self.start_btn.setEnabled(False)
            return
        
        project_id = current.data(Qt.UserRole)
        self.current_project_id = project_id
        
        project = self.project_controller.get_project_by_id(project_id)
        if project:
            self.project_name_label.setText(project.name)
            self.project_description_label.setText(project.description or "Aucune description")
            
            progress = project.get_progress_percentage()
            self.project_progress_label.setText(f"Progression: {project.completed_pomodoros}/{project.target_pomodoros} Pomodoros ({progress:.1f}%)")
            self.project_progress_bar.setValue(int(progress))
            
            self.start_btn.setEnabled(not self.is_running)
    
    def add_project(self):
        """Ouvre le dialogue d'ajout de projet"""
        dialog = ProjectDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name, description, target = dialog.get_project_data()
            try:
                project = self.project_controller.create_project(name, description, target)
                if project:
                    self.load_projects()
                    QMessageBox.information(self, "Succès", "Projet créé avec succès!")
                else:
                    QMessageBox.warning(self, "Erreur", "Impossible de créer le projet.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))
    
    def edit_project(self):
        """Ouvre le dialogue de modification de projet"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un projet à modifier.")
            return
        
        project = self.project_controller.get_project_by_id(self.current_project_id)
        if not project:
            QMessageBox.warning(self, "Erreur", "Projet introuvable.")
            return
        
        dialog = ProjectDialog(self, project)
        if dialog.exec() == QDialog.Accepted:
            name, description, target = dialog.get_project_data()
            try:
                project.name = name
                project.description = description
                project.target_pomodoros = target
                
                if self.project_controller.update_project(project):
                    self.load_projects()
                    self.on_project_selected(self.projects_list.currentItem(), None)
                    QMessageBox.information(self, "Succès", "Projet modifié avec succès!")
                else:
                    QMessageBox.warning(self, "Erreur", "Impossible de modifier le projet.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))
    
    def delete_project(self):
        """Supprime le projet sélectionné"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un projet à supprimer.")
            return
        
        project = self.project_controller.get_project_by_id(self.current_project_id)
        if not project:
            QMessageBox.warning(self, "Erreur", "Projet introuvable.")
            return
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le projet '{project.name}' ?\n"
            "Cette action supprimera également toutes les sessions associées.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.project_controller.delete_project(self.current_project_id):
                self.load_projects()
                QMessageBox.information(self, "Succès", "Projet supprimé avec succès!")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer le projet.")
    
    def show_statistics(self):
        """Affiche les statistiques du projet sélectionné"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un projet pour voir les statistiques.")
            return
        
        dialog = StatisticsDialog(self, self.current_project_id, self.project_controller)
        dialog.exec()
    
    def start_timer(self):
        """Démarre le timer Pomodoro"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un projet avant de démarrer.")
            return
        
        try:
            # Démarrer une session de travail
            session = self.pomodoro_controller.start_work_session(self.current_project_id)
            if session:
                self.time_left = session.get_duration_seconds()
                self.is_running = True
                self.timer.start(1000)  # Mise à jour chaque seconde
                
                self.session_type_label.setText("Session de travail")
                self.update_timer_display()
                self.update_button_states()
                
        except (RuntimeError, ValueError) as e:
            QMessageBox.warning(self, "Erreur", str(e))
    
    def pause_timer(self):
        """Met en pause ou reprend le timer"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.pause_btn.setText("Reprendre")
        else:
            self.timer.start(1000)
            self.is_running = True
            self.pause_btn.setText("Pause")
        
        self.update_button_states()
    
    def stop_timer(self):
        """Arrête le timer et annule la session"""
        self.timer.stop()
        self.is_running = False
        
        if self.pomodoro_controller.get_current_session():
            self.pomodoro_controller.cancel_current_session()
        
        self.reset_timer_display()
        self.update_button_states()
    
    def skip_session(self):
        """Passe à la session suivante"""
        if self.pomodoro_controller.get_current_session():
            self.pomodoro_controller.complete_current_session()
            self.load_projects()  # Recharger pour mettre à jour les compteurs
        
        self.start_next_session()
    
    def update_timer(self):
        """Met à jour le timer (appelé chaque seconde)"""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_updated.emit(self.time_left)
        else:
            # Session terminée
            self.timer.stop()
            self.is_running = False
            self.session_completed.emit()
    
    def update_timer_display(self):
        """Met à jour l'affichage du timer"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.time_display.setText(f"{minutes:02d}:{seconds:02d}")
        
        # Mettre à jour la barre de progression
        current_session = self.pomodoro_controller.get_current_session()
        if current_session:
            total_seconds = current_session.get_duration_seconds()
            progress = ((total_seconds - self.time_left) / total_seconds) * 100
            self.timer_progress.setValue(int(progress))
    
    def reset_timer_display(self):
        """Remet l'affichage du timer à zéro"""
        settings = self.settings_controller.get_settings()
        self.time_left = settings.work_duration * 60
        self.update_timer_display()
        self.timer_progress.setValue(0)
        self.session_type_label.setText("Prêt à commencer")
        self.pause_btn.setText("Pause")
    
    def update_button_states(self):
        """Met à jour l'état des boutons selon l'état du timer"""
        self.start_btn.setEnabled(not self.is_running and self.current_project_id is not None)
        self.pause_btn.setEnabled(self.pomodoro_controller.get_current_session() is not None)
        self.stop_btn.setEnabled(self.pomodoro_controller.get_current_session() is not None)
        self.skip_btn.setEnabled(self.pomodoro_controller.get_current_session() is not None)
    
    def on_timer_updated(self, time_left):
        """Gère la mise à jour du timer"""
        # Changer la couleur selon le temps restant
        if time_left <= 60:  # Dernière minute
            self.time_display.setStyleSheet("color: #dc3545; background-color: #f8f9fa; border: 2px solid #dc3545; border-radius: 10px; padding: 20px;")
        elif time_left <= 300:  # 5 dernières minutes
            self.time_display.setStyleSheet("color: #fd7e14; background-color: #f8f9fa; border: 2px solid #fd7e14; border-radius: 10px; padding: 20px;")
        else:
            self.time_display.setStyleSheet("color: #28a745; background-color: #f8f9fa; border: 2px solid #28a745; border-radius: 10px; padding: 20px;")
    
    def on_session_completed(self):
        """Gère la fin d'une session Pomodoro (travail ou pause)"""
        print("on_session_completed: Session terminée signal received.")
        current_session_data = self.pomodoro_controller.get_current_session()
        session_type = current_session_data.session_type if current_session_data else None

        print(f"on_session_completed: Current session type: {session_type}")
        if self.pomodoro_controller.complete_current_session():
            print("on_session_completed: Current session successfully completed in controller.")
            if session_type == 'work':
                self.update_daily_progress_display()

            settings = self.settings_controller.get_settings()
            if settings.notifications_enabled:
                if session_type == 'work':
                    self.show_notification("Pomodoro terminé!", "Temps de faire une pause!")
                else:
                    self.show_notification("Pause terminée!", "Prêt pour un nouveau Pomodoro!")

            self.load_projects()
            print("on_session_completed: Starting next session.")
            self.start_next_session(last_completed_session_type=session_type)
        else:
            print("on_session_completed: Failed to complete current session in controller.")
            QMessageBox.warning(self, "Erreur", "Impossible de terminer la session actuelle.")

    def start_next_session(self, last_completed_session_type: Optional[str] = None):
        """Démarre la session suivante automatiquement"""
        print("start_next_session: Determining next session type.")
        if not self.current_project_id:
            print("start_next_session: No project selected.")
            return

        # Passer le type de la session précédente au contrôleur
        next_type = self.pomodoro_controller.get_next_session_type(self.current_project_id, last_completed_session_type)
        print(f"start_next_session: Next session type: {next_type}")

        try:
            if next_type == 'work':
                session = self.pomodoro_controller.start_work_session(self.current_project_id)
            else:
                is_long = next_type == 'long_break'
                session = self.pomodoro_controller.start_break_session(self.current_project_id, is_long)

            if session:
                self.time_left = session.get_duration_seconds()
                self.is_running = True
                self.timer.start(1000)

                session_names = {
                    'work': 'Session de travail',
                    'short_break': 'Pause courte',
                    'long_break': 'Pause longue'
                }
                self.session_type_label.setText(session_names.get(next_type, 'Session'))
                self.update_timer_display()
                self.update_button_states()
                print("start_next_session: Session started successfully.")

        except (RuntimeError, ValueError) as e:
            print(f"start_next_session: Error starting session: {str(e)}")
            QMessageBox.warning(self, "Erreur", str(e))
    
    def show_notification(self, title: str, message: str):
        """Affiche une notification système"""
        print(f"show_notification: Tentative d'affichage de la notification - Titre: '{title}', Message: '{message}'")
        try:
            plyer.notification.notify(
                title=title,
                message=message,
                app_name="Pomodoro Timer",
                timeout=5
            )
            print("show_notification: Appel de Plyer réussi.")
        except Exception as e:
            print(f"show_notification: Erreur lors de l'affichage de la notification via plyer: {e}. (Pas de QMessageBox affichée pour éviter de bloquer l'UI)")
            # Ne rien faire en cas d'échec pour éviter de bloquer l'interface utilisateur
    
    def show_settings(self):
        """Ouvre la fenêtre des paramètres"""
        settings_dialog = SettingsDialog(self, self.settings_controller)
        if settings_dialog.exec() == QDialog.Accepted:
            self.load_app_settings()
            # Mettre à jour les paramètres rapides après la modification
            self.work_duration_spin.setValue(self.settings_controller.get_settings().work_duration)
            self.short_break_spin.setValue(self.settings_controller.get_settings().short_break_duration)
            self.long_break_spin.setValue(self.settings_controller.get_settings().long_break_duration)
            # Mettre à jour la barre de progression quotidienne si l'objectif a changé
            self.update_daily_progress_display()
    
    def update_daily_progress_display(self):
        """Met à jour la barre de progression des Pomodoros quotidiens"""
        progress_data = self.pomodoro_controller.get_daily_pomodoro_progress()
        completed = progress_data["completed_today"]
        goal = progress_data["goal"]
        
        self.daily_pomodoro_label.setText(f"Pomodoros aujourd'hui : {completed} / {goal}")
        self.daily_pomodoro_progress_bar.setMaximum(goal)
        self.daily_pomodoro_progress_bar.setValue(completed)
        
        # Mettre à jour le style de la barre si l'objectif est atteint
        if completed >= goal:
            self.daily_pomodoro_progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #28a745; }") # Vert
        else:
            self.daily_pomodoro_progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #007bff; }") # Bleu par défaut
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre"""
        # Déconnecter la base de données
        self.pomodoro_controller.db_manager.disconnect()
        event.accept()