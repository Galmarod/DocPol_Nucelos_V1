from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette, QFont, QPixmap, QIcon

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set size
        self.resize(700, 800)
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create label for logo
        self.label = QLabel()
        logo_path = str(Path(__file__).parent.parent / "assets" / "material" / "logo.png")
        pixmap = QPixmap(logo_path)
        # Scale the logo to a reasonable size while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                padding: 25px;
                border-radius: 10px;
                background-color: #28343e;
            }
        """)
        
        # Add to layout with stretch to center
        layout.addStretch()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        # Create fade out animation
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.setDuration(1000)  # 1 second fade out
        self.fade_anim.finished.connect(self.close)
        
        # Timer to start fade out
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade)
        
    def showEvent(self, event):
        super().showEvent(event)
        # Start timer when shown
        self.timer.start(2000)  # Show for 2 seconds before fade
        
    def start_fade(self):
        self.fade_anim.start()