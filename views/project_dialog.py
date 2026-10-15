"""
Dialogue pour créer/modifier un projet
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLineEdit, QTextEdit, QSpinBox, QPushButton,
                              QLabel, QMessageBox)
from PySide6.QtCore import Qt
from models.project import Project
from typing import Optional, Tuple

class ProjectDialog(QDialog):
    """Dialogue pour créer ou modifier un projet"""
    
    def __init__(self, parent=None, project: Optional[Project] = None):
        super().__init__(parent)
        self.project = project
        self.is_editing = project is not None
        
        self.setup_ui()
        self.setup_connections()
        
        if self.is_editing:
            self.load_project_data()
        
        # Configuration de la fenêtre
        title = "Modifier le projet" if self.is_editing else "Nouveau projet"
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(400, 300)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Formulaire
        form_layout = QFormLayout()
        
        # Nom du projet
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Entrez le nom du projet")
        form_layout.addRow("Nom du projet *:", self.name_edit)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Description du projet (optionnel)")
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_edit)
        
        # Nombre cible de Pomodoros
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 100)
        self.target_spin.setValue(8)
        self.target_spin.setSuffix(" Pomodoros")
        form_layout.addRow("Objectif:", self.target_spin)
        
        layout.addLayout(form_layout)
        
        # Note
        note_label = QLabel("* Champs obligatoires")
        note_label.setStyleSheet("color: #6c757d; font-style: italic;")
        layout.addWidget(note_label)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("Enregistrer" if self.is_editing else "Créer")
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
            
            QLineEdit, QTextEdit, QSpinBox {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border-color: #007bff;
                outline: none;
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
            
            QPushButton[text="Annuler"] {
                background-color: #6c757d;
            }
            
            QPushButton[text="Annuler"]:hover {
                background-color: #545b62;
            }
        """)
    
    def setup_connections(self):
        """Configure les connexions des signaux"""
        self.ok_button.clicked.connect(self.accept_dialog)
        self.cancel_button.clicked.connect(self.reject)
        
        # Validation en temps réel
        self.name_edit.textChanged.connect(self.validate_form)
    
    def load_project_data(self):
        """Charge les données du projet à modifier"""
        if self.project:
            self.name_edit.setText(self.project.name)
            self.description_edit.setPlainText(self.project.description or "")
            self.target_spin.setValue(self.project.target_pomodoros)
    
    def validate_form(self):
        """Valide le formulaire et active/désactive le bouton OK"""
        name = self.name_edit.text().strip()
        self.ok_button.setEnabled(len(name) > 0)
    
    def accept_dialog(self):
        """Valide et accepte le dialogue"""
        name = self.name_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        target = self.target_spin.value()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire.")
            self.name_edit.setFocus()
            return
        
        if len(name) > 255:
            QMessageBox.warning(self, "Erreur", "Le nom du projet ne peut pas dépasser 255 caractères.")
            self.name_edit.setFocus()
            return
        
        if len(description) > 1000:
            QMessageBox.warning(self, "Erreur", "La description ne peut pas dépasser 1000 caractères.")
            self.description_edit.setFocus()
            return
        
        self.accept()
    
    def get_project_data(self) -> Tuple[str, str, int]:
        """Retourne les données du projet saisies"""
        return (
            self.name_edit.text().strip(),
            self.description_edit.toPlainText().strip(),
            self.target_spin.value()
        )