"""
Dialogue pour configurer les paramètres de l'application
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QSpinBox, QCheckBox, QPushButton, QGroupBox,
                              QLabel, QMessageBox)
from PySide6.QtCore import Qt
from controllers.settings_controller import SettingsController

class SettingsDialog(QDialog):
    """Dialogue pour configurer les paramètres de l'application"""
    
    def __init__(self, parent=None, settings_controller: SettingsController = None):
        super().__init__(parent)
        self.settings_controller = settings_controller
        
        self.setup_ui()
        self.setup_connections()
        self.load_current_settings()
        
        # Configuration de la fenêtre
        self.setWindowTitle("Paramètres de l'application")
        self.setModal(True)
        self.resize(400, 350)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Groupe des durées
        durations_group = QGroupBox("Durées des sessions")
        durations_layout = QFormLayout(durations_group)
        
        # Durée de travail
        self.work_duration_spin = QSpinBox()
        self.work_duration_spin.setRange(1, 120)
        self.work_duration_spin.setSuffix(" minutes")
        self.work_duration_spin.setValue(25)
        durations_layout.addRow("Durée de travail:", self.work_duration_spin)
        
        # Durée pause courte
        self.short_break_spin = QSpinBox()
        self.short_break_spin.setRange(1, 60)
        self.short_break_spin.setSuffix(" minutes")
        self.short_break_spin.setValue(5)
        durations_layout.addRow("Pause courte:", self.short_break_spin)
        
        # Durée pause longue
        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 120)
        self.long_break_spin.setSuffix(" minutes")
        self.long_break_spin.setValue(15)
        durations_layout.addRow("Pause longue:", self.long_break_spin)
        
        # Intervalle pause longue
        self.long_break_interval_spin = QSpinBox()
        self.long_break_interval_spin.setRange(1, 10)
        self.long_break_interval_spin.setSuffix(" Pomodoros")
        self.long_break_interval_spin.setValue(4)
        durations_layout.addRow("Pause longue après:", self.long_break_interval_spin)
        
        layout.addWidget(durations_group)
        
        # Groupe des notifications
        notifications_group = QGroupBox("Notifications")
        notifications_layout = QVBoxLayout(notifications_group)
        
        self.notifications_checkbox = QCheckBox("Activer les notifications")
        self.notifications_checkbox.setChecked(True)
        notifications_layout.addWidget(self.notifications_checkbox)
        
        notification_note = QLabel("Les notifications vous alertent à la fin de chaque session.")
        notification_note.setStyleSheet("color: #6c757d; font-style: italic;")
        notification_note.setWordWrap(True)
        notifications_layout.addWidget(notification_note)
        
        layout.addWidget(notifications_group)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Valeurs par défaut")
        self.reset_button.setStyleSheet("background-color: #ffc107; color: #212529;")
        
        actions_layout.addWidget(self.reset_button)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
        # Boutons de validation
        buttons_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("Enregistrer")
        self.cancel_button = QPushButton("Annuler")
        
        self.ok_button.setDefault(True)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.ok_button)
        
        layout.addLayout(buttons_layout)
        
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
            
            QSpinBox {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
                min-width: 100px;
            }
            
            QSpinBox:focus {
                border-color: #007bff;
            }
            
            QCheckBox {
                font-weight: normal;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 2px solid #dee2e6;
                border-radius: 3px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                border: 2px solid #007bff;
                border-radius: 3px;
                background-color: #007bff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMC42IDEuNEw0LjIgNy44TDEuNCA1IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton[text="Annuler"] {
                background-color: #6c757d;
            }
            
            QPushButton[text="Annuler"]:hover {
                background-color: #545b62;
            }
        """)
    
    def setup_connections(self):
        """Configure les connexions des signaux"""
        self.ok_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.reset_button.clicked.connect(self.reset_to_defaults)
    
    def load_current_settings(self):
        """Charge les paramètres actuels"""
        if self.settings_controller:
            settings = self.settings_controller.get_settings()
            
            self.work_duration_spin.setValue(settings.work_duration)
            self.short_break_spin.setValue(settings.short_break_duration)
            self.long_break_spin.setValue(settings.long_break_duration)
            self.long_break_interval_spin.setValue(settings.long_break_interval)
            self.notifications_checkbox.setChecked(settings.notifications_enabled)
    
    def save_settings(self):
        """Enregistre les paramètres"""
        try:
            success = self.settings_controller.update_settings(
                work_duration=self.work_duration_spin.value(),
                short_break_duration=self.short_break_spin.value(),
                long_break_duration=self.long_break_spin.value(),
                long_break_interval=self.long_break_interval_spin.value(),
                notifications_enabled=self.notifications_checkbox.isChecked()
            )
            
            if success:
                QMessageBox.information(self, "Succès", "Paramètres enregistrés avec succès!")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'enregistrer les paramètres.")
                
        except ValueError as e:
            QMessageBox.warning(self, "Erreur de validation", str(e))
    
    def reset_to_defaults(self):
        """Remet les paramètres aux valeurs par défaut"""
        reply = QMessageBox.question(
            self, "Confirmation",
            "Êtes-vous sûr de vouloir remettre tous les paramètres aux valeurs par défaut?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.work_duration_spin.setValue(25)
            self.short_break_spin.setValue(5)
            self.long_break_spin.setValue(15)
            self.long_break_interval_spin.setValue(4)
            self.notifications_checkbox.setChecked(True)