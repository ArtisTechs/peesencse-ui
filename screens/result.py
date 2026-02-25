import qrcode
from PySide6.QtCore import QDateTime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy
)
from PySide6.QtWidgets import QHBoxLayout


class ResultScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setup_ui()

    # ==========================================================
    # UI SETUP
    # ==========================================================

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Segoe UI, Arial;
            }

            QFrame#card {
                background-color: white;
                border-radius: 18px;
                padding: 40px;
            }

            QLabel#heading {
                font-size: 26px;
                font-weight: 600;
                color: #111827;
            }

            QLabel#resultText {
                font-size: 18px;
                color: #111827;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 15px;
                min-height: 48px;
            }

            QPushButton:hover {
                background-color: #1e40af;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(700)
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(25)
        card_layout.setAlignment(Qt.AlignCenter)

        heading = QLabel("Urinalysis Result")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("Waiting for result...")
        self.result_label.setObjectName("resultText")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(220, 220)
        self.qr_label.hide()

        self.back_btn = QPushButton("Test Another Sample")
        self.back_btn.clicked.connect(self.go_home)

        card_layout.addWidget(heading)
        card_layout.addWidget(self.result_label)
        qr_container = QHBoxLayout()
        qr_container.addStretch()
        qr_container.addWidget(self.qr_label, alignment=Qt.AlignCenter)
        qr_container.addStretch()

        card_layout.addLayout(qr_container)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.back_btn)

        main_layout.addWidget(card)

    # ==========================================================
    # SET RESULT (ALIGNED WITH /analyze RESPONSE)
    # ==========================================================

    def set_result(self, data, name="", age="", gender=""):
        self.qr_label.clear()
        self.qr_label.hide()

        if not isinstance(data, dict):
            self.result_label.setText("Invalid server response.")
            return

        rbc = data.get("rbc")
        wbc = data.get("wbc")
        uti = data.get("uti")
        result_url = data.get("result_url")

        uti_text = "POSITIVE" if uti else "NEGATIVE"

        current_dt = QDateTime.currentDateTime()
        time_text = current_dt.toString("MMMM d, yyyy hh:mm ap")

        result_text = (
            f"Patient Name: {name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n\n"
            f"Date & Time: {time_text}\n\n"
            f"RBC Count: {rbc}\n"
            f"WBC Count: {wbc}\n"
            f"UTI Result: {uti_text}"
        )

        self.result_label.setText(result_text)

        if result_url:
            self.generate_qr(result_url)

    # ==========================================================
    # QR GENERATION
    # ==========================================================

    def generate_qr(self, url):
        qr = qrcode.make(url)
        qr_path = "temp_qr.png"
        qr.save(qr_path)

        pixmap = QPixmap(qr_path)
        pixmap = pixmap.scaled(
            200,
            200,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.qr_label.setPixmap(pixmap)
        self.qr_label.show()

    # ==========================================================
    # NAVIGATION
    # ==========================================================
    def reset(self):
        self.result_label.setText("Waiting for result...")
        self.qr_label.clear()
        self.qr_label.hide()

    def go_home(self):
        self.reset()

        if hasattr(self.main, "upload"):
            self.main.upload.reset()

        if hasattr(self.main, "info"):
            self.main.info.reset()

        self.main.stack.setCurrentWidget(self.main.home)