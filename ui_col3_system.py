import os
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
    
    # =========================================================
    # GÓRNY PASEK: BIAŁE LOGO (ROZCIĄGNIĘTE) + PRZYCISK EXIT
    # =========================================================
    top_bar = QtWidgets.QHBoxLayout()
    top_bar.setSpacing(15) # Odstęp między białym paskiem a przyciskiem EXIT
    
    # --- Biały kontener na logo ---
    ui.logo_container_widget = QtWidgets.QFrame()
    ui.logo_container_widget.setStyleSheet("background-color: white; border-radius: 8px; border: none;")
    ui.logo_container_widget.setFixedHeight(80) 
    
    # Wewnętrzny układ dla białej ramki
    logo_internal_layout = QtWidgets.QHBoxLayout(ui.logo_container_widget)
    logo_internal_layout.setContentsMargins(15, 5, 15, 5) 
    logo_internal_layout.setAlignment(QtCore.Qt.AlignCenter) # Środkuje logo wewnątrz długiego paska
    
    ui.lbl_logo = QtWidgets.QLabel()
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    
    if os.path.exists(logo_path):
        ui.setWindowIcon(QtGui.QIcon(logo_path))
        pixmap = QtGui.QPixmap(logo_path).scaled(
            200, 70, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        ui.lbl_logo.setPixmap(pixmap)
        ui.lbl_logo.setStyleSheet("background: transparent;")
    else:
        ui.lbl_logo.setText("⚙️ SHM SYSTEM") 
        ui.lbl_logo.setStyleSheet("color: black; font-size: 26px; font-weight: bold; background: transparent;")
    
    logo_internal_layout.addWidget(ui.lbl_logo)
    
    # DODAJEMY BIAŁY KONTENER Z PARAMETREM STRETCH = 1 (Wypełnia wolne miejsce)
    top_bar.addWidget(ui.logo_container_widget, 1)
    
    # Przycisk EXIT APP (usunięto ikonkę z tekstu)
    ui.btn_exit = QtWidgets.QPushButton("EXIT APP")
    ui.btn_exit.setFixedHeight(80) 
    ui.btn_exit.setFixedWidth(200)
    ui.btn_exit.setStyleSheet(BTN_EXIT_STYLE)
    ui.btn_exit.clicked.connect(ui.close) 
    
    # DODAJEMY PRZYCISK EXIT Z PARAMETREM STRETCH = 0 (Zachowuje swój sztywny rozmiar)
    top_bar.addWidget(ui.btn_exit, 0)
    
    col3_layout.addLayout(top_bar)
    # =========================================================
    
    line_col3 = QtWidgets.QFrame()
    line_col3.setFrameShape(QtWidgets.QFrame.HLine)
    line_col3.setStyleSheet("color: #444444;")
    col3_layout.addWidget(line_col3)
    
    lbl_title_prof = QtWidgets.QLabel("CONFIGURATIONS")
    lbl_title_prof.setStyleSheet(HEADER_STYLE)
    col3_layout.addWidget(lbl_title_prof, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    prof_container = QtWidgets.QVBoxLayout()
    prof_container.setSpacing(10)
    
    m_layout = QtWidgets.QHBoxLayout()
    ui.mem_group = QtWidgets.QButtonGroup(ui)
    ui.mem_group.setExclusive(True)
    
    ui.btn_m1 = QtWidgets.QPushButton("M1")
    ui.btn_m2 = QtWidgets.QPushButton("M2")
    ui.btn_m3 = QtWidgets.QPushButton("M3")
    ui.btn_m4 = QtWidgets.QPushButton("M4")
    
    for i, btn in enumerate([ui.btn_m1, ui.btn_m2, ui.btn_m3, ui.btn_m4]):
        btn.setCheckable(True)
        btn.setFixedHeight(50)
        btn.setStyleSheet(MEM_BTN_STYLE)
        ui.mem_group.addButton(btn, i + 1)
        m_layout.addWidget(btn)
        
    ui.btn_m1.setChecked(True) 
    prof_container.addLayout(m_layout)
    
    action_layout = QtWidgets.QHBoxLayout()
    
    ui.btn_save_prof = QtWidgets.QPushButton("SAVE TO SELECTED")
    ui.btn_save_prof.setFixedHeight(50)
    ui.btn_save_prof.setStyleSheet(REC_BTN_STYLE) 
    ui.btn_save_prof.clicked.connect(ui.save_profile)
    
    ui.btn_load_prof = QtWidgets.QPushButton("LOAD SELECTED")
    ui.btn_load_prof.setFixedHeight(50)
    ui.btn_load_prof.setStyleSheet(REC_BTN_STYLE)
    ui.btn_load_prof.setEnabled(False)
    ui.btn_load_prof.clicked.connect(ui.load_profile)
    
    action_layout.addWidget(ui.btn_save_prof)
    action_layout.addWidget(ui.btn_load_prof)
    
    prof_container.addLayout(action_layout)
    col3_layout.addLayout(prof_container)
    
    line_col3_2 = QtWidgets.QFrame()
    line_col3_2.setFrameShape(QtWidgets.QFrame.HLine)
    line_col3_2.setStyleSheet("color: #444444;")
    col3_layout.addWidget(line_col3_2)
    
    lbl_title_conn = QtWidgets.QLabel("CONNECTIVITY")
    lbl_title_conn.setStyleSheet(HEADER_STYLE)
    col3_layout.addWidget(lbl_title_conn, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    
    conn_layout = QtWidgets.QHBoxLayout()
    
    ui.port_combo = QtWidgets.QComboBox()
    ui.port_combo.setFixedHeight(60)
    ui.port_combo.setStyleSheet("""
        QComboBox {
            background-color: #333333; color: white; 
            font-size: 20px; font-weight: bold; 
            border: 1px solid #444; border-radius: 5px; padding-left: 10px;
        }
        QComboBox::drop-down { border: none; }
    """)
    
    ui.btn_refresh = QtWidgets.QPushButton("🔄")
    ui.btn_refresh.setFixedSize(60, 60)
    ui.btn_refresh.setStyleSheet("""
        QPushButton { background-color: #444444; color: white; font-size: 26px; border-radius: 5px; }
        QPushButton:hover { background-color: #555555; }
        QPushButton:pressed { background-color: #2196F3; }
    """)
    ui.btn_refresh.clicked.connect(ui.refresh_ports)
    
    ui.btn_connect = QtWidgets.QPushButton("CONNECT")
    ui.btn_connect.setFixedHeight(60)
    ui.btn_connect.setStyleSheet("""
        QPushButton { background-color: #444444; color: white; font-size: 20px; font-weight: bold; border-radius: 5px; }
        QPushButton:hover { background-color: #555555; }
        QPushButton:pressed { background-color: #2196F3; }
    """)
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
    ui.terminal.setStyleSheet("background-color: #171717; color: #e0e0e0; font-family: 'Consolas'; font-size: 12pt; border: 1px solid #333; border-radius: 5px;")
    col3_layout.addWidget(ui.terminal, 1)

    parent_layout.addWidget(col3, 1)