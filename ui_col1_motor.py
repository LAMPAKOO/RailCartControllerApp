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
    lbl_r_pfx = QtWidgets.QLabel("SPEED [m/h]: ")
    lbl_r_pfx.setStyleSheet("color: #4caf50; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    ui.lbl_rpm = QtWidgets.QLabel("0.00")
    ui.lbl_rpm.setStyleSheet("color: #4caf50; font-size: 40px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_rpm.addWidget(lbl_r_pfx)
    h_rpm.addWidget(ui.lbl_rpm)
    h_rpm.addStretch()
    
    disp1_layout.addLayout(h_spd)
    disp1_layout.addLayout(h_rpm)
    col1_layout.addWidget(disp1)
    
    # --- PRZYCISKI TRYBÓW ZOSTAŁY USUNIĘTE ---
    
    ui.tabs = QtWidgets.QTabWidget()
    ui.tabs.setStyleSheet(TABS_STYLE)
    
    # Wspólne style
    perc_btn_style = """
        QPushButton { background-color: #444444; color: white; font-weight: bold; border-radius: 5px; }
        QPushButton:hover { background-color: #555555; }
        QPushButton:pressed { background-color: #2196F3; }
    """
    large_apply_style = """
        QPushButton { background-color: #4CAF50; color: white; font-weight: bold; font-size: 20px; border-radius: 8px; }
        QPushButton:hover { background-color: #66BB6A; }
        QPushButton:pressed { background-color: #388E3C; }
        QPushButton:disabled { background-color: #333333; color: #666666; }
    """
    
    # ==========================================
    # ZAKŁADKA 1: MANUAL 
    # ==========================================
    tab_basic = QtWidgets.QWidget()
    basic_layout = QtWidgets.QVBoxLayout(tab_basic)
    basic_layout.setContentsMargins(15, 15, 15, 15)
    
    inc_layout = QtWidgets.QHBoxLayout()
    lbl_inc = QtWidgets.QLabel("STEP INCREMENT:")
    lbl_inc.setFixedWidth(220) 
    lbl_inc.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
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
    
    ui.fwd_speed = create_step_control(ui, basic_layout, "DISPENSE SPEED:", "forwardSpeed")
    ui.bwd_speed = create_step_control(ui, basic_layout, "RETRACT SPEED:", "backwardSpeed")
    
    basic_layout.addSpacing(15)

    # --- NOWE: SEKCJA AUTO CALIB W ZAKŁADCE MANUAL ---
    auto_cal_layout = QtWidgets.QHBoxLayout()
    lbl_auto_cal = QtWidgets.QLabel("AUTO CALIB:")
    lbl_auto_cal.setFixedWidth(220)
    lbl_auto_cal.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
    ui.auto_cal_val = QtWidgets.QLineEdit("0.000")
    ui.auto_cal_val.setFixedSize(160, 70)
    ui.auto_cal_val.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.auto_cal_val.setAlignment(QtCore.Qt.AlignCenter)
    ui.auto_cal_val.setReadOnly(True) 
    ui.auto_cal_val.setStyleSheet("background-color: #222222; color: #888888; border: 1px solid #333; border-radius: 5px;") 
    
    ui.btn_load_auto = QtWidgets.QPushButton("LOAD & APPLY")
    ui.btn_load_auto.setFixedSize(140, 70)
    ui.btn_load_auto.setStyleSheet("""
        QPushButton { background-color: #2196F3; color: white; font-weight: bold; font-size: 16px; border-radius: 5px; }
        QPushButton:hover { background-color: #42A5F5; }
        QPushButton:pressed { background-color: #1E88E5; }
    """)
    
    auto_cal_layout.addWidget(lbl_auto_cal)
    auto_cal_layout.addWidget(ui.auto_cal_val)
    auto_cal_layout.addWidget(ui.btn_load_auto)
    auto_cal_layout.addStretch()
    
    basic_layout.addLayout(auto_cal_layout)
    basic_layout.addSpacing(15)
    # -------------------------------------------------
    
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
    # ZAKŁADKA 2: AUTO 
    # ==========================================
    tab_auto = QtWidgets.QWidget()
    auto_layout = QtWidgets.QVBoxLayout(tab_auto)
    auto_layout.setContentsMargins(15, 20, 15, 15)
    auto_layout.setSpacing(15)
    
    # 1. Pole Percent Increment
    perc_layout = QtWidgets.QHBoxLayout()
    lbl_perc = QtWidgets.QLabel("INCREMENT [%]:")
    lbl_perc.setFixedWidth(220) 
    lbl_perc.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
    ui.btn_perc_step_minus = QtWidgets.QPushButton("-")
    ui.btn_perc_step_minus.setFixedSize(80, 70)
    ui.btn_perc_step_minus.setFont(QtGui.QFont("Segoe UI", 36, QtGui.QFont.Bold))
    ui.btn_perc_step_minus.setStyleSheet(perc_btn_style)

    ui.perc_inc = QtWidgets.QLineEdit("5")
    ui.perc_inc.setFixedSize(160, 70)
    ui.perc_inc.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.perc_inc.setAlignment(QtCore.Qt.AlignCenter)
    ui.perc_inc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    ui.perc_inc.setValidator(QtGui.QIntValidator(1, 100))
    add_touch_keyboard(ui.perc_inc)
    
    ui.btn_perc_step_plus = QtWidgets.QPushButton("+")
    ui.btn_perc_step_plus.setFixedSize(80, 70)
    ui.btn_perc_step_plus.setFont(QtGui.QFont("Segoe UI", 36, QtGui.QFont.Bold))
    ui.btn_perc_step_plus.setStyleSheet(perc_btn_style)

    perc_layout.addWidget(lbl_perc)
    perc_layout.addWidget(ui.btn_perc_step_minus)
    perc_layout.addWidget(ui.perc_inc)
    perc_layout.addWidget(ui.btn_perc_step_plus)
    perc_layout.addStretch()
    
    # 2. Pole Glue Calibration 
    cal_layout = QtWidgets.QHBoxLayout()
    lbl_cal = QtWidgets.QLabel("GLUE CALIB:")
    lbl_cal.setFixedWidth(220)
    lbl_cal.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
    ui.btn_perc_minus = QtWidgets.QPushButton("-%")
    ui.btn_perc_minus.setFixedSize(80, 70)
    ui.btn_perc_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.btn_perc_minus.setStyleSheet(perc_btn_style)

    ui.cal_glue = QtWidgets.QLineEdit("0.000")
    ui.cal_glue.setFixedSize(160, 70)
    ui.cal_glue.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
    ui.cal_glue.setAlignment(QtCore.Qt.AlignCenter) 
    ui.cal_glue.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    regex_cal = QtCore.QRegularExpression(r"^[0-9]*(\.[0-9]{0,3})?$")
    ui.cal_glue.setValidator(QtGui.QRegularExpressionValidator(regex_cal))
    add_touch_keyboard(ui.cal_glue)
    
    ui.btn_perc_plus = QtWidgets.QPushButton("+%")
    ui.btn_perc_plus.setFixedSize(80, 70)
    ui.btn_perc_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.btn_perc_plus.setStyleSheet(perc_btn_style)

    cal_layout.addWidget(lbl_cal)
    cal_layout.addWidget(ui.btn_perc_minus)
    cal_layout.addWidget(ui.cal_glue)
    cal_layout.addWidget(ui.btn_perc_plus)
    cal_layout.addStretch()
    
    ui.btn_apply_cal = QtWidgets.QPushButton("APPLY CALIBRATION")
    ui.btn_apply_cal.setFixedHeight(80)
    ui.btn_apply_cal.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    ui.btn_apply_cal.setStyleSheet(large_apply_style)
    ui.btn_apply_cal.setEnabled(False)
    ui.btn_apply_cal.clicked.connect(lambda: ui.send_cmd(f"calGlue {ui.cal_glue.text()}"))
    
    auto_layout.addLayout(perc_layout)
    auto_layout.addLayout(cal_layout)
    auto_layout.addSpacing(10)
    auto_layout.addWidget(ui.btn_apply_cal) 
    auto_layout.addStretch()

    # LOGIKA PRZYCISKÓW I ZEGARA
    # LOGIKA PRZYCISKÓW I ZEGARA
    def calculate_auto_cal():
        try:
            # Pobieramy HZ z wyświetlacza falownika (zamiast lbl_rpm)
            hz = float(ui.lbl_vfd_freq.text())
            speed = float(ui.lbl_speed.text())
            
            # Zabezpieczenie przed dzieleniem przez zero (gdy silnik stoi)
            if hz != 0:
                val = abs(speed / hz) 
                ui.auto_cal_val.setText(f"{val:.3f}")
            else:
                ui.auto_cal_val.setText("0.000")
        # Wyłapujemy też AttributeError na wypadek, gdyby widget lbl_vfd_freq jeszcze się nie załadował
        except (ValueError, AttributeError):
            pass

    ui.auto_cal_timer = QtCore.QTimer(ui)
    ui.auto_cal_timer.timeout.connect(calculate_auto_cal)
    ui.auto_cal_timer.start(200)

    def load_and_apply_auto_cal():
        val = ui.auto_cal_val.text()
        ui.cal_glue.setText(val)
        try:
            ui.exact_cal_value = float(val) 
        except ValueError:
            pass
        ui.send_cmd(f"calGlue {val}")

    def adjust_cal_perc(is_plus):
        try:
            displayed_val = float(ui.cal_glue.text() or 0)
            saved_exact = getattr(ui, 'exact_cal_value', displayed_val)
            
            if abs(displayed_val - round(saved_exact, 2)) > 0.001:
                current_cal = displayed_val
            else:
                current_cal = saved_exact

            perc_val = float(ui.perc_inc.text() or 0)
            factor = 1.0 + (perc_val / 100.0)

            if is_plus:
                new_cal = current_cal * factor
            else:
                new_cal = current_cal / factor
            
            ui.exact_cal_value = new_cal
            ui.send_cmd(f"calGlue {new_cal:.4f}")
            ui.cal_glue.setText(f"{new_cal:.3f}")
            
        except ValueError:
            pass

    def step_perc_val(delta):
        try:
            val = int(ui.perc_inc.text() or 0)
            new_val = max(1, min(100, val + delta))
            ui.perc_inc.setText(str(new_val))
        except ValueError:
            pass

    ui.btn_load_auto.clicked.connect(load_and_apply_auto_cal)
    ui.btn_perc_minus.clicked.connect(lambda: adjust_cal_perc(False))
    ui.btn_perc_plus.clicked.connect(lambda: adjust_cal_perc(True))
    ui.btn_perc_step_minus.clicked.connect(lambda: step_perc_val(-1))
    ui.btn_perc_step_plus.clicked.connect(lambda: step_perc_val(1))

    # ==========================================
    # ZAKŁADKA 3: SETTINGS
    # ==========================================
    tab_adv = QtWidgets.QWidget()
    adv_layout = QtWidgets.QVBoxLayout(tab_adv)
    adv_layout.setContentsMargins(15, 20, 15, 15)
    adv_layout.setSpacing(15)
    
    # 1. Pole Glue Acceleration
    acc_layout = QtWidgets.QHBoxLayout()
    lbl_acc = QtWidgets.QLabel("GLUE ACC:")
    lbl_acc.setFixedWidth(220)
    lbl_acc.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
    ui.glue_acc = QtWidgets.QLineEdit("0")
    ui.glue_acc.setFixedSize(220, 70)
    ui.glue_acc.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.glue_acc.setAlignment(QtCore.Qt.AlignCenter) 
    ui.glue_acc.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    ui.glue_acc.setValidator(QtGui.QIntValidator(MIN_GLUE_ACC, MAX_GLUE_ACC))
    add_touch_keyboard(ui.glue_acc) 
    
    ui.btn_apply_acc = QtWidgets.QPushButton("APPLY")
    ui.btn_apply_acc.setFixedSize(100, 70)
    ui.btn_apply_acc.setStyleSheet(large_apply_style) 
    ui.btn_apply_acc.setEnabled(False)
    ui.btn_apply_acc.clicked.connect(lambda: ui.send_cmd(f"glueAcc {ui.glue_acc.text() or 0}"))
    
    acc_layout.addWidget(lbl_acc)
    acc_layout.addWidget(ui.glue_acc)
    acc_layout.addWidget(ui.btn_apply_acc) 
    acc_layout.addStretch()

    # 2. Pole FILTER VALUE 
    filter_layout = QtWidgets.QHBoxLayout()
    lbl_filter = QtWidgets.QLabel("FILTER VALUE:")
    lbl_filter.setFixedWidth(220)
    lbl_filter.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
    
    ui.filter_alpha = QtWidgets.QLineEdit("0.200")
    ui.filter_alpha.setFixedSize(220, 70)
    ui.filter_alpha.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    ui.filter_alpha.setAlignment(QtCore.Qt.AlignCenter)
    ui.filter_alpha.setStyleSheet("background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px;")
    
    regex_filter = QtCore.QRegularExpression(r"^(0?(\.\d{0,3})?|1(\.0{0,3})?)$")
    ui.filter_alpha.setValidator(QtGui.QRegularExpressionValidator(regex_filter))
    add_touch_keyboard(ui.filter_alpha)
    
    ui.btn_apply_filter = QtWidgets.QPushButton("APPLY")
    ui.btn_apply_filter.setFixedSize(100, 70)
    ui.btn_apply_filter.setStyleSheet(large_apply_style) 
    ui.btn_apply_filter.setEnabled(False)
    ui.btn_apply_filter.clicked.connect(lambda: ui.send_cmd(f"filterAlpha {ui.filter_alpha.text()}"))
    
    filter_layout.addWidget(lbl_filter)
    filter_layout.addWidget(ui.filter_alpha)
    filter_layout.addWidget(ui.btn_apply_filter)
    filter_layout.addStretch()
    
    adv_layout.addLayout(acc_layout)
    adv_layout.addLayout(filter_layout) 
    adv_layout.addStretch()

    # --- NOWOŚĆ: Logika przełączania trybów zakładkami ---
    ui.tabs.addTab(tab_basic, "MANUAL")
    ui.tabs.addTab(tab_auto, "AUTO")
    ui.tabs.addTab(tab_adv, "SETTINGS")
    
    def on_tab_changed(index):
        if index == 0:
            ui.switch_to_manual()
        elif index == 1:
            ui.switch_to_auto()
            
    ui.tabs.currentChanged.connect(on_tab_changed)
    col1_layout.addWidget(ui.tabs)

    # ==========================================
    # POZA ZAKŁADKAMI: PRZYCISK STOP MOTOR
    # ==========================================
    ui.btn_motor_stop = QtWidgets.QPushButton("STOP GLUE")
    ui.btn_motor_stop.setFixedHeight(140)
    ui.btn_motor_stop.setStyleSheet(STOP_BTN_STYLE)
    ui.btn_motor_stop.setEnabled(False)
    ui.btn_motor_stop.clicked.connect(ui.stop_motor) 
    col1_layout.addWidget(ui.btn_motor_stop)

    col1.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
    parent_layout.addWidget(col1, 1)