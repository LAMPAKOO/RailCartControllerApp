from PySide6 import QtWidgets, QtCore, QtGui
from ui_styles import *

def setup_system_column(ui, parent_layout):
    col3 = QtWidgets.QFrame()
    col3.setObjectName("MainPanel")
    col3.setStyleSheet(PANEL_STYLE)
    col3_layout = QtWidgets.QVBoxLayout(col3)
    col3_layout.setAlignment(QtCore.Qt.AlignTop)
    col3_layout.setContentsMargins(15, 15, 15, 15)
    col3_layout.setSpacing(15)
    
    ui.btn_exit = QtWidgets.QPushButton("⏻ EXIT APP")
    ui.btn_exit.setFixedHeight(50) 
    ui.btn_exit.setFixedWidth(160)
    ui.btn_exit.setStyleSheet(BTN_EXIT_STYLE)
    ui.btn_exit.clicked.connect(ui.close) 
    col3_layout.addWidget(ui.btn_exit, alignment=QtCore.Qt.AlignRight)
    
    line_col3 = QtWidgets.QFrame()
    line_col3.setFrameShape(QtWidgets.QFrame.HLine)
    line_col3.setStyleSheet("color: #444444;")
    col3_layout.addWidget(line_col3)
    
    # =========================================================
    # NOWE: SEKCJA KONFIGURACJI (PROFILI)
    # =========================================================
    lbl_title_prof = QtWidgets.QLabel("CONFIGURATIONS")
    lbl_title_prof.setStyleSheet(HEADER_STYLE)
    col3_layout.addWidget(lbl_title_prof, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    prof_layout = QtWidgets.QHBoxLayout()
    ui.profile_combo = QtWidgets.QComboBox()
    ui.profile_combo.addItems(["Profile 1", "Profile 2", "Profile 3", "Profile 4"])
    ui.profile_combo.setFixedHeight(30)
    ui.profile_combo.setStyleSheet(INPUT_STYLE)
    
    ui.btn_save_prof = QtWidgets.QPushButton("SAVE")
    ui.btn_save_prof.setFixedHeight(30)
    ui.btn_save_prof.setStyleSheet(REC_BTN_STYLE) 
    ui.btn_save_prof.clicked.connect(ui.save_profile)
    
    ui.btn_load_prof = QtWidgets.QPushButton("LOAD")
    ui.btn_load_prof.setFixedHeight(30)
    ui.btn_load_prof.setStyleSheet(REC_BTN_STYLE)
    ui.btn_load_prof.clicked.connect(ui.load_profile)
    
    prof_layout.addWidget(ui.profile_combo, 2)
    prof_layout.addWidget(ui.btn_save_prof, 1)
    prof_layout.addWidget(ui.btn_load_prof, 1)
    
    col3_layout.addLayout(prof_layout)
    
    line_col3_2 = QtWidgets.QFrame()
    line_col3_2.setFrameShape(QtWidgets.QFrame.HLine)
    line_col3_2.setStyleSheet("color: #444444;")
    col3_layout.addWidget(line_col3_2)
    # =========================================================
    
    lbl_title_conn = QtWidgets.QLabel("CONNECTIVITY")
    lbl_title_conn.setStyleSheet(HEADER_STYLE)
    col3_layout.addWidget(lbl_title_conn, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    conn_layout = QtWidgets.QHBoxLayout()
    ui.port_combo = QtWidgets.QComboBox()
    ui.port_combo.setFixedHeight(30)
    ui.btn_refresh = QtWidgets.QPushButton("🔄")
    ui.btn_refresh.setFixedSize(35, 30)
    ui.btn_refresh.clicked.connect(ui.refresh_ports)
    ui.btn_connect = QtWidgets.QPushButton("Connect")
    ui.btn_connect.setFixedHeight(30)
    ui.btn_connect.clicked.connect(ui.toggle_connection)
    
    conn_layout.addWidget(ui.port_combo)
    conn_layout.addWidget(ui.btn_refresh)
    conn_layout.addWidget(ui.btn_connect)
    col3_layout.addLayout(conn_layout)
    
    lbl_term = QtWidgets.QLabel("Terminal:")
    lbl_term.setStyleSheet(LABEL_STYLE)
    col3_layout.addWidget(lbl_term)
    
    ui.terminal = QtWidgets.QPlainTextEdit()
    ui.terminal.setReadOnly(True)
    ui.terminal.setStyleSheet("background-color: #171717; color: #00ff00; font-family: 'Consolas'; font-size: 10pt; border: 1px solid #333; border-radius: 5px;")
    col3_layout.addWidget(ui.terminal, 1)

    parent_layout.addWidget(col3, 1)