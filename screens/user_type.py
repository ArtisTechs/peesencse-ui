from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class UserTypeScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background-color: #eef2f7;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 0)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(650)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(60, 50, 60, 50)
        card_layout.setSpacing(25)

        title = QLabel("Select User Type")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- BUTTON STYLE ----------------
        button_style_primary = """
            QPushButton {
                background-color: #2d63c8;
                color: white;
                font-size: 18px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #1e4ea8;
            }
        """

        button_style_secondary = """
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 18px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #7f8a96;
            }
        """

        registered_btn = QPushButton("Already Registered")
        registered_btn.setFixedHeight(60)
        registered_btn.setStyleSheet(button_style_primary)
        registered_btn.clicked.connect(self.go_registered)

        new_btn = QPushButton("New User")
        new_btn.setFixedHeight(60)
        new_btn.setStyleSheet(button_style_primary)
        new_btn.clicked.connect(self.go_new)

        # ---------------- BACK BUTTON ----------------
        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(55)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #7f8a96;
            }
        """)
        back_btn.clicked.connect(self.go_back)

        card_layout.addWidget(title)
        card_layout.addWidget(registered_btn)
        card_layout.addWidget(new_btn)
        card_layout.addWidget(back_btn)

        # Center card
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(card, alignment=Qt.AlignCenter)
        center_layout.addStretch()

        # ---------------- FOOTER ----------------
        footer = QLabel(
            "© 2026 PeeSense – AI-Assisted Urinalysis System\n"
            "For Academic & Research Use Only"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(70)
        footer.setStyleSheet("""
            background-color: #2d63c8;
            color: white;
            font-size: 14px;
        """)

        main_layout.addLayout(center_layout)
        main_layout.addWidget(footer)

    def go_registered(self):
        self.main.registered.load_users()
        self.main.stack.setCurrentWidget(self.main.registered)

    def go_new(self):
        self.main.stack.setCurrentWidget(self.main.info)

    def go_back(self):
        self.main.stack.setCurrentWidget(self.main.home)