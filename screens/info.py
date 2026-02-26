from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QHBoxLayout, QLineEdit, QComboBox,
    QMessageBox, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIntValidator
from PySide6.QtWidgets import QScrollArea
from services.api import create_user


class ConfirmDialog(QDialog):
    def __init__(self, full_name, age, sex):
        super().__init__()

        self.setFixedSize(340, 240)
        self.setWindowTitle("Confirm Details")
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
            }
            QLabel {
                color: #1a2b49;
                font-size: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Please confirm the entered details:")
        title.setStyleSheet("font-weight:600; font-size:13px;")

        info = QLabel(
            f"Name: {full_name}\n"
            f"Age: {age}\n"
            f"Sex: {sex}"
        )

        question = QLabel("Are these correct?")

        button_layout = QHBoxLayout()

        no_btn = QPushButton("No")
        no_btn.setFixedHeight(35)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                border-radius: 6px;
                font-size: 12px;
            }
        """)
        no_btn.clicked.connect(self.reject)

        yes_btn = QPushButton("Yes")
        yes_btn.setFixedHeight(35)
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d63c8;
                color: white;
                border-radius: 6px;
                font-size: 12px;
            }
        """)
        yes_btn.clicked.connect(self.accept)

        button_layout.addWidget(no_btn)
        button_layout.addWidget(yes_btn)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(question)
        layout.addStretch()
        layout.addLayout(button_layout)

