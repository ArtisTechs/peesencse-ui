import os

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
        self.last_frame = None

        # Preview size (must match stream size)
        self.preview_width = 320
        self.preview_height = 240

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
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(self.preview_width, self.preview_height)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
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
    # CAMERA STREAM (STABLE)
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
            "--width", "320",
            "--height", "240",
            "--framerate", "8",
            "--codec", "mjpeg",
            "--quality", "70",
            "--buffer-count", "2",
            "-o", "-"
        ]

        self.process.start(cmd[0], cmd[1:])

    def read_stream(self):
        if not self.process:
            return

        self.buffer.append(self.process.readAllStandardOutput())

        # Hard memory cap to prevent freeze
        if self.buffer.size() > 1_500_000:
            self.buffer.clear()
            return

        # Extract newest complete JPEG only
        start = self.buffer.lastIndexOf(b'\xff\xd8')
        end = self.buffer.lastIndexOf(b'\xff\xd9')

        if start == -1 or end == -1 or end <= start:
            return

        jpg = self.buffer[start:end + 2]
        self.buffer.clear()

        self.last_frame = bytes(jpg)

        pixmap = QPixmap()
        if not pixmap.loadFromData(jpg):
            return

        scaled = pixmap.scaled(
            self.preview_width,
            self.preview_height,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )

        self.preview_label.setPixmap(scaled)

    # ==========================================================
    # USER DATA
    # ==========================================================

    def set_user_data(self, name, age, sex, user_id):
        self.name = name
        self.age = age
        self.sex = sex
        self.user_id = user_id

    # ==========================================================
    # CAPTURE FROM STREAM
    # ==========================================================

    def start_analysis(self):
        if not self.last_frame:
            QMessageBox.warning(self, "No Frame", "Camera not ready yet.")
            return

        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Processing...")
        QApplication.processEvents()

        self.image_path = os.path.abspath("captured_sample.jpg")

        try:
            with open(self.image_path, "wb") as f:
                f.write(self.last_frame)

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
            self.process.waitForFinished()
        event.accept()

    def reset(self):
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyze Sample")