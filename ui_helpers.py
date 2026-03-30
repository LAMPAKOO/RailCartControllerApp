import os
from PySide6 import QtWidgets, QtCore, QtGui

# --- KLASA FILTRA KLAWIATURY EKRANOWEJ ---
class KeyboardEventFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                try:
                    sciezka_tabtip = r"C:\Program Files\Common Files\microsoft shared\ink\TabTip.exe"
                    os.startfile(sciezka_tabtip)
                except Exception as e:
                    print(f"Nie udało się uruchomić klawiatury: {e}")
        return super().eventFilter(obj, event)

def add_touch_keyboard(widget):
    """Funkcja pomocnicza podpinająca klawiaturę do pola tekstowego"""
    widget.keyboard_filter = KeyboardEventFilter(widget)
    widget.installEventFilter(widget.keyboard_filter)
# ----------------------------------------

class DummyCurve:
    def setData(self, *args, **kwargs): pass

def create_step_control(ui, layout, label, cmd_name):
    h_layout = QtWidgets.QHBoxLayout()
    
    lbl = QtWidgets.QLabel(label)
    lbl.setFixedWidth(140) 
    lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    h_layout.addWidget(lbl)
    
    edit = QtWidgets.QLineEdit("0")
    edit.setFixedSize(120, 50) 
    edit.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    edit.setAlignment(QtCore.Qt.AlignCenter)
    edit.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    edit.setValidator(QtGui.QIntValidator(0, 2000))
    
    add_touch_keyboard(edit) # <--- DODANO KLAWIATURĘ
    
    btn_minus = QtWidgets.QPushButton("-")
    btn_minus.setFixedSize(50, 50) 
    btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_minus.clicked.connect(lambda: ui.adjust_value(edit, cmd_name, -int(ui.speed_inc.text() or 0)))
    
    btn_plus = QtWidgets.QPushButton("+")
    btn_plus.setFixedSize(50, 50) 
    btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_plus.clicked.connect(lambda: ui.adjust_value(edit, cmd_name, int(ui.speed_inc.text() or 0)))
    
    h_layout.addWidget(btn_minus)
    h_layout.addWidget(edit)
    h_layout.addWidget(btn_plus)
    h_layout.addStretch() 
    
    layout.addLayout(h_layout)
    return edit

def create_vfd_step_control(ui, layout, label, cmd_name):
    h_layout = QtWidgets.QHBoxLayout()
    
    lbl = QtWidgets.QLabel(label)
    lbl.setFixedWidth(140) 
    lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    h_layout.addWidget(lbl)
    
    edit = QtWidgets.QLineEdit("0")
    edit.setFixedSize(120, 50) 
    edit.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    edit.setAlignment(QtCore.Qt.AlignCenter)
    edit.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    edit.setValidator(QtGui.QIntValidator(0, 300))
    
    add_touch_keyboard(edit) # <--- DODANO KLAWIATURĘ
    
    btn_minus = QtWidgets.QPushButton("-")
    btn_minus.setFixedSize(50, 50) 
    btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_minus.clicked.connect(lambda: ui.adjust_value(edit, cmd_name, -int(ui.vfd_inc.text() or 0)))
    
    btn_plus = QtWidgets.QPushButton("+")
    btn_plus.setFixedSize(50, 50) 
    btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_plus.clicked.connect(lambda: ui.adjust_value(edit, cmd_name, int(ui.vfd_inc.text() or 0)))
    
    h_layout.addWidget(btn_minus)
    h_layout.addWidget(edit)
    h_layout.addWidget(btn_plus)
    h_layout.addStretch() 
    
    layout.addLayout(h_layout)
    return edit