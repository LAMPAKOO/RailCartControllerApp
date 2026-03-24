from PySide6 import QtWidgets
from ui_helpers import DummyCurve
from ui_col1_motor import setup_motor_column
from ui_col2_inverter import setup_inverter_column
from ui_col3_system import setup_system_column

class AppUI(QtWidgets.QMainWindow):
    def init_ui(self):
        self.setWindowTitle("Industrial Motor Control & Data Logger")
        self.resize(1400, 850)
        
        # Główne tło okna
        self.setStyleSheet("QMainWindow { background-color: #1e1e1e; }")
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny układ podzielony poziomo na 3 równe kolumny
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Uruchamianie plików budujących układ (moduły podpinają się pod "self")
        setup_motor_column(self, main_layout)
        setup_inverter_column(self, main_layout)
        setup_system_column(self, main_layout)

        # Zaślepki chroniące przed błędami logicznymi przy próbie aktualizacji usuniętego wykresu
        self.curve_distance = DummyCurve()
        self.curve_speed = DummyCurve()
        self.curve_rpm = DummyCurve()