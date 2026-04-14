"""
MVVM Demo - Model Layer
"""
from typing import Optional
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class User:
    """User data model"""
    name: str
    age: int
    email: str


class UserModel(QObject):
    """User model - handles business logic and data"""
    
    # Signals for data changes
    user_added = pyqtSignal(User)
    user_updated = pyqtSignal(User)
    user_removed = pyqtSignal(str)  # user_id
    
    def __init__(self):
        super().__init__()
        self._users: dict[str, User] = {}
        self._next_id = 1
    
    def add_user(self, name: str, age: int, email: str) -> str:
        """Add a new user and return user_id"""
        user_id = f"user_{self._next_id}"
        user = User(name=name, age=age, email=email)
        self._users[user_id] = user
        self._next_id += 1
        
        self.user_added.emit(user)
        return user_id
    
    def update_user(self, user_id: str, name: Optional[str] = None, 
                   age: Optional[int] = None, email: Optional[str] = None) -> bool:
        """Update user data"""
        if user_id not in self._users:
            return False
        
        user = self._users[user_id]
        if name is not None:
            user.name = name
        if age is not None:
            user.age = age
        if email is not None:
            user.email = email
        
        self.user_updated.emit(user)
        return True
    
    def remove_user(self, user_id: str) -> bool:
        """Remove a user"""
        if user_id not in self._users:
            return False
        
        del self._users[user_id]
        self.user_removed.emit(user_id)
        return True
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self._users.get(user_id)
    
    def get_all_users(self) -> dict[str, User]:
        """Get all users"""
        return self._users.copy()
