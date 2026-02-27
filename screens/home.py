from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- TOP BAR WITH SMALL X BUTTON ---
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(10, 10, 0, 0)

        exit_btn = QPushButton("X")
        exit_btn.setFixedSize(26, 26)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 13px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #b52b27;
            }
        """)
        exit_btn.clicked.connect(self.open_admin_screen)

        top_bar.addWidget(exit_btn, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)
        # --- END TOP BAR ---

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

        center_layout.addStretch()
        center_layout.addWidget(card, alignment=Qt.AlignCenter)
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

        main_layout.addWidget(center_container)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.user_type)

    def open_admin_screen(self):
        # Navigate directly to admin password page
        self.main.stack.setCurrentWidget(self.main.admin_password)