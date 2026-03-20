import os
from PySide6 import QtWidgets, QtCore, QtGui

# Klasa-zaślepka chroniąca przed błędami logicznymi przy próbie aktualizacji usuniętego wykresu
class DummyCurve:
    def setData(self, *args, **kwargs):
        pass

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
        
        # =========================================================
        # STYLE WIELOKROTNEGO UŻYTKU
        # =========================================================
        panel_style = "#MainPanel { background-color: #2b2b2b; border: 1px solid #3c3c3c; border-radius: 8px; }"
        display_style = "#DisplayPanel { background-color: #141414; border-radius: 5px; border: 1px solid #1f1f1f; }"
        header_style = "color: #00E5FF; font-size: 18px; font-weight: bold; font-family: 'Segoe UI', Arial, sans-serif; background: transparent; margin-bottom: 5px;"
        input_style = "background-color: #333333; color: white; border: 1px solid #444; border-radius: 3px; padding: 6px; font-size: 14px;"
        label_style = "color: #aaaaaa; background: transparent; font-size: 12px;"
        
        move_btn_style = """
            QPushButton { 
                font-size: 20px; 
                font-weight: bold; 
                background-color: #444444; 
                color: white; 
                border-radius: 8px; 
            }
            QPushButton:hover { background-color: #555555; }
            QPushButton:pressed { background-color: #2196F3; }
        """

        # =========================================================
        # KOLUMNA 1: OBSŁUGA SILNIKA
        # =========================================================
        col1 = QtWidgets.QFrame()
        col1.setObjectName("MainPanel")
        col1.setStyleSheet(panel_style)
        col1_layout = QtWidgets.QVBoxLayout(col1)
        col1_layout.setAlignment(QtCore.Qt.AlignTop) 
        col1_layout.setContentsMargins(15, 15, 15, 15)
        col1_layout.setSpacing(15)
        
        lbl_title_1 = QtWidgets.QLabel("MOTOR CONTROL")
        lbl_title_1.setStyleSheet(header_style)
        col1_layout.addWidget(lbl_title_1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        
        disp1 = QtWidgets.QFrame()
        disp1.setObjectName("DisplayPanel")
        disp1.setStyleSheet(display_style)
        disp1_layout = QtWidgets.QVBoxLayout(disp1)
        disp1_layout.setContentsMargins(20, 20, 20, 20)
        disp1_layout.setSpacing(15)
        
        h_spd = QtWidgets.QHBoxLayout()
        lbl_s_pfx = QtWidgets.QLabel("SPEED: ")
        lbl_s_pfx.setStyleSheet("color: #ff5722; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        self.lbl_speed = QtWidgets.QLabel("0.00")
        self.lbl_speed.setStyleSheet("color: #ff5722; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        h_spd.addWidget(lbl_s_pfx)
        h_spd.addWidget(self.lbl_speed)
        h_spd.addStretch()
        
        h_rpm = QtWidgets.QHBoxLayout()
        lbl_r_pfx = QtWidgets.QLabel("RPM: ")
        lbl_r_pfx.setStyleSheet("color: #4caf50; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        self.lbl_rpm = QtWidgets.QLabel("0.00")
        self.lbl_rpm.setStyleSheet("color: #4caf50; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        h_rpm.addWidget(lbl_r_pfx)
        h_rpm.addWidget(self.lbl_rpm)
        h_rpm.addStretch()
        
        disp1_layout.addLayout(h_spd)
        disp1_layout.addLayout(h_rpm)
        col1_layout.addWidget(disp1)
        
        mode_h = QtWidgets.QHBoxLayout()
        mode_h.setSpacing(10)
        mode_btn_style_col1 = """
            QPushButton { font-size: 16px; font-weight: bold; background-color: #444444; color: white; border-radius: 5px; border: none; }
            QPushButton:checked { background-color: #2196F3; color: white; }
        """
        
        self.btn_manual = QtWidgets.QPushButton("MANUAL")
        self.btn_manual.setCheckable(True)
        self.btn_manual.setChecked(True)
        self.btn_manual.setFixedHeight(45)
        self.btn_manual.setStyleSheet(mode_btn_style_col1)
        self.btn_manual.clicked.connect(self.switch_to_manual)
        
        self.btn_auto = QtWidgets.QPushButton("AUTO")
        self.btn_auto.setCheckable(True)
        self.btn_auto.setFixedHeight(45)
        self.btn_auto.setStyleSheet(mode_btn_style_col1)
        self.btn_auto.clicked.connect(lambda: self.send_cmd("MODE_AUTO"))
        
        self.mode_btn_group = QtWidgets.QButtonGroup()
        self.mode_btn_group.addButton(self.btn_manual)
        self.mode_btn_group.addButton(self.btn_auto)
        
        mode_h.addWidget(self.btn_manual)
        mode_h.addWidget(self.btn_auto)
        col1_layout.addLayout(mode_h)
        
        self.tabs = QtWidgets.QTabWidget()
        
        tab_basic = QtWidgets.QWidget()
        basic_layout = QtWidgets.QVBoxLayout(tab_basic)
        
        inc_layout = QtWidgets.QHBoxLayout()
        
        lbl_inc = QtWidgets.QLabel("Step Increment:")
        lbl_inc.setFixedWidth(140) 
        lbl_inc.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
        
        self.speed_inc = QtWidgets.QSpinBox()
        self.speed_inc.setRange(10, 1000)
        self.speed_inc.setValue(50)
        self.speed_inc.setFixedSize(120, 50) 
        self.speed_inc.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        
        btn_inc_minus = QtWidgets.QPushButton("-")
        btn_inc_minus.setFixedSize(50, 50) 
        btn_inc_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_inc_minus.clicked.connect(lambda: self.speed_inc.setValue(self.speed_inc.value() - 10))
        
        btn_inc_plus = QtWidgets.QPushButton("+")
        btn_inc_plus.setFixedSize(50, 50) 
        btn_inc_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_inc_plus.clicked.connect(lambda: self.speed_inc.setValue(self.speed_inc.value() + 10))
        
        inc_layout.addWidget(lbl_inc)
        inc_layout.addWidget(btn_inc_minus)
        inc_layout.addWidget(self.speed_inc)
        inc_layout.addWidget(btn_inc_plus)
        inc_layout.addStretch()
        basic_layout.addLayout(inc_layout)
        
        self.fwd_speed = self.create_step_control(basic_layout, "Forward Speed:", "forwardSpeed")
        self.bwd_speed = self.create_step_control(basic_layout, "Backward Speed:", "backwardSpeed")
        
        basic_layout.addSpacing(15)
        
        move_layout = QtWidgets.QHBoxLayout()
        move_layout.setSpacing(15)
        
        btn_fwd = QtWidgets.QPushButton("▲\nMOVE FWD")
        btn_fwd.setFixedHeight(140) 
        btn_fwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        btn_fwd.setStyleSheet(move_btn_style)
        btn_fwd.clicked.connect(lambda: self.send_cmd("MOVE_FORWARD"))
        
        btn_bwd = QtWidgets.QPushButton("▼\nMOVE BWD")
        btn_bwd.setFixedHeight(140) 
        btn_bwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        btn_bwd.setStyleSheet(move_btn_style)
        btn_bwd.clicked.connect(lambda: self.send_cmd("MOVE_BACKWARD"))
        
        move_layout.addWidget(btn_fwd, 1)
        move_layout.addWidget(btn_bwd, 1)
        basic_layout.addLayout(move_layout)
        
        self.btn_motor_stop = QtWidgets.QPushButton("STOP MOTOR")
        self.btn_motor_stop.setFixedHeight(60)
        self.btn_motor_stop.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; font-size: 18px; border-radius: 8px; margin-top: 10px;")
        self.btn_motor_stop.clicked.connect(lambda: self.send_cmd("STOP"))
        basic_layout.addWidget(self.btn_motor_stop)
        
        basic_layout.addStretch()
        
        tab_adv = QtWidgets.QWidget()
        adv_layout = QtWidgets.QVBoxLayout(tab_adv)
        
        self.glue_acc = QtWidgets.QSpinBox()
        self.glue_acc.setRange(0, 1000000); self.glue_acc.setFixedHeight(30)
        self.cal_glue = QtWidgets.QLineEdit("0.0000"); self.cal_glue.setFixedHeight(30)
        
        adv_layout.addWidget(QtWidgets.QLabel("Glue Acceleration:"))
        adv_layout.addWidget(self.glue_acc)
        adv_layout.addWidget(QtWidgets.QLabel("Glue Calibration:"))
        adv_layout.addWidget(self.cal_glue)
        
        btn_apply = QtWidgets.QPushButton("Apply All Parameters")
        btn_apply.clicked.connect(self.apply_all)
        btn_read = QtWidgets.QPushButton("Refresh from NVS")
        btn_read.clicked.connect(self.read_nvs)
        
        adv_layout.addWidget(btn_apply); adv_layout.addWidget(btn_read); adv_layout.addStretch()
        
        self.tabs.addTab(tab_basic, "Basic Control")
        self.tabs.addTab(tab_adv, "Settings")
        col1_layout.addWidget(self.tabs)

        # =========================================================
        # KOLUMNA 2: FALOWNIK (INVERTER)
        # =========================================================
        col2 = QtWidgets.QFrame()
        col2.setObjectName("MainPanel")
        col2.setStyleSheet(panel_style)
        col2_layout = QtWidgets.QVBoxLayout(col2)
        col2_layout.setAlignment(QtCore.Qt.AlignTop)
        col2_layout.setContentsMargins(15, 15, 15, 15)
        col2_layout.setSpacing(15)
        
        lbl_title_2 = QtWidgets.QLabel("INVERTER CONTROL")
        lbl_title_2.setStyleSheet(header_style)
        col2_layout.addWidget(lbl_title_2, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        
        disp2 = QtWidgets.QFrame()
        disp2.setObjectName("DisplayPanel")
        disp2.setStyleSheet(display_style)
        disp2_layout = QtWidgets.QHBoxLayout(disp2)
        disp2_layout.setContentsMargins(20, 20, 20, 20)
        disp2_layout.setSpacing(15)
        
        lbl_freq_pfx = QtWidgets.QLabel("FREQ: ")
        lbl_freq_pfx.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        
        self.lbl_vfd_freq = QtWidgets.QLabel("0.00")
        self.lbl_vfd_freq.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        
        lbl_freq_sfx = QtWidgets.QLabel(" Hz")
        lbl_freq_sfx.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        
        disp2_layout.addWidget(lbl_freq_pfx)
        disp2_layout.addWidget(self.lbl_vfd_freq)
        disp2_layout.addWidget(lbl_freq_sfx)
        disp2_layout.addStretch()
        col2_layout.addWidget(disp2)
        
        vfd_container = QtWidgets.QWidget()
        vfd_layout = QtWidgets.QVBoxLayout(vfd_container)
        vfd_layout.setContentsMargins(0, 0, 0, 0)
        vfd_layout.setSpacing(15)
        
        vfd_inc_layout = QtWidgets.QHBoxLayout()
        
        lbl_vfd_inc = QtWidgets.QLabel("Step Increment:")
        lbl_vfd_inc.setFixedWidth(140) 
        lbl_vfd_inc.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
        
        self.vfd_inc = QtWidgets.QSpinBox()
        self.vfd_inc.setRange(1, 100)
        self.vfd_inc.setValue(5)
        self.vfd_inc.setFixedSize(120, 50) 
        self.vfd_inc.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        
        btn_vfd_inc_minus = QtWidgets.QPushButton("-")
        btn_vfd_inc_minus.setFixedSize(50, 50) 
        btn_vfd_inc_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_vfd_inc_minus.clicked.connect(lambda: self.vfd_inc.setValue(self.vfd_inc.value() - 1))
        
        btn_vfd_inc_plus = QtWidgets.QPushButton("+")
        btn_vfd_inc_plus.setFixedSize(50, 50) 
        btn_vfd_inc_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_vfd_inc_plus.clicked.connect(lambda: self.vfd_inc.setValue(self.vfd_inc.value() + 1))
        
        vfd_inc_layout.addWidget(lbl_vfd_inc)
        vfd_inc_layout.addWidget(btn_vfd_inc_minus)
        vfd_inc_layout.addWidget(self.vfd_inc)
        vfd_inc_layout.addWidget(btn_vfd_inc_plus)
        vfd_inc_layout.addStretch()
        
        vfd_layout.addLayout(vfd_inc_layout)
        
        self.vfd_freq = self.create_vfd_step_control(vfd_layout, "Frequency (Hz):", "HZ")
        
        vfd_layout.addSpacing(15)
        
        vfd_move_layout = QtWidgets.QHBoxLayout()
        vfd_move_layout.setSpacing(15)
        
        btn_vfd_fwd = QtWidgets.QPushButton("▲\nMOVE FWD")
        btn_vfd_fwd.setFixedHeight(140) 
        btn_vfd_fwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        btn_vfd_fwd.setStyleSheet(move_btn_style)
        btn_vfd_fwd.clicked.connect(lambda: self.send_cmd("VFD_FORWARD"))
        
        btn_vfd_bwd = QtWidgets.QPushButton("▼\nMOVE BWD")
        btn_vfd_bwd.setFixedHeight(140) 
        btn_bwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        btn_vfd_bwd.setStyleSheet(move_btn_style)
        btn_vfd_bwd.clicked.connect(lambda: self.send_cmd("VFD_REVERSE"))
        
        vfd_move_layout.addWidget(btn_vfd_fwd, 1)
        vfd_move_layout.addWidget(btn_vfd_bwd, 1)
        vfd_layout.addLayout(vfd_move_layout)
        
        col2_layout.addWidget(vfd_container)
        col2_layout.addStretch() 
        
        self.btn_vfd_stop = QtWidgets.QPushButton("STOP INVERTER")
        self.btn_vfd_stop.setFixedHeight(70)
        self.btn_vfd_stop.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; font-size: 16px; border-radius: 5px; margin-top: 10px;")
        self.btn_vfd_stop.clicked.connect(lambda: self.send_cmd("VFD_STOP"))
        col2_layout.addWidget(self.btn_vfd_stop)

        # =========================================================
        # KOLUMNA 3: RECORDING, CONNECTION, TERMINAL
        # =========================================================
        col3 = QtWidgets.QFrame()
        col3.setObjectName("MainPanel")
        col3.setStyleSheet(panel_style)
        col3_layout = QtWidgets.QVBoxLayout(col3)
        col3_layout.setAlignment(QtCore.Qt.AlignTop)
        col3_layout.setContentsMargins(15, 15, 15, 15)
        col3_layout.setSpacing(15)
        
        # --- PRZYCISK EXIT PRZENIESIONY NA SAMĄ GÓRĘ 3 KOLUMNY ---
        self.btn_exit = QtWidgets.QPushButton("⏻ EXIT APP")
        self.btn_exit.setFixedHeight(50) 
        self.btn_exit.setFixedWidth(160) # <-- DODANE: sztywne ograniczenie szerokości
        self.btn_exit.setStyleSheet("""
            QPushButton { 
                background-color: #4a0000; 
                color: #ffaaaa; 
                font-size: 18px; 
                font-weight: bold; 
                border-radius: 8px; 
            }
            QPushButton:hover { background-color: #660000; color: white; }
            QPushButton:pressed { background-color: #ff0000; color: white; }
        """)
        self.btn_exit.clicked.connect(self.close) 
        
        # <-- ZMIENIONE: dodano parametr alignment spymający przycisk do prawej
        col3_layout.addWidget(self.btn_exit, alignment=QtCore.Qt.AlignRight)
        # ---------------------------------------------------------

        
        lbl_title_3 = QtWidgets.QLabel("DATA RECORDING")
        lbl_title_3.setStyleSheet(header_style)
        # Dodajemy mały margines z góry, by oddzielić od przycisku EXIT
        lbl_title_3.setContentsMargins(0, 10, 0, 0)
        col3_layout.addWidget(lbl_title_3, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        
        disp3 = QtWidgets.QFrame()
        disp3.setObjectName("DisplayPanel")
        disp3.setStyleSheet(display_style)
        disp3_layout = QtWidgets.QHBoxLayout(disp3)
        disp3_layout.setContentsMargins(20, 30, 20, 30)
        disp3_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.lbl_distance = QtWidgets.QLabel("0.00")
        self.lbl_distance.setStyleSheet("color: #2196F3; font-size: 50px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        lbl_m = QtWidgets.QLabel(" m")
        lbl_m.setStyleSheet("color: #2196F3; font-size: 50px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
        
        disp3_layout.addWidget(self.lbl_distance)
        disp3_layout.addWidget(lbl_m)
        col3_layout.addWidget(disp3)
        
        lbl_fn = QtWidgets.QLabel("Filename:")
        lbl_fn.setStyleSheet(label_style)
        
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_input.setStyleSheet(input_style)
        
        col3_layout.addWidget(lbl_fn)
        col3_layout.addWidget(self.filename_input)

        lbl_dir = QtWidgets.QLabel("Save Directory:")
        lbl_dir.setStyleSheet(label_style)
        
        self.save_path_input = QtWidgets.QLineEdit()
        self.save_path_input.setStyleSheet(input_style)
        
        btn_browse = QtWidgets.QPushButton("Browse")
        btn_browse.setStyleSheet("background-color: #444444; color: white; border-radius: 3px; padding: 6px; font-size: 14px;")
        btn_browse.clicked.connect(self.select_save_path)
        
        dir_h = QtWidgets.QHBoxLayout()
        dir_h.addWidget(self.save_path_input)
        dir_h.addWidget(btn_browse)
        
        col3_layout.addWidget(lbl_dir)
        col3_layout.addLayout(dir_h)
        
        rec_h = QtWidgets.QHBoxLayout()
        rec_btn_style = """
            QPushButton { background-color: #444444; color: #aaaaaa; font-size: 14px; border-radius: 5px; border: none; }
            QPushButton:enabled { color: white; }
            QPushButton:hover:enabled { background-color: #555555; }
        """
        
        self.btn_start_rec = QtWidgets.QPushButton("START REC")
        self.btn_start_rec.setFixedHeight(40)
        self.btn_start_rec.setStyleSheet(rec_btn_style)
        self.btn_start_rec.setEnabled(False)
        self.btn_start_rec.clicked.connect(self.start_recording)
        
        self.btn_stop_rec = QtWidgets.QPushButton("STOP REC")
        self.btn_stop_rec.setFixedHeight(40)
        self.btn_stop_rec.setStyleSheet(rec_btn_style)
        self.btn_stop_rec.setEnabled(False)
        self.btn_stop_rec.clicked.connect(self.stop_recording)
        
        rec_h.addWidget(self.btn_start_rec)
        rec_h.addWidget(self.btn_stop_rec)
        col3_layout.addLayout(rec_h)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet("color: #444444;")
        col3_layout.addWidget(line)
        
        lbl_title_conn = QtWidgets.QLabel("CONNECTIVITY")
        lbl_title_conn.setStyleSheet(header_style)
        col3_layout.addWidget(lbl_title_conn, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        
        conn_layout = QtWidgets.QHBoxLayout()
        self.port_combo = QtWidgets.QComboBox()
        self.port_combo.setFixedHeight(30)
        self.btn_refresh = QtWidgets.QPushButton("🔄")
        self.btn_refresh.setFixedSize(35, 30)
        self.btn_refresh.clicked.connect(self.refresh_ports)
        self.btn_connect = QtWidgets.QPushButton("Connect")
        self.btn_connect.setFixedHeight(30)
        self.btn_connect.clicked.connect(self.toggle_connection)
        
        conn_layout.addWidget(self.port_combo)
        conn_layout.addWidget(self.btn_refresh)
        conn_layout.addWidget(self.btn_connect)
        col3_layout.addLayout(conn_layout)
        
        lbl_term = QtWidgets.QLabel("Terminal:")
        lbl_term.setStyleSheet(label_style)
        col3_layout.addWidget(lbl_term)
        
        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #171717; color: #00ff00; font-family: 'Consolas'; font-size: 10pt; border: 1px solid #333; border-radius: 5px;")
        col3_layout.addWidget(self.terminal, 1)

        # =========================================================
        # ZKOŃCZENIE UKŁADU I ZAŚLEPKI DLA app_logic.py
        # =========================================================
        self.curve_distance = DummyCurve()
        self.curve_speed = DummyCurve()
        self.curve_rpm = DummyCurve()

        main_layout.addWidget(col1, 1)
        main_layout.addWidget(col2, 1)
        main_layout.addWidget(col3, 1)

    # ----------------- FUNKCJE POMOCNICZE UI -----------------

    def create_step_control(self, layout, label, cmd_name):
        h_layout = QtWidgets.QHBoxLayout()
        
        lbl = QtWidgets.QLabel(label)
        lbl.setFixedWidth(140) 
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
        h_layout.addWidget(lbl)
        
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(0, 10000)
        spin.setFixedSize(120, 50) 
        spin.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        
        btn_minus = QtWidgets.QPushButton("-")
        btn_minus.setFixedSize(50, 50) 
        btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_minus.clicked.connect(lambda: self.adjust_value(spin, cmd_name, -self.speed_inc.value()))
        
        btn_plus = QtWidgets.QPushButton("+")
        btn_plus.setFixedSize(50, 50) 
        btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_plus.clicked.connect(lambda: self.adjust_value(spin, cmd_name, self.speed_inc.value()))
        
        h_layout.addWidget(btn_minus)
        h_layout.addWidget(spin)
        h_layout.addWidget(btn_plus)
        h_layout.addStretch() 
        
        layout.addLayout(h_layout)
        return spin

    def create_vfd_step_control(self, layout, label, cmd_name):
        h_layout = QtWidgets.QHBoxLayout()
        
        lbl = QtWidgets.QLabel(label)
        lbl.setFixedWidth(140) 
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #cccccc;")
        h_layout.addWidget(lbl)
        
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(0, 100) 
        spin.setFixedSize(120, 50) 
        spin.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        
        btn_minus = QtWidgets.QPushButton("-")
        btn_minus.setFixedSize(50, 50) 
        btn_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_minus.clicked.connect(lambda: self.adjust_value(spin, cmd_name, -self.vfd_inc.value()))
        
        btn_plus = QtWidgets.QPushButton("+")
        btn_plus.setFixedSize(50, 50) 
        btn_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        btn_plus.clicked.connect(lambda: self.adjust_value(spin, cmd_name, self.vfd_inc.value()))
        
        h_layout.addWidget(btn_minus)
        h_layout.addWidget(spin)
        h_layout.addWidget(btn_plus)
        h_layout.addStretch() 
        
        layout.addLayout(h_layout)
        return spin