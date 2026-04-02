from PySide6 import QtWidgets, QtCore, QtGui
from ui_styles import *
from ui_helpers import create_step_control, add_touch_keyboard

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
    lbl_s_pfx.setStyleSheet("color: #ff5722; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    ui.lbl_speed = QtWidgets.QLabel("0.00")
    ui.lbl_speed.setStyleSheet("color: #ff5722; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_spd.addWidget(lbl_s_pfx)
    h_spd.addWidget(ui.lbl_speed)
    h_spd.addStretch()
    
    h_rpm = QtWidgets.QHBoxLayout()
    lbl_r_pfx = QtWidgets.QLabel("SPEED [m/min]: ")
    lbl_r_pfx.setStyleSheet("color: #4caf50; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    ui.lbl_rpm = QtWidgets.QLabel("0.00")
    ui.lbl_rpm.setStyleSheet("color: #4caf50; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
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
    ui.btn_manual.setFixedHeight(60)
    ui.btn_manual.setStyleSheet(MODE_BTN_STYLE)
    ui.btn_manual.setEnabled(False)
    ui.btn_manual.clicked.connect(ui.switch_to_manual)
    
    ui.btn_auto = QtWidgets.QPushButton("AUTO")
    ui.btn_auto.setCheckable(True)
    ui.btn_auto.setFixedHeight(60)
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
    
    # Wspólny styl dla małych przycisków APPLY
    small_apply_style = """
        QPushButton { background-color: #4CAF50; color: white; font-weight: bold; font-size: 16px; border-radius: 5px; }
        QPushButton:hover { background-color: #66BB6A; }
        QPushButton:pressed { background-color: #388E3C; }
        QPushButton:disabled { background-color: #333333; color: #666666; }
    """
    
    # ==========================================
    # ZAKŁADKA 1: BASIC CONTROL
    # ==========================================
    tab_basic = QtWidgets.QWidget()
    basic_layout = QtWidgets.QVBoxLayout(tab_basic)
    basic_layout.setContentsMargins(15, 15, 15, 15)
    
    inc_layout = QtWidgets.QHBoxLayout()
    lbl_inc = QtWidgets.QLabel("Step Increment:")
    lbl_inc.setFixedWidth(160) 
    lbl_inc.setStyleSheet("font-size: 20px; font-weight: bold; color: #cccccc;")
    
    ui.speed_inc = QtWidgets.QLineEdit("50")
    ui.speed_inc.setFixedSize(140, 70) 
    ui.speed_inc.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.speed_inc.setAlignment(QtCore.Qt.AlignCenter)
    ui.speed_inc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    ui.speed_inc.setValidator(QtGui.QIntValidator(MIN_SPEED_INC, MAX_SPEED_INC))
    add_touch_keyboard(ui.speed_inc)
    
    btn_inc_minus = QtWidgets.QPushButton("-")
    btn_inc_minus.setFixedSize(70, 70) 
    btn_inc_minus.setFont(QtGui.QFont("Segoe UI", 36, QtGui.QFont.Bold))
    btn_inc_minus.clicked.connect(lambda: ui.speed_inc.setText(str(max(MIN_SPEED_INC, int(ui.speed_inc.text() or 0) - 10))))
    
    btn_inc_plus = QtWidgets.QPushButton("+")
    btn_inc_plus.setFixedSize(70, 70) 
    btn_inc_plus.setFont(QtGui.QFont("Segoe UI", 36, QtGui.QFont.Bold))
    btn_inc_plus.clicked.connect(lambda: ui.speed_inc.setText(str(min(MAX_SPEED_INC, int(ui.speed_inc.text() or 0) + 10))))
    
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
    basic_layout.addStretch()
    
    # ==========================================
    # ZAKŁADKA 2: AUTO SETTINGS 
    # ==========================================
    tab_auto = QtWidgets.QWidget()
    auto_layout = QtWidgets.QVBoxLayout(tab_auto)
    auto_layout.setContentsMargins(15, 20, 15, 15)
    auto_layout.setSpacing(15)
    
    # 1. Pole Auto Calib Value (ZABLOKOWANE DO EDYCJI)
    auto_cal_layout = QtWidgets.QHBoxLayout()
    lbl_auto_cal = QtWidgets.QLabel("Auto Calib Value:")
    lbl_auto_cal.setFixedWidth(180)
    lbl_auto_cal.setStyleSheet("font-size: 20px; font-weight: bold; color: #cccccc;")
    
    ui.auto_cal_val = QtWidgets.QLineEdit("0.0000")
    ui.auto_cal_val.setFixedSize(220, 70)
    ui.auto_cal_val.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.auto_cal_val.setAlignment(QtCore.Qt.AlignCenter)
    ui.auto_cal_val.setReadOnly(True) # Odczyt tylko
    # Pociemniający styl dla pola read-only
    ui.auto_cal_val.setStyleSheet("background-color: #222222; color: #888888; border: 1px solid #333; border-radius: 5px;") 
    
    auto_cal_layout.addWidget(lbl_auto_cal)
    auto_cal_layout.addWidget(ui.auto_cal_val)
    auto_cal_layout.addStretch()
    
    # 2. Przyciski CALCULATE i LOAD
    btn_auto_layout = QtWidgets.QHBoxLayout()
    
    ui.btn_calc_auto = QtWidgets.QPushButton("CALCULATE")
    ui.btn_calc_auto.setFixedHeight(60)
    ui.btn_calc_auto.setStyleSheet("""
        QPushButton { background-color: #FF9800; color: white; font-weight: bold; font-size: 18px; border-radius: 8px; }
        QPushButton:hover { background-color: #FFB74D; }
        QPushButton:pressed { background-color: #F57C00; }
    """)
    
    ui.btn_load_auto = QtWidgets.QPushButton("LOAD TO GLUE CALIB")
    ui.btn_load_auto.setFixedHeight(60)
    ui.btn_load_auto.setStyleSheet("""
        QPushButton { background-color: #2196F3; color: white; font-weight: bold; font-size: 18px; border-radius: 8px; }
        QPushButton:hover { background-color: #42A5F5; }
        QPushButton:pressed { background-color: #1E88E5; }
    """)
    
    btn_auto_layout.addWidget(ui.btn_calc_auto)
    btn_auto_layout.addWidget(ui.btn_load_auto)
    
    # 3. Pole Glue Calibration + MAŁY PRZYCISK APPLY
    cal_layout = QtWidgets.QHBoxLayout()
    lbl_cal = QtWidgets.QLabel("Glue Calibration:")
    lbl_cal.setFixedWidth(180)
    lbl_cal.setStyleSheet("font-size: 20px; font-weight: bold; color: #cccccc;")
    
    ui.cal_glue = QtWidgets.QLineEdit("0.0000")
    ui.cal_glue.setFixedSize(220, 70)
    ui.cal_glue.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.cal_glue.setAlignment(QtCore.Qt.AlignCenter) 
    ui.cal_glue.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    regex_cal = QtCore.QRegularExpression(r"^[0-9]+(\.[0-9]{0,4})?$")
    ui.cal_glue.setValidator(QtGui.QRegularExpressionValidator(regex_cal))
    add_touch_keyboard(ui.cal_glue)
    
    ui.btn_apply_cal = QtWidgets.QPushButton("APPLY")
    ui.btn_apply_cal.setFixedSize(100, 70)
    ui.btn_apply_cal.setStyleSheet(small_apply_style)
    ui.btn_apply_cal.setEnabled(False)
    ui.btn_apply_cal.clicked.connect(lambda: ui.send_cmd(f"calGlue {ui.cal_glue.text()}"))
    
    cal_layout.addWidget(lbl_cal)
    cal_layout.addWidget(ui.cal_glue)
    cal_layout.addWidget(ui.btn_apply_cal)
    cal_layout.addStretch()
    
    auto_layout.addLayout(auto_cal_layout)
    auto_layout.addLayout(btn_auto_layout)
    auto_layout.addSpacing(15)
    auto_layout.addLayout(cal_layout)
    auto_layout.addStretch()

    # LOGIKA PRZYCISKÓW W ZAKŁADCE AUTO
    def calculate_auto_cal():
        try:
            rpm = float(ui.lbl_rpm.text())
            speed = float(ui.lbl_speed.text())
            if rpm != 0:
                val = speed / rpm
                ui.auto_cal_val.setText(f"{val:.4f}")
            else:
                ui.auto_cal_val.setText("0.0000")
        except ValueError:
            pass

    def load_auto_cal():
        ui.cal_glue.setText(ui.auto_cal_val.text())

    ui.btn_calc_auto.clicked.connect(calculate_auto_cal)
    ui.btn_load_auto.clicked.connect(load_auto_cal)

    # ==========================================
    # ZAKŁADKA 3: SETTINGS
    # ==========================================
    tab_adv = QtWidgets.QWidget()
    adv_layout = QtWidgets.QVBoxLayout(tab_adv)
    adv_layout.setContentsMargins(15, 20, 15, 15)
    adv_layout.setSpacing(15)
    
    # Pole Glue Acceleration + MAŁY PRZYCISK APPLY
    acc_layout = QtWidgets.QHBoxLayout()
    lbl_acc = QtWidgets.QLabel("Glue Acceleration:")
    lbl_acc.setFixedWidth(180)
    lbl_acc.setStyleSheet("font-size: 20px; font-weight: bold; color: #cccccc;")
    
    ui.glue_acc = QtWidgets.QLineEdit("0")
    ui.glue_acc.setFixedSize(220, 70)
    ui.glue_acc.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.glue_acc.setAlignment(QtCore.Qt.AlignCenter) 
    ui.glue_acc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    ui.glue_acc.setValidator(QtGui.QIntValidator(MIN_GLUE_ACC, MAX_GLUE_ACC))
    add_touch_keyboard(ui.glue_acc) 
    
    ui.btn_apply_acc = QtWidgets.QPushButton("APPLY")
    ui.btn_apply_acc.setFixedSize(100, 70)
    ui.btn_apply_acc.setStyleSheet(small_apply_style)
    ui.btn_apply_acc.setEnabled(False)
    ui.btn_apply_acc.clicked.connect(lambda: ui.send_cmd(f"glueAcc {ui.glue_acc.text() or 0}"))
    
    acc_layout.addWidget(lbl_acc)
    acc_layout.addWidget(ui.glue_acc)
    acc_layout.addWidget(ui.btn_apply_acc)
    acc_layout.addStretch()
    
    adv_layout.addLayout(acc_layout)
    adv_layout.addSpacing(80) 
    adv_layout.addStretch()
    
    # --- Dodanie zakładek we właściwej kolejności ---
    ui.tabs.addTab(tab_basic, "Basic Control")
    ui.tabs.addTab(tab_auto, "Auto Settings")
    ui.tabs.addTab(tab_adv, "Settings")
    col1_layout.addWidget(ui.tabs)

    # ==========================================
    # POZA ZAKŁADKAMI: PRZYCISK STOP MOTOR
    # ==========================================
    ui.btn_motor_stop = QtWidgets.QPushButton("STOP MOTOR")
    ui.btn_motor_stop.setFixedHeight(140)
    ui.btn_motor_stop.setStyleSheet(STOP_BTN_STYLE)
    ui.btn_motor_stop.setEnabled(False)
    ui.btn_motor_stop.clicked.connect(ui.stop_motor) 
    col1_layout.addWidget(ui.btn_motor_stop)

    col1.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
    parent_layout.addWidget(col1, 1)