import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QFrame)
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from core.buffer import InputBuffer
from core.constants import DIR_SYMBOLS
from input_backends.keyboard_backend import KeyboardBackend
from input_backends.controller_backend import ControllerBackend
from services.input_service import processInput
from services.motion_loader import get_all_motions, load_motion
from services.motion_service import get_motion_step_symbols

class TrainingView(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id
        self.backend = None
        self.buffer = InputBuffer(maxSize=100, frame_rate=60)
        self.motion_id = None
        self.target_symbols = ""
        
        # UI Refresh Timer (60Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Header with back button
        header = QHBoxLayout()
        self.btn_back = QPushButton("Stop Training")
        self.btn_back.clicked.connect(self.stop_training)
        header.addWidget(self.btn_back)
        
        self.lbl_device = QLabel("Device: None")
        header.addWidget(self.lbl_device, 1, Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(header)

        # Configuration Row
        config_layout = QHBoxLayout()
        
        self.combo_motion = QComboBox()
        self.populate_motions()
        self.combo_motion.currentIndexChanged.connect(self.on_motion_changed)
        config_layout.addWidget(QLabel("Motion:"))
        config_layout.addWidget(self.combo_motion, 1)

        self.combo_device = QComboBox()
        self.combo_device.addItems(["Keyboard", "Controller / Hitbox"])
        config_layout.addWidget(QLabel("Input:"))
        config_layout.addWidget(self.combo_device)
        
        self.btn_start = QPushButton("Start Polling")
        self.btn_start.clicked.connect(self.toggle_polling)
        config_layout.addWidget(self.btn_start)
        
        self.layout.addLayout(config_layout)

        # Visualization Area
        viz_frame = QFrame()
        viz_frame.setFrameShape(QFrame.Shape.StyledPanel)
        viz_frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px;")
        viz_layout = QVBoxLayout(viz_frame)

        self.lbl_target = QLabel("Target: --")
        self.lbl_target.setStyleSheet("color: #00ff00; font-size: 20px; font-family: monospace;")
        viz_layout.addWidget(self.lbl_target)

        self.lbl_current = QLabel("Current: 5")
        self.lbl_current.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        viz_layout.addWidget(self.lbl_current, 0, Qt.AlignmentFlag.AlignCenter)

        self.lbl_buffer = QLabel("Buffer: --")
        self.lbl_buffer.setStyleSheet("color: #aaaaaa; font-size: 18px; font-family: monospace;")
        viz_layout.addWidget(self.lbl_buffer)

        self.lbl_frames = QLabel("Frames: --")
        self.lbl_frames.setStyleSheet("color: #666666; font-size: 14px; font-family: monospace;")
        viz_layout.addWidget(self.lbl_frames)

        self.layout.addWidget(viz_frame, 1)

        # Status Label (Detection Feed)
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffff00;")
        self.layout.addWidget(self.lbl_status, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.on_motion_changed() # Initialize symbols

    def populate_motions(self):
        motions = get_all_motions()
        seen = set()
        for m_id, name in motions:
            if name not in seen:
                self.combo_motion.addItem(name, m_id)
                seen.add(name)

    def on_motion_changed(self):
        self.motion_id = self.combo_motion.currentData()
        steps = load_motion(self.motion_id)
        self.target_symbols = get_motion_step_symbols(steps)
        self.lbl_target.setText(f"Target:  {self.target_symbols}")

    def toggle_polling(self):
        if self.timer.isActive():
            self.stop_polling()
        else:
            self.start_polling()

    def start_polling(self):
        backend_type = self.combo_device.currentText().lower()
        if "keyboard" in backend_type:
            self.backend = KeyboardBackend()
        else:
            self.backend = ControllerBackend()
        
        self.backend.start()
        self.lbl_device.setText(f"Device: {getattr(self.backend, 'device_name', 'Active')}")
        self.btn_start.setText("Stop Polling")
        self.combo_device.setEnabled(False)
        self.combo_motion.setEnabled(False)
        self.timer.start(16) # ~60fps

    def stop_polling(self):
        self.timer.stop()
        if self.backend:
            self.backend.stop()
            self.backend = None
        self.btn_start.setText("Start Polling")
        self.lbl_device.setText("Device: None")
        self.combo_device.setEnabled(True)
        self.combo_motion.setEnabled(True)

    def stop_training(self):
        self.stop_polling()
        self.back_requested.emit()

    def update_loop(self):
        if not self.backend:
            return

        # 1. Hardware Poll
        state = self.backend.poll()
        current_direction = state.get_direction()
        
        # 2. Update Buffer
        self.buffer.update(current_direction)
        
        # 3. Process Detection
        status = processInput(self.buffer, self.session_id, self.motion_id)
        
        # 4. Update UI
        self.lbl_current.setText(f"Current: {DIR_SYMBOLS.get(current_direction, '5')}")
        
        # Update Status Message
        if status == "SUCCESS":
            self.lbl_status.setText("SUCCESS! ★★★")
            self.lbl_status.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")
            QTimer.singleShot(500, lambda: self.lbl_status.setText(""))
        elif status == "FAILED":
            self.lbl_status.setText("FAILED! ✗✗✗")
            self.lbl_status.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff0000;")
            QTimer.singleShot(500, lambda: self.lbl_status.setText(""))

        # Update Buffer Strings
        sequence = self.buffer.get_recent_with_timing(10)
        icons = [DIR_SYMBOLS.get(e["direction"], "?") for e in sequence]
        frames = [str(e["frames"]) for e in sequence]
        
        self.lbl_buffer.setText(f"Buffer:  {' '.join(icons)}")
        self.lbl_frames.setText(f"Frames:  {' '.join(frames)}")
