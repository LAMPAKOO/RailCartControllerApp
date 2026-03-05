import serial
import serial.tools.list_ports
import csv
import os
import sys
import json
from datetime import datetime
from collections import deque
from PySide6 import QtWidgets, QtCore, QtGui

# Importujemy klasę interfejsu z drugiego pliku
from ui_layout import AppUI

class IndustrialControlApp(AppUI):
    def __init__(self):
        super().__init__()
        
        # --- Internal States ---
        self.ser = None
        self.is_recording = False
        self.csv_file = None
        self.csv_writer = None
        self.current_full_path = ""
        
        # Osobne bufory dla TRZECH zmiennych
        self.data_distance = deque([0] * 100, maxlen=100)
        self.data_speed = deque([0] * 100, maxlen=100)
        self.data_rpm = deque([0] * 100, maxlen=100)
        
        # --- Config States ---
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.config_file = os.path.join(self.base_dir, "config.json")
        self.config_data = {"filename": "motor_test", "save_dir": self.base_dir}
        
        # Budowa UI (dziedziczona z AppUI)
        self.init_ui()
        
        # Inicjalizacja konfiguracji (odczyt + podpięcie sygnałów zapisu)
        self.init_config()
        
        self.refresh_ports()
        
        # UART Reading Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.listen_to_uart)

    # ------------------ KONFIGURACJA PLIKÓW ------------------
    def init_config(self):
        """Odczytuje config z pliku JSON i ustawia wartości w UI."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if os.path.isdir(loaded.get("save_dir", "")):
                        self.config_data["save_dir"] = loaded["save_dir"]
                    self.config_data["filename"] = loaded.get("filename", "motor_test")
            except Exception as e:
                self.log(f"Config Load Error: {str(e)}")

        # Wpisanie odczytanych wartości do pól w UI
        self.filename_input.setText(self.config_data["filename"])
        self.save_path_input.setText(self.config_data["save_dir"])
        
        # Podpięcie sygnałów: zapisz config za każdym razem, gdy użytkownik wpisze tekst
        self.filename_input.textChanged.connect(self.save_config)
        self.save_path_input.textChanged.connect(self.save_config)

    def save_config(self):
        """Zapisuje obecne wartości pól do pliku JSON."""
        self.config_data["filename"] = self.filename_input.text()
        self.config_data["save_dir"] = self.save_path_input.text()
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            self.log(f"Config Save Error: {str(e)}")

    def select_save_path(self):
        """Otwiera okno dialogowe do wyboru folderu zapisu."""
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.save_path_input.text())
        if path:
            self.save_path_input.setText(path)
            self.save_config()

    # ------------------ LOGIKA GŁÓWNA ------------------
    def log(self, msg):
        time_str = datetime.now().strftime('%H:%M:%S')
        self.terminal.appendPlainText(f" {time_str} | {msg}")
        self.terminal.moveCursor(QtGui.QTextCursor.End)

    def refresh_ports(self):
        self.port_combo.clear()
        
        ports = []
        for p in serial.tools.list_ports.comports():
            if sys.platform.startswith('linux'):
                # Jeśli to Linux, dodaj tylko te porty, które mają 'tty' w nazwie
                # (odrzuca np. dziwne porty wirtualne lub puste duszki)
                if 'tty' in p.device.lower():
                    ports.append(p.device)
            else:
                # Jeśli to Windows/Mac, zostaw standardowe ładowanie (np. COM3)
                ports.append(p.device)
                
        self.port_combo.addItems(ports)
        self.log("SYSTEM: Port list updated")

    def toggle_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.ser = None
            self.timer.stop()
            self.btn_connect.setText("Connect")
            self.log("Disconnected")
        else:
            try:
                port = self.port_combo.currentText()
                if not port: return
                self.ser = serial.Serial(port, 115200, timeout=0.1)
                self.btn_connect.setText("Disconnect")
                self.timer.start(30)
                
                # Zsynchronizuj tryb z kontrolerem zaraz po połączeniu
                if self.btn_manual.isChecked():
                    self.send_cmd("MODE_MANUAL")
                else:
                    self.send_cmd("MODE_AUTO")
                
                # Pobierz aktualne wartości z kontrolera
                self.read_nvs()
                self.log(f"Connected to {port}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def send_cmd(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())
            self.log(f">> {cmd}")

    def adjust_value(self, spin, cmd, delta):
        new_val = max(0, spin.value() + delta)
        spin.setValue(new_val)
        self.send_cmd(f"{cmd} {new_val}")
        
    def switch_to_manual(self):
        self.send_cmd("MODE_MANUAL")
        self.send_cmd("STOP")
        if self.ser and self.ser.is_open:
            self.send_cmd(f"forwardSpeed {self.fwd_speed.value()}")
            self.send_cmd(f"backwardSpeed {self.bwd_speed.value()}")

    def listen_to_uart(self):
        if not self.ser or not self.ser.is_open: return
        try:
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='replace').strip()
                if not line: continue
                
                if line.startswith("DATA:"):
                    try:
                        raw_data = line.replace("DATA:", "").strip()
                        parts = raw_data.split(",")
                        
                        if len(parts) >= 3:
                            dist = float(parts[0])
                            speed = float(parts[1])
                            rpm = float(parts[2])
                            
                            # --- UPDATE DISPLAYS ---
                            self.lbl_distance.setText(f"{dist:.2f}")
                            self.lbl_speed.setText(f"{speed:.2f}")
                            self.lbl_rpm.setText(f"{rpm:.2f}")
                            
                            # --- UPDATE PLOT DATA (Hidden) ---
                            self.data_distance.append(dist)
                            self.data_speed.append(speed)
                            self.data_rpm.append(rpm)
                            self.curve_distance.setData(list(self.data_distance))
                            self.curve_speed.setData(list(self.data_speed))
                            self.curve_rpm.setData(list(self.data_rpm))
                            
                            # --- RECORD CSV ---
                            if self.is_recording:
                                self.csv_writer.writerow([
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], 
                                    dist, speed, rpm
                                ])
                    except ValueError:
                        pass # Zignoruj błędy uszkodzonej ramki
                else:
                    self.log(f"<< {line}")
                    self.process_incoming_params(line)
        except Exception as e:
            self.log(f"UART ERR: {str(e)}")

    def process_incoming_params(self, line):
        if ":" in line and "==" not in line:
            try:
                name, val = [x.strip() for x in line.split(":")]
                val_f = float(val)
                if name == "forwardSpeed": self.fwd_speed.setValue(val_f)
                elif name == "backwardSpeed": self.bwd_speed.setValue(val_f)
                elif name == "accGlue": self.glue_acc.setValue(int(val_f))
                elif name == "calibGlue": self.cal_glue.setText(f"{val_f:.4f}")
            except: pass

    def start_recording(self):
        base_name = self.filename_input.text().strip()
        folder = self.save_path_input.text().strip()
        if not base_name: return
        try:
            start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_full_path = os.path.join(folder, f"{base_name}_start_{start_time}.csv")
            self.csv_file = open(self.current_full_path, mode='w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            
            self.csv_writer.writerow(["Timestamp", "Distance", "Speed", "RPM"])
            self.is_recording = True
            self.send_cmd("START_RECORDING")
            
            self.btn_start_rec.setEnabled(False)
            self.btn_stop_rec.setEnabled(True)
            self.log(f"RECORDING STARTED: {os.path.basename(self.current_full_path)}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "File Error", str(e))

    def stop_recording(self):
        if not self.is_recording: return
        self.is_recording = False
        
        self.send_cmd("STOP_RECORDING")
        self.csv_file.close()
        
        end_time = datetime.now().strftime("%H%M%S")
        final_path = self.current_full_path.replace(".csv", f"_end_{end_time}.csv")
        os.rename(self.current_full_path, final_path)
        
        self.btn_start_rec.setEnabled(True)
        self.btn_stop_rec.setEnabled(False)
        self.log(f"RECORDING SAVED: {os.path.basename(final_path)}")

    def apply_all(self):
        self.send_cmd(f"forwardSpeed {self.fwd_speed.value()}")
        self.send_cmd(f"backwardSpeed {self.bwd_speed.value()}")
        self.send_cmd(f"glueAcc {self.glue_acc.value()}")
        self.send_cmd(f"calGlue {self.cal_glue.text()}")

    def read_nvs(self):
        self.send_cmd("READNVS")