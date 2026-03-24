PANEL_STYLE = "#MainPanel { background-color: #2b2b2b; border: 1px solid #3c3c3c; border-radius: 8px; }"
DISPLAY_STYLE = "#DisplayPanel { background-color: #141414; border-radius: 5px; border: 1px solid #1f1f1f; }"
HEADER_STYLE = "color: #00E5FF; font-size: 18px; font-weight: bold; font-family: 'Segoe UI', Arial, sans-serif; background: transparent; margin-bottom: 5px;"
INPUT_STYLE = "background-color: #333333; color: white; border: 1px solid #444; border-radius: 3px; padding: 6px; font-size: 14px;"
LABEL_STYLE = "color: #aaaaaa; background: transparent; font-size: 12px;"

MOVE_BTN_STYLE = """
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

MODE_BTN_STYLE = """
    QPushButton { font-size: 16px; font-weight: bold; background-color: #444444; color: white; border-radius: 5px; border: none; }
    QPushButton:checked { background-color: #2196F3; color: white; }
"""

REC_BTN_STYLE = """
    QPushButton { background-color: #444444; color: #aaaaaa; font-size: 14px; border-radius: 5px; border: none; }
    QPushButton:enabled { color: white; }
    QPushButton:hover:enabled { background-color: #555555; }
"""

BTN_EXIT_STYLE = """
    QPushButton { 
        background-color: #4a0000; 
        color: #ffaaaa; 
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 8px; 
    }
    QPushButton:hover { background-color: #660000; color: white; }
    QPushButton:pressed { background-color: #ff0000; color: white; }
"""

TABS_STYLE = """
    QTabBar::tab {
        font-size: 16px; font-weight: bold; padding: 12px 25px;
        background-color: #333333; color: #aaaaaa;
        border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 4px;
    }
    QTabBar::tab:selected { background-color: #2196F3; color: white; }
    QTabWidget::pane { border: 1px solid #444444; border-radius: 4px; }
"""