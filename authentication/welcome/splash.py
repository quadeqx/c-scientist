from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import sys

class SplashScreen(QSplashScreen):
    """Loading splash screen."""

    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.SplashScreen)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.setContentsMargins(10, 10, 10, 20)

        container = QWidget(self)
        container.setLayout(layout)
        container.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.showMessage("Fetching data from Binance...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)

def resource_path(relative_path):
    """Return the absolute path to a resource, compatible with AppImage."""
    # Base path of the currently running script (in AppImage or dev)
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

def show_splash(app, main_window_class):
    """Show splash screen then the main window."""
    image_path = resource_path("authentication/welcome/images/GTR.jpg")
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        #print(f"Error: Failed to load image at {image_path}")
        pixmap = QPixmap(200, 150)
        pixmap.fill(Qt.GlobalColor.black)

    splash = SplashScreen(pixmap)
    splash.show()
    app.processEvents()
    import time
    time.sleep(0.01)  # 10ms to ensure splash screen renders
    app.processEvents()

    main_window = main_window_class()

    return splash, main_window
