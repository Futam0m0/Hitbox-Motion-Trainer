import sys
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication, QMessageBox
from gui.views.main_menu_view import MainMenuView
from gui.views.analytics_view import AnalyticsView
from gui.views.training_view import TrainingView
from db import create_session
from services.session_service import create_session_summary

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hitbox Motion Trainer")
        self.setMinimumSize(800, 600)
        
        self.session_id = None
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.init_views()
        self.show_main_menu()

    def init_views(self):
        # Main Menu
        self.menu_view = MainMenuView()
        self.menu_view.start_training_requested.connect(self.start_training_session)
        self.menu_view.view_analytics_requested.connect(self.show_analytics)
        self.menu_view.exit_requested.connect(self.close)
        self.central_widget.addWidget(self.menu_view)

        # Analytics View
        self.analytics_view = AnalyticsView()
        self.analytics_view.back_requested.connect(self.show_main_menu)
        self.central_widget.addWidget(self.analytics_view)

    def show_main_menu(self):
        self.central_widget.setCurrentWidget(self.menu_view)

    def show_analytics(self):
        # Refresh analytics data before showing
        self.analytics_view.load_motion_stats()
        self.central_widget.setCurrentWidget(self.analytics_view)

    def start_training_session(self):
        try:
            self.session_id = create_session(player_id=1)
            
            # Create a fresh training view for the session
            self.training_view = TrainingView(self.session_id)
            self.training_view.back_requested.connect(self.end_training_session)
            
            # Add to stack and switch
            idx = self.central_widget.addWidget(self.training_view)
            self.central_widget.setCurrentIndex(idx)
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not start session: {str(e)}")

    def end_training_session(self):
        if self.session_id:
            create_session_summary(self.session_id)
        
        # Remove training view from stack and return to menu
        widget = self.central_widget.currentWidget()
        self.central_widget.setCurrentWidget(self.menu_view)
        self.central_widget.removeWidget(widget)
        widget.deleteLater()
