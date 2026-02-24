import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

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

        # Start at home
        self.stack.setCurrentWidget(self.home)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())