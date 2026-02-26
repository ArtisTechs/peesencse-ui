from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QHBoxLayout, QLineEdit, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

EXIT_PASSWORD = "admin123"


class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(280, 130)
        self.setWindowTitle("Exit Authorization")

        # Stronger top-most behavior
        self.setWindowFlags(
            Qt.Dialog |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter password")
        self.input.setEchoMode(QLineEdit.Password)

        confirm = QPushButton("Confirm")
        confirm.clicked.connect(self.check_password)

        layout.addWidget(self.input)
        layout.addWidget(confirm)

    def check_password(self):
        if self.input.text() == EXIT_PASSWORD:
            QApplication.quit()
        else:
            self.input.clear()


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

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Top bar
        top_bar = QHBoxLayout()
        exit_btn = QPushButton("✕")
        exit_btn.setFixedSize(36, 36)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 18px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        exit_btn.clicked.connect(self.open_password)

        top_bar.addWidget(exit_btn, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        # Card container (smaller for 7" screen)
        card = QFrame()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 25px;
            }
        """)

        card_layout = QVBoxLayout()
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

        card.setLayout(card_layout)

        # Footer (smaller text)
        footer = QLabel("© 2026 PeeSense – AI-Assisted Urinalysis System\nFor Academic & Research Use Only")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            background-color: #2d63c8;
            color: white;
            padding: 10px;
            font-size: 11px;
        """)

        main_layout.addLayout(top_bar)
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.user_type)

    def open_password(self):
        self.dialog = PasswordDialog()
        self.dialog.show()
        self.dialog.activateWindow()
        self.dialog.raise_()