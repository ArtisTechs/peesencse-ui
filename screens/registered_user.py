from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from services.api import get_users


class RegisteredUserScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.users = []

        self.setStyleSheet("background-color: #eef2f7;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 0)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(750)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(18)

        title = QLabel("Select Registered User")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- SEARCH ----------------
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search user...")
        self.search.setFixedHeight(55)
        self.search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cfd9e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                background: white;
                color: #1a2b49;
            }
        """)
        self.search.textChanged.connect(self.filter_users)

        # ---------------- LIST ----------------
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #cfd9e6;
                border-radius: 10px;
                font-size: 16px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 15px;
            }
            QListWidget::item:selected {
                background-color: #2d63c8;
                color: white;
            }
        """)
        self.list_widget.itemClicked.connect(self.select_user)

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
        back_btn.clicked.connect(
            lambda: self.main.stack.setCurrentWidget(self.main.user_type)
        )

        card_layout.addWidget(title)
        card_layout.addWidget(self.search)
        card_layout.addWidget(self.list_widget)
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

    # ---------------- LOAD USERS ----------------
    def load_users(self):
        self.users = get_users()
        self.populate_list(self.users)

    def populate_list(self, users):
        self.list_widget.clear()
        for user in users:
            item = QListWidgetItem(
                f'{user["full_name"]} | Age: {user["age"]} | {user["sex"]}'
            )
            item.setData(Qt.UserRole, user)
            self.list_widget.addItem(item)

    # ---------------- SEARCH ----------------
    def filter_users(self, text):
        filtered = [
            u for u in self.users
            if text.lower() in u["full_name"].lower()
        ]
        self.populate_list(filtered)

    # ---------------- SELECT ----------------
    def select_user(self, item):
        user = item.data(Qt.UserRole)

        self.main.upload.set_user_data(
            user["full_name"],
            str(user["age"]),
            user["sex"]
        )

        self.main.stack.setCurrentWidget(self.main.upload)