from PySide6 import QtWidgets, QtCore, QtGui
from ui_styles import *
from ui_helpers import create_vfd_step_control

def setup_inverter_column(ui, parent_layout):
    col2 = QtWidgets.QFrame()
    col2.setObjectName("MainPanel")
    col2.setStyleSheet(PANEL_STYLE)
    col2_layout = QtWidgets.QVBoxLayout(col2)
    col2_layout.setAlignment(QtCore.Qt.AlignTop)
    col2_layout.setContentsMargins(15, 15, 15, 15)
    col2_layout.setSpacing(15)
    
    lbl_title_2 = QtWidgets.QLabel("DRIVE MOTOR CONTROL")
    lbl_title_2.setStyleSheet(HEADER_STYLE)
    col2_layout.addWidget(lbl_title_2, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    disp2 = QtWidgets.QFrame()
    disp2.setObjectName("DisplayPanel")
    disp2.setStyleSheet(DISPLAY_STYLE)
    disp2_layout = QtWidgets.QHBoxLayout(disp2)
    disp2_layout.setContentsMargins(20, 20, 20, 20)
    disp2_layout.setSpacing(15)
    
    lbl_freq_pfx = QtWidgets.QLabel("FREQ: ")
    lbl_freq_pfx.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    
    ui.lbl_vfd_freq = QtWidgets.QLabel("0.00")
    ui.lbl_vfd_freq.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    
    lbl_freq_sfx = QtWidgets.QLabel(" Hz")
    lbl_freq_sfx.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    
    disp2_layout.addWidget(lbl_freq_pfx)
    disp2_layout.addWidget(ui.lbl_vfd_freq)
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
    
    ui.vfd_inc = QtWidgets.QSpinBox()
    ui.vfd_inc.setRange(1, 100)
    ui.vfd_inc.setValue(5)
    ui.vfd_inc.setFixedSize(120, 50) 
    ui.vfd_inc.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
    
    btn_vfd_inc_minus = QtWidgets.QPushButton("-")
    btn_vfd_inc_minus.setFixedSize(50, 50) 
    btn_vfd_inc_minus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_vfd_inc_minus.clicked.connect(lambda: ui.vfd_inc.setValue(ui.vfd_inc.value() - 1))
    
    btn_vfd_inc_plus = QtWidgets.QPushButton("+")
    btn_vfd_inc_plus.setFixedSize(50, 50) 
    btn_vfd_inc_plus.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
    btn_vfd_inc_plus.clicked.connect(lambda: ui.vfd_inc.setValue(ui.vfd_inc.value() + 1))
    
    vfd_inc_layout.addWidget(lbl_vfd_inc)
    vfd_inc_layout.addWidget(btn_vfd_inc_minus)
    vfd_inc_layout.addWidget(ui.vfd_inc)
    vfd_inc_layout.addWidget(btn_vfd_inc_plus)
    vfd_inc_layout.addStretch()
    
    vfd_layout.addLayout(vfd_inc_layout)
    
    ui.vfd_freq = create_vfd_step_control(ui, vfd_layout, "Frequency (Hz):", "HZ")
    
    vfd_layout.addSpacing(15)
    
    vfd_move_layout = QtWidgets.QHBoxLayout()
    vfd_move_layout.setSpacing(15)
    
    # --- PRZYPISANIE DO ui. ORAZ ZABLOKOWANIE ---
    ui.btn_vfd_fwd = QtWidgets.QPushButton("▲\nDRIVE FORWARD")
    ui.btn_vfd_fwd.setFixedHeight(140) 
    ui.btn_vfd_fwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    ui.btn_vfd_fwd.setStyleSheet(MOVE_BTN_STYLE)
    ui.btn_vfd_fwd.setEnabled(False)
    ui.btn_vfd_fwd.clicked.connect(lambda: ui.send_cmd("VFD_FORWARD"))
    
    ui.btn_vfd_bwd = QtWidgets.QPushButton("▼\nDRIVE BACKWARD")
    ui.btn_vfd_bwd.setFixedHeight(140) 
    ui.btn_vfd_bwd.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    ui.btn_vfd_bwd.setStyleSheet(MOVE_BTN_STYLE)
    ui.btn_vfd_bwd.setEnabled(False)
    ui.btn_vfd_bwd.clicked.connect(lambda: ui.send_cmd("VFD_REVERSE"))
    
    vfd_move_layout.addWidget(ui.btn_vfd_fwd, 1)
    vfd_move_layout.addWidget(ui.btn_vfd_bwd, 1)
    vfd_layout.addLayout(vfd_move_layout)
    
    col2_layout.addWidget(vfd_container)
    
    ui.btn_vfd_stop = QtWidgets.QPushButton("STOP INVERTER")
    ui.btn_vfd_stop.setFixedHeight(100) # Zmienione z 70 na 60, aby był IDENTYCZNY jak w col1
    ui.btn_vfd_stop.setStyleSheet(STOP_BTN_STYLE) # <--- Użycie nowego stylu
    ui.btn_vfd_stop.setEnabled(False)             # <--- Domyślne wyszarzenie
    ui.btn_vfd_stop.clicked.connect(lambda: ui.send_cmd("VFD_STOP"))
    col2_layout.addWidget(ui.btn_vfd_stop)

    col2_layout.addSpacing(15)
    
    line_col2 = QtWidgets.QFrame()
    line_col2.setFrameShape(QtWidgets.QFrame.HLine)
    line_col2.setStyleSheet("color: #444444;")
    col2_layout.addWidget(line_col2)

    # --- SEKCJA RECORDING ---
    lbl_title_3 = QtWidgets.QLabel("DISTANCE RECORDING")
    lbl_title_3.setStyleSheet(HEADER_STYLE)
    lbl_title_3.setContentsMargins(0, 10, 0, 0)
    col2_layout.addWidget(lbl_title_3, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    disp3 = QtWidgets.QFrame()
    disp3.setObjectName("DisplayPanel")
    disp3.setStyleSheet(DISPLAY_STYLE)
    disp3_layout = QtWidgets.QHBoxLayout(disp3)
    disp3_layout.setContentsMargins(10, 15, 10, 15)
    
    rel_layout = QtWidgets.QVBoxLayout()
    rel_layout.setAlignment(QtCore.Qt.AlignCenter)
    lbl_rel_title = QtWidgets.QLabel("RELATIVE")
    lbl_rel_title.setStyleSheet("color: #aaaaaa; font-size: 14px; font-weight: bold; background: transparent;")
    lbl_rel_title.setAlignment(QtCore.Qt.AlignCenter)
    
    h_rel = QtWidgets.QHBoxLayout()
    ui.lbl_distance_rel = QtWidgets.QLabel("0.00")
    ui.lbl_distance_rel.setStyleSheet("color: #2196F3; font-size: 36px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    lbl_rel_m = QtWidgets.QLabel("m")
    lbl_rel_m.setStyleSheet("color: #2196F3; font-size: 20px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_rel.addWidget(ui.lbl_distance_rel)
    h_rel.addWidget(lbl_rel_m)
    h_rel.setAlignment(QtCore.Qt.AlignCenter)
    
    rel_layout.addWidget(lbl_rel_title)
    rel_layout.addLayout(h_rel)
    
    v_line_dist = QtWidgets.QFrame()
    v_line_dist.setFrameShape(QtWidgets.QFrame.VLine)
    v_line_dist.setStyleSheet("color: #333333;")
    
    abs_layout = QtWidgets.QVBoxLayout()
    abs_layout.setAlignment(QtCore.Qt.AlignCenter)
    lbl_abs_title = QtWidgets.QLabel("ABSOLUTE")
    lbl_abs_title.setStyleSheet("color: #aaaaaa; font-size: 14px; font-weight: bold; background: transparent;")
    lbl_abs_title.setAlignment(QtCore.Qt.AlignCenter)
    
    h_abs = QtWidgets.QHBoxLayout()
    ui.lbl_distance_abs = QtWidgets.QLabel("0.00")
    ui.lbl_distance_abs.setStyleSheet("color: #FF9800; font-size: 36px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    lbl_abs_m = QtWidgets.QLabel("m")
    lbl_abs_m.setStyleSheet("color: #FF9800; font-size: 20px; font-weight: bold; font-family: 'Consolas'; background: transparent;")
    h_abs.addWidget(ui.lbl_distance_abs)
    h_abs.addWidget(lbl_abs_m)
    h_abs.setAlignment(QtCore.Qt.AlignCenter)
    
    abs_layout.addWidget(lbl_abs_title)
    abs_layout.addLayout(h_abs)
    
    disp3_layout.addLayout(rel_layout)
    disp3_layout.addWidget(v_line_dist)
    disp3_layout.addLayout(abs_layout)
    
    col2_layout.addWidget(disp3)
    
    file_dir_layout = QtWidgets.QHBoxLayout()
    file_dir_layout.setSpacing(10)
    
    lbl_fn = QtWidgets.QLabel("Filename:")
    lbl_fn.setStyleSheet(LABEL_STYLE)
    ui.filename_input = QtWidgets.QLineEdit()
    ui.filename_input.setStyleSheet(INPUT_STYLE)
    
    lbl_dir = QtWidgets.QLabel("Save Dir:")
    lbl_dir.setStyleSheet(LABEL_STYLE)
    lbl_dir.setContentsMargins(10, 0, 0, 0)
    ui.save_path_input = QtWidgets.QLineEdit()
    ui.save_path_input.setStyleSheet(INPUT_STYLE)
    
    btn_browse = QtWidgets.QPushButton("Browse")
    btn_browse.setStyleSheet("background-color: #444444; color: white; border-radius: 3px; padding: 6px; font-size: 14px;")
    btn_browse.clicked.connect(ui.select_save_path)
    
    file_dir_layout.addWidget(lbl_fn)
    file_dir_layout.addWidget(ui.filename_input, 1)
    file_dir_layout.addWidget(lbl_dir)
    file_dir_layout.addWidget(ui.save_path_input, 2)
    file_dir_layout.addWidget(btn_browse)
    
    col2_layout.addLayout(file_dir_layout)
    
    rec_h = QtWidgets.QHBoxLayout()
    
    ui.btn_start_rec = QtWidgets.QPushButton("START RECORDING")
    ui.btn_start_rec.setFixedHeight(70)
    ui.btn_start_rec.setStyleSheet(REC_BTN_STYLE)
    ui.btn_start_rec.setEnabled(False)
    ui.btn_start_rec.clicked.connect(ui.start_recording)
    
    ui.btn_stop_rec = QtWidgets.QPushButton("STOP RECORDING")
    ui.btn_stop_rec.setFixedHeight(70)
    ui.btn_stop_rec.setStyleSheet(REC_BTN_STYLE)
    ui.btn_stop_rec.setEnabled(False)
    ui.btn_stop_rec.clicked.connect(ui.stop_recording)
    
    rec_h.addWidget(ui.btn_start_rec)
    rec_h.addWidget(ui.btn_stop_rec)
    col2_layout.addLayout(rec_h)
    
    col2_layout.addStretch() 
    parent_layout.addWidget(col2, 1)