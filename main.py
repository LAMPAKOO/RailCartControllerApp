import ctypes
import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from app_logic import IndustrialControlApp

# --- BLOKADA SKALOWANIA EKRANU (Zastępuje plik .bat) ---
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
# -------------------------------------------------------

try:
    myappid = 'shm.system.RailCartController.1' # Dowolny, unikalny ciąg znaków
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# Added distance calibration parameter command and GUI (settings tab) support.

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Konfiguracja ciemnego motywu
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(30, 30, 30))
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(65, 65, 65))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    app.setPalette(palette)
    
    # Uruchomienie głównego okna
    window = IndustrialControlApp()
    window.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
