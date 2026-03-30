from PySide6 import QtWidgets, QtCore, QtGui

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
    edit.setValidator(QtGui.QIntValidator(0, 100))
    
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