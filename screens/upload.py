import os
import subprocess

IS_RPI = True

from PySide6.QtCore import Qt, QProcess, QByteArray
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QApplication,
    QSizePolicy
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

        self.process = None
        self.buffer = QByteArray()

        self.setup_ui()
        self.start_camera_stream()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #f3f6fb; font-family: Segoe UI, Arial; }
            QLabel#title { font-size: 20px; font-weight: 600; color: #1f2937; }
            QLabel#subtitle { font-size: 13px; color: #6b7280; }
            QFrame#card { background-color: white; border-radius: 16px; padding: 18px; }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 15px;
                border-radius: 10px;
                min-height: 48px;
            }
            QPushButton:pressed { background-color: #1e40af; }
            QPushButton:disabled { background-color: #9ca3af; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        title = QLabel("Urine Sample Capture")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Ensure proper focus and stable lighting before analysis.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(360)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview_label.setStyleSheet("""
            background-color: #111827;
            border-radius: 12px;
        """)

        self.analyze_btn = QPushButton("Analyze Sample")
        self.analyze_btn.clicked.connect(self.start_analysis)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.analyze_btn)
        button_layout.addStretch()

        card_layout.addWidget(self.preview_label)
        card_layout.addLayout(button_layout)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(self.card)

    # ==========================================================
    # LIVE STREAM USING RPICAM-VID
    # ==========================================================

    def start_camera_stream(self):
        if not IS_RPI:
            return

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stream)

        cmd = [
            "rpicam-vid",
            "--nopreview",
            "--inline",
            "--width", "640",
            "--height", "480",
            "--framerate", "30",
            "--codec", "mjpeg",
            "-o", "-"
        ]

        self.process.start(cmd[0], cmd[1:])

    def set_user_data(self, name, age, sex, user_id):
        self.name = name
        self.age = age
        self.sex = sex
        self.user_id = user_id

    def read_stream(self):
        self.buffer.append(self.process.readAllStandardOutput())

        while True:
            start = self.buffer.indexOf(b'\xff\xd8')  # JPEG start
            end = self.buffer.indexOf(b'\xff\xd9')    # JPEG end

            if start != -1 and end != -1 and end > start:
                jpg = self.buffer[start:end+2]
                self.buffer = self.buffer[end+2:]

                pixmap = QPixmap()
                pixmap.loadFromData(jpg)
                scaled = pixmap.scaled(
                    self.preview_label.width(),
                    self.preview_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled)
            else:
                break

    # ==========================================================
    # CAPTURE
    # ==========================================================

    def start_analysis(self):
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Capturing...")
        QApplication.processEvents()

        self.image_path = os.path.abspath("captured_sample.jpg")

        try:
            cmd = [
                "rpicam-still",
                "-o", self.image_path,
                "--width", "1280",
                "--height", "720",
                "--nopreview",
                "--timeout", "600",
                "--shutter", "20000",
                "--gain", "1"
            ]
            subprocess.run(cmd, check=True)

            self.analyze_btn.setText("Processing...")
            QApplication.processEvents()

            self.perform_analysis()

        except Exception as e:
            QMessageBox.critical(self, "Capture Error", str(e))

        self.analyze_btn.setText("Analyze Sample")
        self.analyze_btn.setEnabled(True)

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

    # ==========================================================
    # CLEANUP
    # ==========================================================

    def closeEvent(self, event):
        if self.process:
            self.process.kill()
        event.accept()

    def reset(self):
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyze Sample")