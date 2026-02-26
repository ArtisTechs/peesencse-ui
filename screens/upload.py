import os
import subprocess

# ==========================================================
# PLATFORM MODE
# ==========================================================
IS_RPI = True

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QApplication
)

from services.api import analyze_sample


class UploadScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.name = ""
        self.age = ""
        self.sex = ""
        self.user_id = ""
        self.image_path = ""

        self.setup_ui()

    # ==========================================================
    # UI SETUP (7-INCH OPTIMIZED)
    # ==========================================================

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f6;
                font-family: Segoe UI, Arial;
            }

            QLabel#title {
                font-size: 18px;
                font-weight: 600;
                color: #1f2937;
            }

            QFrame#card {
                background-color: white;
                border-radius: 14px;
                padding: 16px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                min-height: 42px;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QPushButton:disabled {
                background-color: #9ca3af;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        # Title
        title = QLabel("Urine Sample Capture")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Card container
        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(10)

        # Preview placeholder (scaled to 7" screen)
        self.preview_label = QLabel("Camera Ready")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedHeight(380)
        self.preview_label.setStyleSheet("""
            background-color: #111827;
            color: white;
            border-radius: 10px;
            font-size: 14px;
        """)

        # Analyze Button
        button_layout = QHBoxLayout()

        self.analyze_btn = QPushButton("Analyze Sample")
        self.analyze_btn.clicked.connect(self.start_analysis)

        button_layout.addStretch()
        button_layout.addWidget(self.analyze_btn)
        button_layout.addStretch()

        card_layout.addWidget(self.preview_label)
        card_layout.addLayout(button_layout)

        main_layout.addWidget(title)
        main_layout.addWidget(self.card)

    # ==========================================================
    # USER DATA
    # ==========================================================

    def set_user_data(self, name, age, sex, user_id):
        self.name = name
        self.age = age
        self.sex = sex
        self.user_id = user_id

    # ==========================================================
    # CAPTURE + ANALYSIS (RPICAM)
    # ==========================================================

    def start_analysis(self):
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Capturing...")
        QApplication.processEvents()

        self.image_path = os.path.abspath("captured_sample.jpg")

        try:
            if IS_RPI:
                cmd = [
                    "rpicam-still",
                    "-o", self.image_path,
                    "--width", "1280",
                    "--height", "720",
                    "--nopreview",
                    "--timeout", "1000",
                    "--shutter", "20000",
                    "--gain", "1"
                ]
                subprocess.run(cmd, check=True)
            else:
                raise RuntimeError("Non-RPI mode not supported")

            self.preview_label.setText("Processing...")
            QApplication.processEvents()

            self.perform_analysis()

        except Exception as e:
            QMessageBox.critical(self, "Capture Error", str(e))
            self.analyze_btn.setEnabled(True)
            self.analyze_btn.setText("Analyze Sample")
            self.preview_label.setText("Camera Error")

    # ==========================================================
    # ANALYSIS
    # ==========================================================

    def perform_analysis(self):
        try:
            response = analyze_sample(
                self.user_id,
                self.age,
                self.sex,
                self.image_path
            )

            self.main.result.set_result(
                response,
                name=self.name,
                age=self.age,
                gender=self.sex
            )
            self.main.stack.setCurrentWidget(self.main.result)

        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", str(e))

        self.analyze_btn.setText("Analyze Sample")
        self.analyze_btn.setEnabled(True)
        self.preview_label.setText("Camera Ready")

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):
        self.name = ""
        self.age = ""
        self.sex = ""
        self.user_id = ""
        self.image_path = ""

        self.analyze_btn.setText("Analyze Sample")
        self.analyze_btn.setEnabled(True)
        self.preview_label.setText("Camera Ready")