from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton,
    QLabel, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QGuiApplication
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
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 0)
        main_layout.setSpacing(0)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(880)
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #f9fafb;
                border-radius: 22px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(60, 45, 60, 45)
        card_layout.setSpacing(22)

        title = QLabel("Select Registered User")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- SEARCH ----------------
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search user...")
        self.search.setFixedHeight(58)
        self.search.setAttribute(Qt.WA_InputMethodEnabled, True)
        self.search.setFocusPolicy(Qt.StrongFocus) 
        self.search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 14px;
                font-size: 17px;
                background: white;
                color: #111827;
            }
        """)
        self.search.textChanged.connect(self.filter_users)

        # ---------------- LIST ----------------
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(12)
        self.list_widget.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }

            QListWidget::item {
                border-radius: 14px;
                padding: 20px;
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
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
            }
        """)
        self.list_widget.itemClicked.connect(self.select_user)

        # ---------------- BACK BUTTON ----------------
        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(58)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 17px;
                border-radius: 12px;
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
        card_layout.addSpacing(40)  # bottom buffer for keyboard

        # ---------------- SCROLL WRAPPER ----------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.addStretch()
        scroll_layout.addWidget(card, alignment=Qt.AlignCenter)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_container)

        # ---------------- FOOTER ----------------
        footer = QLabel(
            "© 2026 PeeSense – AI-Assisted Urinalysis System\n"
            "For Academic & Research Use Only"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setMinimumHeight(60)
        footer.setMaximumHeight(80)
        footer.setStyleSheet("""
            background-color: #2d63c8;
            color: white;
            font-size: 14px;
            font-weight: 500;
        """)

        main_layout.addWidget(scroll)
        main_layout.addWidget(footer)

    # -------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        self.load_users()

        # Force focus to search field
        self.search.setFocus(Qt.OtherFocusReason)

        # Force keyboard show
        QGuiApplication.inputMethod().show()

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
            item.setSizeHint(item.sizeHint())
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

        self.main.upload.set_user_data(
            user["full_name"],
            str(user["age"]),
            user["gender"],
            user["id"]
        )

        self.main.stack.setCurrentWidget(self.main.upload)