import os

IS_RPI = True

from PySide6.QtCore import Qt, QProcess, QByteArray, QTimer
from PySide6.QtGui import QPixmap
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

        self.process = None
        self.buffer = QByteArray()
        self.last_frame = None

        self.preview_width = 640
        self.preview_height = 480

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
            QFrame#card { background-color: white; border-radius: 16px; padding: 24px; }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                min-height: 42px;
                padding: 6px 14px;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)
        card_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Urine Sample Capture")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Ensure proper focus and stable lighting before analysis.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(self.preview_width, self.preview_height)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(
            "background-color: #111827; border-radius: 12px;"
        )

        self.analyze_btn = QPushButton("Analyze Sample")
        self.analyze_btn.clicked.connect(self.start_analysis)

        self.refresh_btn = QPushButton("Refresh Camera")
        self.refresh_btn.clicked.connect(self.refresh_camera)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.analyze_btn)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.preview_label)
        card_layout.addLayout(button_layout)

        main_layout.addWidget(self.card)

    # ==========================================================
    # CAMERA CONTROL
    # ==========================================================

    def start_camera_stream(self):
        if not IS_RPI:
            return

        # disable buttons during warmup
        self.set_buttons_enabled(False)
        self.refresh_btn.setText("Starting Camera...")
        self.analyze_btn.setText("Waiting...")

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stream)

        cmd = [
            "rpicam-vid",
            "--nopreview",
            "--inline",
            "--width", "640",
            "--height", "480",
            "--framerate", "20",
            "--codec", "mjpeg",
            "--quality", "90",
            "-o", "-"
        ]

        self.process.start(cmd[0], cmd[1:])

        if not self.process.waitForStarted(3000):
            QMessageBox.critical(self, "Camera Error", "Failed to start camera.")
            self.process = None
            return

        # 5 second warmup delay
        QTimer.singleShot(5000, self.camera_ready)

    def camera_ready(self):
        self.refresh_btn.setText("Refresh Camera")
        self.analyze_btn.setText("Analyze Sample")
        self.set_buttons_enabled(True)

    def stop_camera_stream(self):
        if self.process:
            self.process.kill()
            self.process.waitForFinished(3000)
            self.process = None

        self.buffer.clear()
        self.last_frame = None
        self.preview_label.clear()

    def refresh_camera(self):
        self.set_buttons_enabled(False)
        self.refresh_btn.setText("Restarting...")
        self.analyze_btn.setText("Waiting...")
        QApplication.processEvents()

        self.stop_camera_stream()

        QTimer.singleShot(500, self.start_camera_stream)

    # ==========================================================
    # STREAM READER
    # ==========================================================

    def read_stream(self):
        if not self.process:
            return

        self.buffer.append(self.process.readAllStandardOutput())

        if self.buffer.size() > 2_000_000:
            self.buffer.clear()
            return

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
    # ANALYSIS
    # ==========================================================

    def start_analysis(self):
        if not self.last_frame:
            QMessageBox.warning(self, "No Frame", "Camera not ready yet.")
            return

        self.set_buttons_enabled(False)
        self.analyze_btn.setText("Analyzing...")
        QApplication.processEvents()

        self.image_path = os.path.abspath("captured_sample.jpg")

        try:
            with open(self.image_path, "wb") as f:
                f.write(self.last_frame)

            self.perform_analysis()

        except Exception as e:
            QMessageBox.critical(self, "Capture Error", str(e))

        self.analyze_btn.setText("Analyze Sample")
        self.set_buttons_enabled(True)

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
    # UTIL
    # ==========================================================

    def set_buttons_enabled(self, state):
        self.refresh_btn.setEnabled(state)
        self.analyze_btn.setEnabled(state)

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):
        self.stop_camera_stream()
        QTimer.singleShot(300, self.start_camera_stream)

    # ==========================================================
    # CLEANUP
    # ==========================================================

    def closeEvent(self, event):
        self.stop_camera_stream()
        event.accept()