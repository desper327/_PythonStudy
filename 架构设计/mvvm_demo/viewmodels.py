"""
MVVM Demo - ViewModel Layer
"""
from typing import Optional, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty
from models import User, UserModel


class UserViewModel(QObject):
    """ViewModel - exposes model data as observable properties for the View"""
    
    # Signals for property changes
    nameChanged = pyqtSignal()
    ageChanged = pyqtSignal()
    emailChanged = pyqtSignal()
    usersChanged = pyqtSignal()
    selectedUserIdChanged = pyqtSignal()
    statusMessageChanged = pyqtSignal()
    
    def __init__(self, model: UserModel):
        super().__init__()
        self._model = model
        self._name = ""
        self._age = 0
        self._email = ""
        self._users: List[dict] = []
        self._selected_user_id: Optional[str] = None
        self._status_message = "Ready"
        
        # Connect to model signals
        model.user_added.connect(self._on_user_added)
        model.user_updated.connect(self._on_user_updated)
        model.user_removed.connect(self._on_user_removed)
        
        # Load initial data
        self._refresh_users()
    
    # Observable properties
    @pyqtProperty(str, notify=nameChanged)
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if self._name != value:
            self._name = value
            self.nameChanged.emit()
    
    @pyqtProperty(int, notify=ageChanged)
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int):
        if self._age != value:
            self._age = value
            self.ageChanged.emit()
    
    @pyqtProperty(str, notify=emailChanged)
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if self._email != value:
            self._email = value
            self.emailChanged.emit()
    
    @pyqtProperty("QVariantList", notify=usersChanged)
    def users(self) -> List[dict]:
        return self._users
    
    @pyqtProperty(str, notify=selectedUserIdChanged)
    def selectedUserId(self) -> str:
        return self._selected_user_id or ""
    
    @selectedUserId.setter
    def selectedUserId(self, value: str):
        if self._selected_user_id != value:
            self._selected_user_id = value if value else None
            self.selectedUserIdChanged.emit()
            self._load_selected_user()
    
    @pyqtProperty(str, notify=statusMessageChanged)
    def statusMessage(self) -> str:
        return self._status_message
    
    # Commands (methods that View can call)
    def addUser(self):
        """Command to add a new user"""
        if not self.name.strip():
            self.statusMessage = "Name cannot be empty"
            return
        
        if self.age <= 0 or self.age > 120:
            self.statusMessage = "Please enter a valid age"
            return
        
        user_id = self._model.add_user(self.name, self.age, self.email)
        self.statusMessage = f"User added: {self.name}"
        self._clear_form()
    
    def updateUser(self):
        """Command to update selected user"""
        if not self._selected_user_id:
            self.statusMessage = "No user selected"
            return
        
        success = self._model.update_user(
            self._selected_user_id, self.name, self.age, self.email
        )
        
        if success:
            self.statusMessage = f"User updated: {self.name}"
        else:
            self.statusMessage = "Failed to update user"
    
    def removeUser(self):
        """Command to remove selected user"""
        if not self._selected_user_id:
            self.statusMessage = "No user selected"
            return
        
        success = self._model.remove_user(self._selected_user_id)
        
        if success:
            self.statusMessage = "User removed"
            self._clear_form()
        else:
            self.statusMessage = "Failed to remove user"
    
    def clearForm(self):
        """Command to clear the form"""
        self._clear_form()
        self.statusMessage = "Form cleared"
    
    # Private methods
    def _clear_form(self):
        """Clear input form"""
        self.name = ""
        self.age = 0
        self.email = ""
        self.selectedUserId = ""
    
    def _load_selected_user(self):
        """Load selected user data into form"""
        if not self._selected_user_id:
            return
        
        user = self._model.get_user(self._selected_user_id)
        if user:
            self.name = user.name
            self.age = user.age
            self.email = user.email
    
    def _refresh_users(self):
        """Refresh users list from model"""
        users_data = []
        for user_id, user in self._model.get_all_users().items():
            users_data.append({
                "id": user_id,
                "name": user.name,
                "age": user.age,
                "email": user.email
            })
        
        self._users = users_data
        self.usersChanged.emit()
    
    def _set_status_message(self, message: str):
        """Set status message"""
        self._status_message = message
        self.statusMessageChanged.emit()
    
    # Model signal handlers
    def _on_user_added(self, user: User):
        """Handle user added signal from model"""
        self._refresh_users()
        self._set_status_message(f"User added: {user.name}")
    
    def _on_user_updated(self, user: User):
        """Handle user updated signal from model"""
        self._refresh_users()
        self._set_status_message(f"User updated: {user.name}")
    
    def _on_user_removed(self, user_id: str):
        """Handle user removed signal from model"""
        self._refresh_users()
        self._set_status_message(f"User removed: {user_id}")
