from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QApplication, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

EXIT_PASSWORD = "admin123"


class AdminPasswordScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f7;
                color: #1a2b49;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(350)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 25px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)

        title = QLabel("Admin Authorization")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter admin password")
        self.input.setEchoMode(QLineEdit.Password)

        confirm_btn = QPushButton("Confirm")
        confirm_btn.setFixedHeight(40)
        confirm_btn.clicked.connect(self.check_password)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(35)
        back_btn.clicked.connect(self.go_back)

        card_layout.addWidget(title)
        card_layout.addWidget(self.input)
        card_layout.addWidget(confirm_btn)
        card_layout.addWidget(back_btn)

        main_layout.addWidget(card)

    def check_password(self):
        if self.input.text() == EXIT_PASSWORD:
            QApplication.quit()
        else:
            self.input.clear()

    def go_back(self):
        self.input.clear()
        self.main.stack.setCurrentWidget(self.main.home)


class HomeScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f7;
                color: #1a2b49;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with small X button
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(10, 10, 0, 0)

        exit_btn = QPushButton("X")
        exit_btn.setFixedSize(28, 28)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b52b27;
            }
        """)
        exit_btn.clicked.connect(self.open_admin_screen)

        top_bar.addWidget(exit_btn, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 25px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)

        title = QLabel("PeeSense")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("AI-Assisted Urinalysis System")
        subtitle.setStyleSheet("""
            color: #3b4a6b;
            font-size: 14px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)

        start_btn = QPushButton("Get Started")
        start_btn.setFixedHeight(45)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d63c8;
                color: white;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1e4ea8;
            }
        """)
        start_btn.clicked.connect(self.go_next)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(start_btn)

        center_layout.addStretch()
        center_layout.addWidget(card)
        center_layout.addStretch()

        footer = QLabel(
            "© 2026 PeeSense – AI-Assisted Urinalysis System\n"
            "For Academic & Research Use Only"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        footer.setStyleSheet("""
            background-color: #2d63c8;
            color: white;
            padding: 10px;
            font-size: 11px;
        """)

        main_layout.addLayout(top_bar)
        main_layout.addWidget(center_container)
        main_layout.addWidget(footer)

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.user_type)

    def open_admin_screen(self):
        self.main.stack.setCurrentWidget(self.main.admin_password)