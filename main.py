import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit
from PySide6.QtCore import Qt

import services.keyboard as keyboard

from screens.home import HomeScreen
from screens.info import InfoScreen
from screens.upload import UploadScreen
from screens.result import ResultScreen
from screens.user_type import UserTypeScreen
from screens.registered_user import RegisteredUserScreen

EXIT_PASSWORD = "admin123"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PeeSense")

        # DO NOT use showFullScreen on X11
        # Allow stacking with external keyboard
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showMaximized()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize screens
        self.home = HomeScreen(self)
        self.user_type = UserTypeScreen(self)
        self.info = InfoScreen(self)
        self.upload = UploadScreen(self)
        self.result = ResultScreen(self)
        self.registered = RegisteredUserScreen(self)

        # Add to stack
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.user_type)
        self.stack.addWidget(self.info)
        self.stack.addWidget(self.upload)
        self.stack.addWidget(self.result)
        self.stack.addWidget(self.registered)

        self.stack.setCurrentWidget(self.home)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setFocus()
        keyboard.hide_keyboard()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Focus-based keyboard control
    def _on_focus_changed(old, new):
        if isinstance(new, QLineEdit):
            keyboard.show_keyboard()
        else:
            keyboard.hide_keyboard()

    app.focusChanged.connect(_on_focus_changed)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())