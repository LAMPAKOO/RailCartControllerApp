import sys
import os
from PySide6 import QtWidgets, QtCore, QtGui

# --- 1. Definicja naszego filtra zdarzeń ---
class KeyboardEventFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        # Przechwytujemy zdarzenie wciśnięcia lewego przycisku myszy (lub "kliknięcia" palcem w ekran USB)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                try:
                    # Twarde wywołanie systemowej klawiatury dotykowej
                    sciezka_tabtip = r"C:\Program Files\Common Files\microsoft shared\ink\TabTip.exe"
                    os.startfile(sciezka_tabtip)
                    print("Klawiatura wywołana!")
                except Exception as e:
                    print(f"Nie udało się uruchomić klawiatury: {e}")
                    
        # Ważne: zwracamy standardowe zachowanie, aby kursor pojawił się w polu tekstowym
        return super().eventFilter(obj, event)


# --- 2. Główne okno aplikacji ---
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Klawiatury USB")
        self.resize(400, 300)

        # Główny layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Etykieta informacyjna
        label = QtWidgets.QLabel("Kliknij w pole poniżej (myszką lub palcem):")
        label.setFont(QtGui.QFont("Segoe UI", 12))
        layout.addWidget(label)

        # Tworzymy pole tekstowe (QLineEdit)
        self.pole_tekstowe = QtWidgets.QLineEdit()
        self.pole_tekstowe.setFixedSize(300, 50)
        self.pole_tekstowe.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold))
        self.pole_tekstowe.setPlaceholderText("Wpisz wartość...")
        self.pole_tekstowe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pole_tekstowe)

        # --- 3. PODPIĘCIE FILTRA ---
        # Tworzymy instancję naszego filtra i przypisujemy ją do okna (self)
        self.keyboard_filter = KeyboardEventFilter(self)
        
        # Instalujemy filtr na konkretnym polu tekstowym
        self.pole_tekstowe.installEventFilter(self.keyboard_filter)

        # Dodajemy pustą przestrzeń na dole, żeby okno ładnie wyglądało
        layout.addStretch()


# --- 4. Uruchomienie aplikacji ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Tworzymy i pokazujemy główne okno
    window = MainWindow()
    window.show()
    
    # Uruchamiamy główną pętlę programu
    sys.exit(app.exec())