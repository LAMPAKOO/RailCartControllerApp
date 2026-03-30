PANEL_STYLE = "#MainPanel { background-color: #2b2b2b; border: 1px solid #3c3c3c; border-radius: 8px; }"
DISPLAY_STYLE = "#DisplayPanel { background-color: #141414; border-radius: 5px; border: 1px solid #1f1f1f; }"
HEADER_STYLE = "color: #00E5FF; font-size: 24px; font-weight: bold; font-family: 'Segoe UI', Arial, sans-serif; background: transparent; margin-bottom: 5px;"
INPUT_STYLE = "background-color: #333333; color: white; border: 1px solid #444; border-radius: 5px; padding: 8px; font-size: 18px;"
LABEL_STYLE = "color: #aaaaaa; background: transparent; font-size: 16px;"

MOVE_BTN_STYLE = """
    QPushButton { 
        font-size: 24px; 
        font-weight: bold; 
        border-radius: 8px; 
        background-color: #333333; 
        color: #666666; 
    }
    QPushButton:enabled { background-color: #444444; color: white; }
    QPushButton:hover:enabled { background-color: #555555; }
    QPushButton:pressed:enabled { background-color: #2196F3; }
"""

STOP_BTN_STYLE = """
    QPushButton { 
        font-size: 28px; 
        font-weight: bold; 
        border-radius: 8px; 
        margin-top: 10px;
        background-color: #333333; 
        color: #666666; 
    }
    QPushButton:enabled { background-color: #d32f2f; color: white; }
    QPushButton:hover:enabled { background-color: #f44336; }
    QPushButton:pressed:enabled { background-color: #b71c1c; }
"""

MODE_BTN_STYLE = """
    QPushButton { font-size: 20px; font-weight: bold; border-radius: 5px; border: none; background-color: #333333; color: #666666; }
    QPushButton:enabled { background-color: #444444; color: white; }
    QPushButton:checked:enabled { background-color: #2196F3; color: white; }
"""

REC_BTN_STYLE = """
    QPushButton { font-size: 18px; font-weight: bold; border-radius: 5px; border: none; background-color: #333333; color: #666666; }
    QPushButton:enabled { background-color: #444444; color: white; }
    QPushButton:hover:enabled { background-color: #555555; }
"""

BTN_EXIT_STYLE = """
    QPushButton { background-color: #4a0000; color: #ffaaaa; font-size: 24px; font-weight: bold; border-radius: 8px; }
    QPushButton:hover { background-color: #660000; color: white; }
    QPushButton:pressed { background-color: #ff0000; color: white; }
"""

TABS_STYLE = """
    QTabBar::tab { font-size: 20px; font-weight: bold; padding: 15px 30px; background-color: #333333; color: #aaaaaa; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px; }
    QTabBar::tab:selected { background-color: #2196F3; color: white; }
    QTabWidget::pane { border: 1px solid #444444; border-radius: 4px; }
"""

MEM_BTN_STYLE = """
    QPushButton { 
        font-size: 20px; font-weight: bold; border-radius: 5px; border: none; 
        background-color: #333333; color: #aaaaaa; 
    }
    QPushButton:checked { background-color: #FF9800; color: white; }
    QPushButton:hover:!checked { background-color: #444444; }
"""