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
    # SEKCJA KONFIGURACJI (PROFILI M1-M4)
    # =========================================================
    lbl_title_prof = QtWidgets.QLabel("CONFIGURATIONS")
    lbl_title_prof.setStyleSheet(HEADER_STYLE)
    col3_layout.addWidget(lbl_title_prof, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    prof_container = QtWidgets.QVBoxLayout()
    prof_container.setSpacing(10)
    
    # Rząd przycisków M1-M4
    m_layout = QtWidgets.QHBoxLayout()
    ui.mem_group = QtWidgets.QButtonGroup(ui)
    ui.mem_group.setExclusive(True)
    
    ui.btn_m1 = QtWidgets.QPushButton("M1")
    ui.btn_m2 = QtWidgets.QPushButton("M2")
    ui.btn_m3 = QtWidgets.QPushButton("M3")
    ui.btn_m4 = QtWidgets.QPushButton("M4")
    
    for i, btn in enumerate([ui.btn_m1, ui.btn_m2, ui.btn_m3, ui.btn_m4]):
        btn.setCheckable(True)
        btn.setFixedHeight(35)
        btn.setStyleSheet(MEM_BTN_STYLE)
        ui.mem_group.addButton(btn, i + 1)
        m_layout.addWidget(btn)
        
    ui.btn_m1.setChecked(True) # Domyślnie zaznaczony pierwszy
    
    prof_container.addLayout(m_layout)
    
    # Rząd przycisków SAVE/LOAD
    action_layout = QtWidgets.QHBoxLayout()
    
    ui.btn_save_prof = QtWidgets.QPushButton("SAVE TO SELECTED")
    ui.btn_save_prof.setFixedHeight(35)
    ui.btn_save_prof.setStyleSheet(REC_BTN_STYLE) 
    ui.btn_save_prof.clicked.connect(ui.save_profile)
    
    ui.btn_load_prof = QtWidgets.QPushButton("LOAD SELECTED")
    ui.btn_load_prof.setFixedHeight(35)
    ui.btn_load_prof.setStyleSheet(REC_BTN_STYLE)
    ui.btn_load_prof.clicked.connect(ui.load_profile)
    
    action_layout.addWidget(ui.btn_save_prof)
    action_layout.addWidget(ui.btn_load_prof)
    
    prof_container.addLayout(action_layout)
    col3_layout.addLayout(prof_container)
    
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