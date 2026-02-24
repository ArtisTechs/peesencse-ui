import qrcode
import uuid

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
                background-color: #f3f4f6;
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
                font-size: 20px;
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

        # Card (controlled width)
        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(700)
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(25)
        card_layout.setAlignment(Qt.AlignCenter)

        # Heading
        heading = QLabel("Urinalysis Result")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)

        # Result Text
        self.result_label = QLabel("Waiting for result...")
        self.result_label.setObjectName("resultText")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)

        # QR
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(220, 220)
        self.qr_label.hide()

        # Single Button (inside card only)
        self.back_btn = QPushButton("Test Another Sample")
        self.back_btn.clicked.connect(self.go_home)

        card_layout.addWidget(heading)
        card_layout.addWidget(self.result_label)
        card_layout.addWidget(self.qr_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.back_btn)

        main_layout.addWidget(card)

    # ==========================================================
    # SET RESULT + QR
    # ==========================================================

    def set_result(self, result):
        self.qr_label.clear()
        self.qr_label.hide()

        if isinstance(result, dict):
            message = result.get("message", "Result available.")
            url = result.get("url")

            self.result_label.setText(message)

            if not url:
                random_id = uuid.uuid4().hex[:10]
                url = f"https://preesense.ai/report/{random_id}"

            self.generate_qr(url)

        else:
            self.result_label.setText(str(result))
            random_id = uuid.uuid4().hex[:10]
            sample_url = f"https://preesense.ai/report/{random_id}"
            self.generate_qr(sample_url)

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

    def go_home(self):
        self.qr_label.clear()
        self.qr_label.hide()
        self.main.stack.setCurrentWidget(self.main.home)