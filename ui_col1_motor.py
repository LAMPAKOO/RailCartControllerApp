from PySide6 import QtWidgets, QtCore, QtGui
from ui_styles import *
from ui_helpers import create_step_control

def setup_motor_column(ui, parent_layout):
    col1 = QtWidgets.QFrame()
    col1.setObjectName("MainPanel")
    col1.setStyleSheet(PANEL_STYLE)
    col1_layout = QtWidgets.QVBoxLayout(col1)
    col1_layout.setAlignment(QtCore.Qt.AlignTop) 
    col1_layout.setContentsMargins(15, 15, 15, 15)
    col1_layout.setSpacing(15)
    
    lbl_title_1 = QtWidgets.QLabel("GLUE CONTROL")
    lbl_title_1.setStyleSheet(HEADER_STYLE)
    col1_layout.addWidget(lbl_title_1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    disp1 = QtWidgets.QFrame()
    disp1.setObjectName("DisplayPanel")
    disp1.setStyleSheet(DISPLAY_STYLE)
    disp1_layout = QtWidgets.QVBoxLayout(disp1)
    disp1_layout.setContentsMargins(20, 20, 20, 20)
    disp1_layout.setSpacing(15)
    
    h_spd = QtWidgets.QHBoxLayout()
    lbl_s_pfx = QtWidgets.QLabel("GLUE: ")
    lbl_s_pfx.setStyleSheet("color: #ff5722; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    ui.lbl_speed = QtWidgets.QLabel("0.00")
    ui.lbl_speed.setStyleSheet("color: #ff5722; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_spd.addWidget(lbl_s_pfx)
    h_spd.addWidget(ui.lbl_speed)
    h_spd.addStretch()
    
    h_rpm = QtWidgets.QHBoxLayout()
    lbl_r_pfx = QtWidgets.QLabel("SPEED [m/min]: ")
    lbl_r_pfx.setStyleSheet("color: #4caf50; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    ui.lbl_rpm = QtWidgets.QLabel("0.00")
    ui.lbl_rpm.setStyleSheet("color: #4caf50; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_rpm.addWidget(lbl_r_pfx)
    h_rpm.addWidget(ui.lbl_rpm)
    h_rpm.addStretch()
    
    disp1_layout.addLayout(h_spd)
    disp1_layout.addLayout(h_rpm)
    col1_layout.addWidget(disp1)
    
    mode_h = QtWidgets.QHBoxLayout()
    mode_h.setSpacing(10)
    
    ui.btn_manual = QtWidgets.QPushButton("MANUAL")
    ui.btn_manual.setCheckable(True)
    ui.btn_manual.setChecked(True)
    ui.btn_manual.setFixedHeight(45)
    ui.btn_manual.setStyleSheet(MODE_BTN_STYLE)
    ui.btn_manual.setEnabled(False)
    ui.btn_manual.clicked.connect(ui.switch_to_manual)
    
    ui.btn_auto = QtWidgets.QPushButton("AUTO")
    ui.btn_auto.setCheckable(True)
    ui.btn_auto.setFixedHeight(45)
    ui.btn_auto.setStyleSheet(MODE_BTN_STYLE)
    ui.btn_auto.setEnabled(False)
    ui.btn_auto.clicked.connect(ui.switch_to_auto)
    
    ui.mode_btn_group = QtWidgets.QButtonGroup()
    ui.mode_btn_group.addButton(ui.btn_manual)
    ui.mode_btn_group.addButton(ui.btn_auto)
    
    mode_h.addWidget(ui.btn_manual)
    mode_h.addWidget(ui.btn_auto)
    col1_layout.addLayout(mode_h)
    
    ui.tabs = QtWidgets.QTabWidget()
    ui.tabs.setStyleSheet(TABS_STYLE)
    
    # ==========================================
    # ZAKŁADKA BASIC
    # ==========================================
    tab_basic = QtWidgets.QWidget()
    basic_layout = QtWidgets.QVBoxLayout(tab_basic)
    basic_layout.setContentsMargins(15, 15, 15, 15)
    
    inc_layout = QtWidgets.QHBoxLayout()
    lbl_inc = QtWidgets.QLabel("Step Increment:")
    lbl_inc.setFixedWidth(140) 
    lbl_inc.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    
    ui.speed_inc = QtWidgets.QLineEdit("50")
    ui.speed_inc.setFixedSize(120, 50) 
    ui.speed_inc.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    ui.speed_inc.setAlignment(QtCore.Qt.AlignCenter)
    ui.speed_inc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    ui.speed_inc.setValidator(QtGui.QIntValidator(1, 1000))
    
    btn_inc_minus = QtWidgets.QPushButton("-")
    btn_inc_minus.setFixedSize(50, 50) 
    btn_inc_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_inc_minus.clicked.connect(lambda: ui.speed_inc.setText(str(max(1, int(ui.speed_inc.text() or 0) - 10))))
    
    btn_inc_plus = QtWidgets.QPushButton("+")
    btn_inc_plus.setFixedSize(50, 50) 
    btn_inc_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_inc_plus.clicked.connect(lambda: ui.speed_inc.setText(str(min(1000, int(ui.speed_inc.text() or 0) + 10))))
    
    inc_layout.addWidget(lbl_inc)
    inc_layout.addWidget(btn_inc_minus)
    inc_layout.addWidget(ui.speed_inc)
    inc_layout.addWidget(btn_inc_plus)
    inc_layout.addStretch()
    basic_layout.addLayout(inc_layout)
    
    ui.fwd_speed = create_step_control(ui, basic_layout, "Dispense Speed:", "forwardSpeed")
    ui.bwd_speed = create_step_control(ui, basic_layout, "Retract Speed:", "backwardSpeed")
    
    basic_layout.addSpacing(15)
    
    move_layout = QtWidgets.QHBoxLayout()
    move_layout.setSpacing(15)
    
    ui.btn_glue_fwd = QtWidgets.QPushButton("▲\nDISPENSE GLUE")
    ui.btn_glue_fwd.setFixedHeight(140) 
    ui.btn_glue_fwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    ui.btn_glue_fwd.setStyleSheet(MOVE_BTN_STYLE)
    ui.btn_glue_fwd.setEnabled(False)
    ui.btn_glue_fwd.clicked.connect(ui.start_dispense)
    
    ui.btn_glue_bwd = QtWidgets.QPushButton("▼\nRETRACT")
    ui.btn_glue_bwd.setFixedHeight(140) 
    ui.btn_glue_bwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    ui.btn_glue_bwd.setStyleSheet(MOVE_BTN_STYLE)
    ui.btn_glue_bwd.setEnabled(False)
    ui.btn_glue_bwd.clicked.connect(ui.start_retract)
    
    move_layout.addWidget(ui.btn_glue_fwd, 1)
    move_layout.addWidget(ui.btn_glue_bwd, 1)
    basic_layout.addLayout(move_layout)
    
    ui.btn_motor_stop = QtWidgets.QPushButton("STOP MOTOR")
    ui.btn_motor_stop.setFixedHeight(60)
    ui.btn_motor_stop.setStyleSheet(STOP_BTN_STYLE)
    ui.btn_motor_stop.setEnabled(False)
    ui.btn_motor_stop.clicked.connect(ui.stop_motor) 
    basic_layout.addWidget(ui.btn_motor_stop)
    
    basic_layout.addStretch()
    
    # ==========================================
    # ZAKŁADKA ADVANCED / SETTINGS
    # ==========================================
    tab_adv = QtWidgets.QWidget()
    adv_layout = QtWidgets.QVBoxLayout(tab_adv)
    adv_layout.setContentsMargins(15, 20, 15, 15)
    adv_layout.setSpacing(15)
    
    # --- Sekcja Glue Acceleration ---
    acc_layout = QtWidgets.QHBoxLayout()
    lbl_acc = QtWidgets.QLabel("Glue Acceleration:")
    lbl_acc.setFixedWidth(160)
    lbl_acc.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    
    ui.glue_acc = QtWidgets.QLineEdit("0")
    ui.glue_acc.setFixedSize(180, 50)
    ui.glue_acc.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    ui.glue_acc.setAlignment(QtCore.Qt.AlignCenter) # Tekst na środku
    ui.glue_acc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    
    # Walidator dla liczb całkowitych (od 0 do miliona)
    ui.glue_acc.setValidator(QtGui.QIntValidator(0, 1000000))
    
    acc_layout.addWidget(lbl_acc)
    acc_layout.addWidget(ui.glue_acc)
    acc_layout.addStretch()
    
    # --- Sekcja Glue Calibration ---
    cal_layout = QtWidgets.QHBoxLayout()
    lbl_cal = QtWidgets.QLabel("Glue Calibration:")
    lbl_cal.setFixedWidth(160)
    lbl_cal.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
    
    ui.cal_glue = QtWidgets.QLineEdit("0.0000")
    ui.cal_glue.setFixedSize(180, 50)
    ui.cal_glue.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    ui.cal_glue.setAlignment(QtCore.Qt.AlignCenter) # Tekst na środku
    ui.cal_glue.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    
    # Zabezpieczenie: Walidator Regex pozwalający na ułamek TYLKO z kropką (np. 1.2345)
    regex_cal = QtCore.QRegularExpression(r"^[0-9]+(\.[0-9]{0,4})?$")
    ui.cal_glue.setValidator(QtGui.QRegularExpressionValidator(regex_cal))
    
    cal_layout.addWidget(lbl_cal)
    cal_layout.addWidget(ui.cal_glue)
    cal_layout.addStretch()
    
    adv_layout.addLayout(acc_layout)
    adv_layout.addLayout(cal_layout)
    adv_layout.addSpacing(20)
    
    # --- Przyciski Apply / Refresh ---
    btn_apply = QtWidgets.QPushButton("APPLY ALL PARAMETERS")
    btn_apply.setFixedHeight(60)
    btn_apply.setStyleSheet("""
        QPushButton { background-color: #4CAF50; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; }
        QPushButton:hover { background-color: #66BB6A; }
        QPushButton:pressed { background-color: #388E3C; }
    """)
    btn_apply.clicked.connect(ui.apply_all)
    
    btn_read = QtWidgets.QPushButton("REFRESH FROM NVS")
    btn_read.setFixedHeight(60)
    btn_read.setStyleSheet("""
        QPushButton { background-color: #2196F3; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; }
        QPushButton:hover { background-color: #42A5F5; }
        QPushButton:pressed { background-color: #1976D2; }
    """)
    btn_read.clicked.connect(ui.read_nvs)
    
    adv_layout.addWidget(btn_apply)
    adv_layout.addWidget(btn_read)
    adv_layout.addStretch()
    
    ui.tabs.addTab(tab_basic, "Basic Control")
    ui.tabs.addTab(tab_adv, "Settings")
    col1_layout.addWidget(ui.tabs)

    parent_layout.addWidget(col1, 1)