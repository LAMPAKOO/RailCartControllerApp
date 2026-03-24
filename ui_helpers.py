from PySide6 import QtWidgets, QtGui

class DummyCurve:
    def setData(self, *args, **kwargs): pass

def create_step_control(ui, layout, label, cmd_name):
    h_layout = QtWidgets.QHBoxLayout()
    
    lbl = QtWidgets.QLabel(label)
    lbl.setFixedWidth(140) 
    lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    h_layout.addWidget(lbl)
    
    spin = QtWidgets.QSpinBox()
    spin.setRange(0, 2000)
    spin.setFixedSize(120, 50) 
    spin.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    
    btn_minus = QtWidgets.QPushButton("-")
    btn_minus.setFixedSize(50, 50) 
    btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_minus.clicked.connect(lambda: ui.adjust_value(spin, cmd_name, -ui.speed_inc.value()))
    
    btn_plus = QtWidgets.QPushButton("+")
    btn_plus.setFixedSize(50, 50) 
    btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_plus.clicked.connect(lambda: ui.adjust_value(spin, cmd_name, ui.speed_inc.value()))
    
    h_layout.addWidget(btn_minus)
    h_layout.addWidget(spin)
    h_layout.addWidget(btn_plus)
    h_layout.addStretch() 
    
    layout.addLayout(h_layout)
    return spin

def create_vfd_step_control(ui, layout, label, cmd_name):
    h_layout = QtWidgets.QHBoxLayout()
    
    lbl = QtWidgets.QLabel(label)
    lbl.setFixedWidth(140) 
    lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    h_layout.addWidget(lbl)
    
    spin = QtWidgets.QSpinBox()
    spin.setRange(0, 100) 
    spin.setFixedSize(120, 50) 
    spin.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    
    btn_minus = QtWidgets.QPushButton("-")
    btn_minus.setFixedSize(50, 50) 
    btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_minus.clicked.connect(lambda: ui.adjust_value(spin, cmd_name, -ui.vfd_inc.value()))
    
    btn_plus = QtWidgets.QPushButton("+")
    btn_plus.setFixedSize(50, 50) 
    btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_plus.clicked.connect(lambda: ui.adjust_value(spin, cmd_name, ui.vfd_inc.value()))
    
    h_layout.addWidget(btn_minus)
    h_layout.addWidget(spin)
    h_layout.addWidget(btn_plus)
    h_layout.addStretch() 
    
    layout.addLayout(h_layout)
    return spin