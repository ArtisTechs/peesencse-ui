from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMessageBox

from services.api import get_users


class RegisteredUserScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.users = []

        self.setObjectName("root")
        self.setStyleSheet("""
            QWidget#root {
                background-color: #1e1e1e;
                color: #111827;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 0)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(500)
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #f9fafb;
                border-radius: 16px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        title = QLabel("Select Registered User")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- SEARCH ----------------
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search user...")
        self.search.setFixedHeight(40)
        self.search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                background: white;
                color: #111827;
            }
        """)
        self.search.textChanged.connect(self.filter_users)

        # ---------------- LIST ----------------
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(6)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
                font-size: 13px;
            }

            QListWidget::item {
                border-radius: 10px;
                padding: 10px;
                background-color: white;
                color: #111827;
                border: 1px solid #e5e7eb;
            }

            QListWidget::item:hover {
                background-color: #eef2ff;
                border: 1px solid #2d63c8;
            }

            QListWidget::item:selected {
                background-color: #2d63c8;
                color: white;
                border: 1px solid #2d63c8;
            }

            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 3px;
            }
        """)
        self.list_widget.itemClicked.connect(self.select_user)

        # ---------------- BACK BUTTON ----------------
        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 13px;
                border-radius: 8px;
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
        footer.setFixedHeight(55)
        footer.setStyleSheet("""
            background-color: #2d63c8;
            color: white;
            font-size: 11px;
        """)

        main_layout.addLayout(center_layout)
        main_layout.addWidget(footer)

    # -------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        self.load_users()

    # -------------------------------------------------
    def load_users(self):
        try:
            raw_users = get_users()
            self.users = self.normalize_users(raw_users)
            self.populate_list(self.users)
        except Exception as e:
            print("Failed to load users:", e)
            self.users = []
            self.list_widget.clear()

    # -------------------------------------------------
    def normalize_users(self, raw_users):
        normalized = []

        for u in raw_users:
            firstname = (u.get("firstname") or "").strip()
            middlename = (u.get("middlename") or "").strip()
            lastname = (u.get("lastname") or "").strip()

            full_name = f"{firstname} {middlename} {lastname}".strip()
            full_name = " ".join(full_name.split())

            normalized.append({
                "id": u.get("id"),
                "full_name": full_name,
                "age": u.get("age"),
                "gender": u.get("gender")
            })

        return normalized

    # -------------------------------------------------
    def populate_list(self, users):
        self.list_widget.clear()

        for user in users:
            item = QListWidgetItem(
                f'{user["full_name"]}\nAge: {user["age"]}    Sex: {user["gender"]}'
            )
            item.setData(Qt.UserRole, user)
            self.list_widget.addItem(item)

    # -------------------------------------------------
    def filter_users(self, text):
        text = text.lower().strip()

        filtered = [
            u for u in self.users
            if text in u["full_name"].lower()
        ]

        self.populate_list(filtered)

    # -------------------------------------------------
        def select_user(self, item):
            user = item.data(Qt.UserRole)

            reply = QMessageBox.question(
                self,
                "Confirm Selection",
                f'Select user:\n\n{user["full_name"]}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                return

            self.main.upload.set_user_data(
                user["full_name"],
                str(user["age"]),
                user["gender"],
                user["id"]
            )

            self.main.stack.setCurrentWidget(self.main.upload)