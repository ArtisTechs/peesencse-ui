import os

# ==========================================================
# PLATFORM MODE
# ==========================================================
# True  = Raspberry Pi mode
# False = Windows / standard webcam mode
IS_RPI = False

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QSizePolicy,
    QApplication
)
from PySide6.QtMultimedia import (
    QCamera,
    QMediaDevices,
    QImageCapture,
    QMediaCaptureSession
)
from PySide6.QtMultimediaWidgets import QVideoWidget

from services.api import analyze_sample


class UploadScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.name = ""
        self.age = ""
        self.sex = ""
        self.image_path = ""

        self.camera = None
        self.capture = None
        self.capture_session = None

        self.setup_ui()
        self.setup_camera()

    # ==========================================================
    # UI SETUP
    # ==========================================================

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f6;
                font-family: Segoe UI, Arial;
            }

            QLabel#title {
                font-size: 22px;
                font-weight: 600;
                color: #1f2937;
            }

            QFrame#card {
                background-color: white;
                border-radius: 16px;
                padding: 20px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 15px;
                min-height: 48px;
            }

            QPushButton:hover {
                background-color: #1e40af;
            }

            QPushButton:disabled {
                background-color: #9ca3af;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 0)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Urine Sample Camera Capture")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Card container
        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # Camera preview
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(360)
        self.video_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # Single Analyze Button
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.analyze_btn = QPushButton("Analyze Sample")
        self.analyze_btn.clicked.connect(self.start_analysis)

        button_layout.addStretch()
        button_layout.addWidget(self.analyze_btn)
        button_layout.addStretch()

        card_layout.addWidget(self.video_widget)
        card_layout.addLayout(button_layout)

        # Footer
        footer = QLabel(
            "© 2026 PreeSense – AI-Assisted Urinalysis Screening System\n"
            "For Academic & Research Use Only"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(75)
        footer.setStyleSheet("""
            background-color: #2563eb;
            color: white;
            font-size: 14px;
            font-weight: 500;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(self.card)
        main_layout.addStretch()
        main_layout.addWidget(footer)

    # ==========================================================
    # CAMERA SETUP (QT6)
    # ==========================================================

    def setup_camera(self):
        cameras = QMediaDevices.videoInputs()

        if not cameras:
            QMessageBox.critical(
                self,
                "Camera Error",
                "No camera detected.\nCheck system permissions."
            )
            return

        selected_camera = None

        if IS_RPI:
            for cam in cameras:
                if "libcamera" in cam.description().lower():
                    selected_camera = cam
                    break

        if not selected_camera:
            selected_camera = cameras[0]

        self.camera = QCamera(selected_camera)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setVideoOutput(self.video_widget)

        self.capture = QImageCapture()
        self.capture_session.setImageCapture(self.capture)

        # Use imageCaptured instead of imageSaved
        self.capture.imageCaptured.connect(self.on_image_captured)

        self.camera.start()

    # ==========================================================
    # USER DATA
    # ==========================================================

    def set_user_data(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    # ==========================================================
    # ANALYZE FLOW (AUTO CAPTURE + API)
    # ==========================================================

    def start_analysis(self):
        if not self.capture:
            return

        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Processing...")
        QApplication.processEvents()

        self.image_path = os.path.abspath("captured_sample.jpg")
        self.capture.captureToFile(self.image_path)

    def on_image_captured(self, id, image):
        self.perform_analysis()

    def perform_analysis(self):
        try:
            QApplication.processEvents()

            response = analyze_sample(
                self.name,
                self.age,
                self.sex,
                self.image_path
            )

            self.main.result.set_result(response)
            self.main.stack.setCurrentWidget(self.main.result)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Analysis Error",
                str(e)
            )

        self.analyze_btn.setText("Analyze Sample")
        self.analyze_btn.setEnabled(True)

    # ==========================================================
    # CAMERA LIFECYCLE
    # ==========================================================

    def showEvent(self, event):
        if self.camera:
            self.camera.start()
        super().showEvent(event)

    def hideEvent(self, event):
        if self.camera:
            self.camera.stop()
        super().hideEvent(event)

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        event.accept()