class InfoScreen(QWidget):
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

        # ---------------- SCROLL AREA ----------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(420)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        title = QLabel("Basic Information")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # INPUTS (unchanged)
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.first_name.setFixedHeight(40)

        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name (Optional)")
        self.middle_name.setFixedHeight(40)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        self.last_name.setFixedHeight(40)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        self.age.setFixedHeight(40)
        self.age.setValidator(QIntValidator(0, 120))

        self.sex = QComboBox()
        self.sex.addItems(["Select Sex", "Male", "Female"])
        self.sex.setFixedHeight(40)

        input_style = """
            QLineEdit, QComboBox {
                border: 1px solid #cfd9e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                background: white;
                color: #1a2b49;
            }
        """

        for widget in [
            self.first_name,
            self.middle_name,
            self.last_name,
            self.age,
            self.sex
        ]:
            widget.setStyleSheet(input_style)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
        self.error_label.hide()

        button_layout = QHBoxLayout()

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 13px;
                border-radius: 8px;
            }
        """)
        back_btn.clicked.connect(self.go_back)

        next_btn = QPushButton("Next")
        next_btn.setFixedHeight(40)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d63c8;
                color: white;
                font-size: 14px;
                border-radius: 8px;
            }
        """)
        next_btn.clicked.connect(self.go_next)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(next_btn)

        card_layout.addWidget(title)
        card_layout.addWidget(self.first_name)
        card_layout.addWidget(self.middle_name)
        card_layout.addWidget(self.last_name)
        card_layout.addWidget(self.age)
        card_layout.addWidget(self.sex)
        card_layout.addWidget(self.error_label)
        card_layout.addLayout(button_layout)

        scroll_layout.addWidget(card, alignment=Qt.AlignTop)
        scroll.setWidget(scroll_content)

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

        main_layout.addWidget(scroll)
        main_layout.addWidget(footer)

        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f7;
                color: #1a2b49;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 0)

        # ---------------- CARD ----------------
        card = QFrame()
        card.setMaximumWidth(420)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        title = QLabel("Basic Information")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2d63c8;")
        title.setAlignment(Qt.AlignCenter)

        # ---------------- INPUTS ----------------
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.first_name.setFixedHeight(40)

        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name (Optional)")
        self.middle_name.setFixedHeight(40)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        self.last_name.setFixedHeight(40)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        self.age.setFixedHeight(40)
        self.age.setValidator(QIntValidator(0, 120))

        self.sex = QComboBox()
        self.sex.addItems(["Select Sex", "Male", "Female"])
        self.sex.setFixedHeight(40)

        input_style = """
            QLineEdit, QComboBox {
                border: 1px solid #cfd9e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                background: white;
                color: #1a2b49;
            }
            QComboBox QAbstractItemView {
                background: white;
                color: black;
                selection-background-color: #2d63c8;
                selection-color: white;
            }
        """

        for widget in [
            self.first_name,
            self.middle_name,
            self.last_name,
            self.age,
            self.sex
        ]:
            widget.setStyleSheet(input_style)

        # ---------------- ERROR LABEL ----------------
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("""
            color: #d32f2f;
            font-size: 12px;
        """)
        self.error_label.hide()

        # ---------------- BUTTONS ----------------
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa5b1;
                color: white;
                font-size: 13px;
                border-radius: 8px;
            }
        """)
        back_btn.clicked.connect(self.go_back)

        next_btn = QPushButton("Next")
        next_btn.setFixedHeight(40)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d63c8;
                color: white;
                font-size: 14px;
                border-radius: 8px;
            }
        """)
        next_btn.clicked.connect(self.go_next)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(next_btn)

        card_layout.addWidget(title)
        card_layout.addWidget(self.first_name)
        card_layout.addWidget(self.middle_name)
        card_layout.addWidget(self.last_name)
        card_layout.addWidget(self.age)
        card_layout.addWidget(self.sex)
        card_layout.addWidget(self.error_label)
        card_layout.addLayout(button_layout)

        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(card, alignment=Qt.AlignCenter)
        center_layout.addStretch()

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

    # ---------------- VALIDATION ----------------
    def validate_fields(self):
        self.error_label.hide()
        self.error_label.setText("")

        if not self.first_name.text().strip():
            self.show_error("First name is required.")
            self.highlight(self.first_name)
            return False

        if not self.last_name.text().strip():
            self.show_error("Last name is required.")
            self.highlight(self.last_name)
            return False

        if not self.age.text().strip():
            self.show_error("Age is required.")
            self.highlight(self.age)
            return False

        if not self.age.text().isdigit():
            self.show_error("Age must be numeric.")
            self.highlight(self.age)
            return False

        if self.sex.currentText() == "Select Sex":
            self.show_error("Please select a sex.")
            self.highlight(self.sex)
            return False

        return True

    def highlight(self, widget):
        widget.setStyleSheet("""
            border: 2px solid #d32f2f;
            border-radius: 6px;
            padding: 6px;
            font-size: 13px;
            background: white;
            color: #1a2b49;
        """)

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()

    # ---------------- NAVIGATION ----------------
    def go_back(self):
        self.main.stack.setCurrentWidget(self.main.user_type)

    def go_next(self):
        if not self.validate_fields():
            return

        firstname = self.first_name.text().strip().title()
        middlename = self.middle_name.text().strip().title()
        lastname = self.last_name.text().strip().title()

        self.first_name.setText(firstname)
        self.middle_name.setText(middlename)
        self.last_name.setText(lastname)

        full_name = f"{firstname} {middlename} {lastname}".strip()
        full_name = " ".join(full_name.split())

        age = self.age.text().strip()
        sex = self.sex.currentText()

        dialog = ConfirmDialog(full_name, age, sex)

        if dialog.exec() == QDialog.Accepted:
            try:
                result = create_user(
                    firstname,
                    middlename,
                    lastname,
                    age,
                    sex
                )

                user_id = result.get("id")

                self.main.upload.set_user_data(
                    full_name,
                    age,
                    sex,
                    user_id
                )

                self.main.stack.setCurrentWidget(self.main.upload)

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "API Error",
                    f"Failed to save user:\n{str(e)}"
                )

    def reset(self):
        self.first_name.clear()
        self.middle_name.clear()
        self.last_name.clear()
        self.age.clear()
        self.sex.setCurrentIndex(0)

        self.error_label.hide()
        self.error_label.setText("")

        default_style = """
            QLineEdit, QComboBox {
                border: 1px solid #cfd9e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                background: white;
                color: #1a2b49;
            }
        """

        for widget in [
            self.first_name,
            self.middle_name,
            self.last_name,
            self.age,
            self.sex
        ]:
            widget.setStyleSheet(default_style)