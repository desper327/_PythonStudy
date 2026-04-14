"""
MVVM Demo - View Layer
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QLabel,
    QMessageBox, QListWidgetItem, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSlot
from viewmodels import UserViewModel


class UserListView(QMainWindow):
    """Main View - displays UI and binds to ViewModel"""
    
    def __init__(self, viewmodel: UserViewModel):
        super().__init__()
        self._viewmodel = viewmodel
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("MVVM Demo - User Management")
        self.setGeometry(100, 100, 600, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left side - User list
        left_layout = QVBoxLayout()
        
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        left_layout.addWidget(QLabel("Users:"))
        left_layout.addWidget(self.user_list)
        
        # Right side - User form
        right_layout = QVBoxLayout()
        
        # Form
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.age_edit = QLineEdit()
        self.email_edit = QLineEdit()
        
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Age:", self.age_edit)
        form_layout.addRow("Email:", self.email_edit)
        
        right_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add User")
        self.update_button = QPushButton("Update User")
        self.remove_button = QPushButton("Remove User")
        self.clear_button = QPushButton("Clear Form")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.clear_button)
        
        right_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("QLabel { color: blue; }")
        right_layout.addWidget(self.status_label)
        
        right_layout.addStretch()
        
        # Add layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)
    
    def setup_bindings(self):
        """Setup bindings between View and ViewModel"""
        # Connect button clicks to ViewModel commands
        self.add_button.clicked.connect(self._viewmodel.addUser)
        self.update_button.clicked.connect(self._viewmodel.updateUser)
        self.remove_button.clicked.connect(self._viewmodel.removeUser)
        self.clear_button.clicked.connect(self._viewmodel.clearForm)
        
        # Connect ViewModel property changes to UI updates
        self._viewmodel.nameChanged.connect(self._update_name_edit)
        self._viewmodel.ageChanged.connect(self._update_age_edit)
        self._viewmodel.emailChanged.connect(self._update_email_edit)
        self._viewmodel.usersChanged.connect(self._update_user_list)
        self._viewmodel.selectedUserIdChanged.connect(self._update_selection)
        self._viewmodel.statusMessageChanged.connect(self._update_status)
        
        # Connect UI changes to ViewModel properties
        self.name_edit.textChanged.connect(self._on_name_changed)
        self.age_edit.textChanged.connect(self._on_age_changed)
        self.email_edit.textChanged.connect(self._on_email_changed)
        
        # Initial load
        self._update_user_list()
    
    # UI event handlers
    @pyqtSlot()
    def on_user_selected(self):
        """Handle user selection in list"""
        current_item = self.user_list.currentItem()
        if current_item:
            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            self._viewmodel.selectedUserId = user_id
    
    @pyqtSlot(str)
    def _on_name_changed(self, text: str):
        """Handle name edit text change"""
        self._viewmodel.name = text
    
    @pyqtSlot(str)
    def _on_age_changed(self, text: str):
        """Handle age edit text change"""
        try:
            age = int(text) if text else 0
            self._viewmodel.age = age
        except ValueError:
            pass  # Keep current value if invalid
    
    @pyqtSlot(str)
    def _on_email_changed(self, text: str):
        """Handle email edit text change"""
        self._viewmodel.email = text
    
    # ViewModel property change handlers
    @pyqtSlot()
    def _update_name_edit(self):
        """Update name edit from ViewModel"""
        if self.name_edit.text() != self._viewmodel.name:
            self.name_edit.setText(self._viewmodel.name)
    
    @pyqtSlot()
    def _update_age_edit(self):
        """Update age edit from ViewModel"""
        age_text = str(self._viewmodel.age) if self._viewmodel.age > 0 else ""
        if self.age_edit.text() != age_text:
            self.age_edit.setText(age_text)
    
    @pyqtSlot()
    def _update_email_edit(self):
        """Update email edit from ViewModel"""
        if self.email_edit.text() != self._viewmodel.email:
            self.email_edit.setText(self._viewmodel.email)
    
    @pyqtSlot()
    def _update_user_list(self):
        """Update user list from ViewModel"""
        self.user_list.clear()
        
        for user_data in self._viewmodel.users:
            item = QListWidgetItem(f"{user_data['name']} ({user_data['age']})")
            item.setData(Qt.ItemDataRole.UserRole, user_data['id'])
            self.user_list.addItem(item)
    
    @pyqtSlot()
    def _update_selection(self):
        """Update list selection from ViewModel"""
        selected_id = self._viewmodel.selectedUserId
        
        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            user_id = item.data(Qt.ItemDataRole.UserRole)
            
            if user_id == selected_id:
                self.user_list.setCurrentItem(item)
                break
        else:
            self.user_list.clearSelection()
    
    @pyqtSlot()
    def _update_status(self):
        """Update status label from ViewModel"""
        self.status_label.setText(self._viewmodel.statusMessage)
