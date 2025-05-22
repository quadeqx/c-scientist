from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.SplashScreen)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid white;
                border-radius: 5px;
                text-align: center;
                background-color: rgba(0, 0, 0, 50);
                color: white;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
            }
        """)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.progress_bar)
        layout.setContentsMargins(10, 10, 10, 20)

        container = QWidget(self)
        container.setLayout(layout)
        container.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.showMessage("Application Loading...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)

        self.progress_value = 0
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.progress_timer.stop()

def show_splash(app, main_window_class):
    image_path = "authentication/welcome/images/GTR.jpg"
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        print(f"Error: Failed to load image at {image_path}")
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.GlobalColor.black)
    splash = SplashScreen(pixmap)
    splash.show()

    app.processEvents()

    main_window = main_window_class()

    def show_main_window():
        main_window.show()
        QTimer.singleShot(100, splash.close)

    QTimer.singleShot(10000, show_main_window)

    return main_window
