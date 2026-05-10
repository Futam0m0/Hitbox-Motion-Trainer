from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget)
from PyQt6.QtCore import pyqtSignal, Qt
import services.analytics_service as analytics

class AnalyticsView(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # Header with back button
        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back to Menu")
        self.btn_back.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(self.btn_back)
        
        title = QLabel("Training Analytics")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(header_layout)

        # Tabs for different reports (using buttons for simplicity to match CLI flow)
        report_nav = QHBoxLayout()
        self.btn_stats = QPushButton("Motion Stats")
        self.btn_sessions = QPushButton("Session History")
        self.btn_rankings = QPushButton("Rankings")
        self.btn_consistency = QPushButton("Consistency")
        
        report_nav.addWidget(self.btn_stats)
        report_nav.addWidget(self.btn_sessions)
        report_nav.addWidget(self.btn_rankings)
        report_nav.addWidget(self.btn_consistency)
        self.main_layout.addLayout(report_nav)

        # Table for displaying data
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_layout.addWidget(self.table)

        # Connect report buttons
        self.btn_stats.clicked.connect(self.load_motion_stats)
        self.btn_sessions.clicked.connect(self.load_session_stats)
        self.btn_rankings.clicked.connect(self.load_rankings)
        self.btn_consistency.clicked.connect(self.load_consistency)

        self.setLayout(self.main_layout)
        
        # Load initial report
        self.load_motion_stats()

    def _setup_table(self, headers):
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)

    def load_motion_stats(self):
        self._setup_table(["Motion", "Total", "Success", "Rate%", "Avg Time"])
        stats = analytics.get_motion_statistics()
        self.table.setRowCount(len(stats))
        for i, row in enumerate(stats):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row[3]}%"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{row[4] if row[4] else 0.0:.3f}s"))

    def load_session_stats(self):
        self._setup_table(["ID", "Start Time", "Attempts", "Rate%", "Avg Time"])
        sessions = analytics.get_session_statistics()
        self.table.setRowCount(len(sessions))
        for i, row in enumerate(sessions):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row[3]}%"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{row[4] if row[4] else 0.0:.3f}s"))

    def load_rankings(self):
        self._setup_table(["Motion", "Time", "Rank", "Avg", "Diff"])
        rankings = analytics.get_motion_rankings()
        self.table.setRowCount(min(len(rankings), 50))
        for i, row in enumerate(rankings[:50]):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(f"{row[1]:.3f}s"))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row[3]:.3f}s"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{row[4]:.3f}s"))

    def load_consistency(self):
        self._setup_table(["Motion", "Sess #", "Avg Time", "Improvement"])
        report = analytics.get_consistency_report()
        self.table.setRowCount(len(report))
        for i, row in enumerate(report):
            imp = row[3] if row[3] is not None else 0.0
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row[2]:.3f}s"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{imp:.3f}s"))
