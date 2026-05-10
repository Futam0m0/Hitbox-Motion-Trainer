from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class MainMenuView(QWidget):
    # Signals to communicate with the MainWindow controller
    start_training_requested = pyqtSignal()
    view_analytics_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Hitbox Motion Trainer")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_training = QPushButton("Start Training Session")
        self.btn_analytics = QPushButton("View Analytics Reports")
        self.btn_exit = QPushButton("Exit")

        # Basic styling
        button_style = "padding: 10px; font-size: 16px; min-width: 250px;"
        self.btn_training.setStyleSheet(button_style)
        self.btn_analytics.setStyleSheet(button_style)
        self.btn_exit.setStyleSheet(button_style)

        layout.addWidget(self.btn_training)
        layout.addWidget(self.btn_analytics)
        layout.addWidget(self.btn_exit)

        # Connect signals
        self.btn_training.clicked.connect(self.start_training_requested.emit)
        self.btn_analytics.clicked.connect(self.view_analytics_requested.emit)
        self.btn_exit.clicked.connect(self.exit_requested.emit)

        self.setLayout(layout)
