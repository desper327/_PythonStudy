"""
MVVM Demo - Main Application Entry Point
Demonstrates complete MVVM architecture with PyQt6
"""
import sys
from PyQt6.QtWidgets import QApplication
from models import UserModel
from viewmodels import UserViewModel
from views import UserListView


def main():
    """Main function to run the MVVM demo"""
    app = QApplication(sys.argv)
    
    print("=" * 60)
    print("MVVM Architecture Demo - User Management")
    print("=" * 60)
    print("Architecture Components:")
    print("1. Model (UserModel): Business logic and data management")
    print("2. ViewModel (UserViewModel): Observable properties and commands")
    print("3. View (UserListView): UI presentation and data binding")
    print("=" * 60)
    print("Data Flow:")
    print("View -> ViewModel -> Model -> ViewModel -> View")
    print("UI updates automatically through property binding")
    print("=" * 60)
    
    try:
        # Create Model layer
        model = UserModel()
        
        # Create ViewModel layer with Model
        viewmodel = UserViewModel(model)
        
        # Create View layer with ViewModel
        view = UserListView(viewmodel)
        
        # Add some sample data
        model.add_user("Alice", 25, "alice@example.com")
        model.add_user("Bob", 30, "bob@example.com")
        model.add_user("Charlie", 35, "charlie@example.com")
        
        # Show the main window
        view.show()
        
        print("MVVM Demo started successfully!")
        print("Try the following operations:")
        print("- Select a user from the list to edit")
        print("- Add a new user using the form")
        print("- Update an existing user")
        print("- Remove a user")
        print("- Notice how UI updates automatically!")
        
        # Start the event loop
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Application startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
