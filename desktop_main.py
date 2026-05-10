import sys
import os

# Add src to python path so we can use absolute imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # Hide the pygame community message (just in case controller is used)
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
