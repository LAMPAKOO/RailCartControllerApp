import serial
import serial.tools.list_ports
import csv
import os
import sys
import json
import time 
import html
from datetime import datetime
from collections import deque
from PySide6 import QtWidgets, QtCore, QtGui

from ui_layout import AppUI
from ui_styles import * 

class IndustrialControlApp(AppUI):
    def __init__(self):
        super().__init__()
        
        self.ser = None
        self.is_recording = False
        self.csv_file = None
        self.csv_writer = None
        self.current_full_path = ""
        
        self.data_distance = deque([0] * 100, maxlen=100)
        self.data_speed = deque([0] * 100, maxlen=100)
        self.data_rpm = deque([0] * 100, maxlen=100)
        
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.config_file = os.path.join(self.base_dir, "config.json")
        
        self.config_data = {
            "last_port": "",
            "global_filename": "motor_test",
            "global_save_dir": self.base_dir,
            "profiles": {
                f"Profile {i}": {
                    "filename": "motor_test",
                    "save_dir": self.base_dir,
                    "speed_inc": 50,
                    "fwd_speed": 0,
                    "bwd_speed": 0,
                    "vfd_inc": 5,
                    "vfd_freq": 0,
                    "glue_acc": 0,
                    "cal_glue": "0.0000"
                } for i in range(1, 5)
            }
        }
        
        self.init_ui()
        self.init_config()           
        self.setup_initial_state()   
        self.refresh_ports()         
        
        # ==========================================
        # NOWE: LOGI TERMINALA (OSOBNY PLIK)
        # ==========================================
        self.logs_dir = os.path.join(self.base_dir, "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        self.log_file_path = os.path.join(self.logs_dir, f"terminal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        self.log_file = open(self.log_file_path, "a", encoding="utf-8")
        
        # ==========================================
        # NOWE: AUTO-SAVE (ZABEZPIECZENIE DANYCH)
        # ==========================================
        self.autosave_timer = QtCore.QTimer()
        self.autosave_timer.timeout.connect(self.autosave_files)
        self.autosave_timer.start(5000) # Co 5 sekund twardy zapis na dysk

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.listen_to_uart)

    def autosave_files(self):
        """Wymusza twardy zapis buforów plików na dysk (ochrona przed utratą zasilania)"""
        try:
            if self.is_recording and self.csv_file and not self.csv_file.closed:
                self.csv_file.flush()
                os.fsync(self.csv_file.fileno())
                
            if hasattr(self, 'log_file') and self.log_file and not self.log_file.closed:
                self.log_file.flush()
                os.fsync(self.log_file.fileno())
        except Exception:
            pass # Ignoruje ewentualne konflikty zapisu

    def show_modern_question(self, title, text):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg.setDefaultButton(QtWidgets.QMessageBox.No)
        
        msg.setStyleSheet("""
            QMessageBox { background-color: #2b2b2b; }
            QLabel { color: #ffffff; font-size: 20px; font-weight: bold; font-family: 'Segoe UI'; margin-right: 20px; margin-bottom: 5px; }
            QPushButton { 
                background-color: #444444; color: white; font-size: 18px; 
                font-weight: bold; border-radius: 6px; padding: 10px 25px; 
                min-width: 100px; margin: 10px 5px; 
            }
            QPushButton:hover { background-color: #2196F3; }
            QPushButton:pressed { background-color: #1976D2; }
        """)
        return msg.exec()

    def show_modern_error(self, title, text):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        
        msg.setStyleSheet("""
            QMessageBox { background-color: #2b2b2b; }
            QLabel { color: #ff5252; font-size: 20px; font-weight: bold; font-family: 'Segoe UI'; margin-right: 20px; margin-bottom: 5px; }
            QPushButton { 
                background-color: #444444; color: white; font-size: 18px; 
                font-weight: bold; border-radius: 6px; padding: 10px 25px; 
                min-width: 100px; margin: 10px 5px; 
            }
            QPushButton:hover { background-color: #d32f2f; }
            QPushButton:pressed { background-color: #b71c1c; }
        """)
        msg.exec()

    def closeEvent(self, event):
        reply = self.show_modern_question(
            'Exit Confirmation', 
            'Are you sure you want to exit the application?'
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            if self.is_recording:
                self.stop_recording()
                
            if self.ser and self.ser.is_open:
                try:
                    self.send_cmd("STOP")
                    self.send_cmd("VFD_STOP")
                    time.sleep(0.1) 
                    self.ser.close()
                except Exception:
                    pass
            
            # Zamykamy plik z logami
            if hasattr(self, 'log_file') and self.log_file and not self.log_file.closed:
                self.log_file.close()
                
            event.accept()
        else:
            event.ignore()

    def init_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    
                    if "profiles" in loaded:
                        for p in loaded["profiles"]:
                            if p in self.config_data["profiles"]:
                                self.config_data["profiles"][p].update(loaded["profiles"][p])
                    if "last_port" in loaded:
                        self.config_data["last_port"] = loaded["last_port"]
                    if "global_filename" in loaded:
                        self.config_data["global_filename"] = loaded["global_filename"]
                    if "global_save_dir" in loaded:
                        self.config_data["global_save_dir"] = loaded["global_save_dir"]
            except Exception as e:
                self.log(f"Config Load Error: {str(e)}")

    def setup_initial_state(self):
        self.filename_input.setText(self.config_data["global_filename"])
        self.save_path_input.setText(self.config_data["global_save_dir"])
        
        self.filename_input.textChanged.connect(self.save_global_state)
        self.save_path_input.textChanged.connect(self.save_global_state)
        self.port_combo.currentTextChanged.connect(self.save_global_state)

    def save_global_state(self, *args):
        self.config_data["global_filename"] = self.filename_input.text()
        self.config_data["global_save_dir"] = self.save_path_input.text()
        self.config_data["last_port"] = self.port_combo.currentText()
        self.save_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            self.log(f"Config Save Error: {str(e)}")

    def get_selected_profile(self):
        mem_id = self.mem_group.checkedId()
        return f"Profile {mem_id}" if mem_id > 0 else "Profile 1"

    def save_profile(self):
        current_prof = self.get_selected_profile()
        if current_prof not in self.config_data["profiles"]: return
        
        reply = self.show_modern_question(
            'Save Confirmation', 
            f'Are you sure you want to OVERWRITE settings in {current_prof}?'
        )
        if reply == QtWidgets.QMessageBox.No:
            return
            
        prof = self.config_data["profiles"][current_prof]
        
        prof["filename"] = self.filename_input.text()
        prof["save_dir"] = self.save_path_input.text()
        prof["speed_inc"] = int(self.speed_inc.text() or 0)
        prof["fwd_speed"] = int(self.fwd_speed.text() or 0)
        prof["bwd_speed"] = int(self.bwd_speed.text() or 0)
        prof["vfd_inc"] = int(self.vfd_inc.text() or 0)
        prof["vfd_freq"] = int(self.vfd_freq.text() or 0)
        prof["glue_acc"] = int(self.glue_acc.text() or 0)
        prof["cal_glue"] = self.cal_glue.text()
        
        self.save_config()
        self.log(f"SYSTEM: Configuration saved to slot {current_prof.replace('Profile ', 'M')}")

    def load_profile(self):
        current_prof = self.get_selected_profile()
        if current_prof not in self.config_data["profiles"]: return
        
        reply = self.show_modern_question(
            'Load Confirmation', 
            f'Are you sure you want to LOAD {current_prof}?\nCurrent unsaved parameters will be lost.'
        )
        if reply == QtWidgets.QMessageBox.No:
            return
            
        prof = self.config_data["profiles"][current_prof]
        
        self.filename_input.setText(prof.get("filename", "motor_test"))
        self.save_path_input.setText(prof.get("save_dir", self.base_dir))
        
        self.speed_inc.setText(str(prof.get("speed_inc", 50)))
        self.fwd_speed.setText(str(prof.get("fwd_speed", 0)))
        self.bwd_speed.setText(str(prof.get("bwd_speed", 0)))
        self.vfd_inc.setText(str(prof.get("vfd_inc", 5)))
        self.vfd_freq.setText(str(prof.get("vfd_freq", 0)))
        self.glue_acc.setText(str(prof.get("glue_acc", 0)))
        self.cal_glue.setText(prof.get("cal_glue", "0.0000"))
        
        self.log(f"SYSTEM: Configuration loaded from slot {current_prof.replace('Profile ', 'M')}")

    def select_save_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.save_path_input.text())
        if path:
            self.save_path_input.setText(path)

    def log(self, msg):
        time_str = datetime.now().strftime('%H:%M:%S')
        color = "#e0e0e0"  
        msg_lower = msg.lower()
        
        if "error" in msg_lower or "err:" in msg_lower:
            color = "#d32f2f" 
        elif msg.startswith(">>"):
            color = "#4FC3F7"  
        elif "system:" in msg_lower or "connected" in msg_lower or "disconnected" in msg_lower or "recording" in msg_lower:
            color = "#FFCA28"  
            
        try:
            if hasattr(self, 'log_file') and self.log_file and not self.log_file.closed:
                self.log_file.write(f"[{time_str}] {msg}\n")
        except Exception:
            pass
            
        safe_msg = html.escape(msg)
        
        # Używamy kuloodpornej tabeli HTML do idealnego wyrównania długiego tekstu
        html_line = (
            f'<table width="100%" style="margin:0; padding:0; border:none;">'
            f'<tr>'
            f'<td width="95" style="color: #666666; vertical-align: top; white-space: nowrap;">{time_str} | </td>'
            f'<td style="color: {color}; vertical-align: top;">{safe_msg}</td>'
            f'</tr>'
            f'</table>'
        )
        
        self.terminal.append(html_line) # Dla QTextEdit używamy append() zamiast appendHtml()
        self.terminal.moveCursor(QtGui.QTextCursor.End)

    def refresh_ports(self):
        self.port_combo.blockSignals(True)
        self.port_combo.clear()
        
        ports = []
        for p in serial.tools.list_ports.comports():
            if sys.platform.startswith('linux'):
                if 'ttyUSB' in p.device or 'ttyACM' in p.device:
                    ports.append(p.device)
            else:
                ports.append(p.device)
        
        self.port_combo.addItems(ports)
        
        saved_port = self.config_data.get("last_port", "")
        if saved_port in ports:
            self.port_combo.setCurrentText(saved_port)
        elif ports:
            self.port_combo.setCurrentIndex(0)
            
        self.port_combo.blockSignals(False)
        self.save_global_state() 
        self.log("SYSTEM: Port list updated")

    def toggle_connection(self):
        if self.ser and self.ser.is_open:
            
            reply = self.show_modern_question(
                'Disconnect Confirmation', 
                'Are you sure you want to DISCONNECT from the machine?'
            )
            if reply == QtWidgets.QMessageBox.No:
                return

            if self.is_recording:
                self.stop_recording()
                
            self.ser.close()
            self.ser = None
            self.timer.stop()
            self.btn_connect.setText("CONNECT")
            self.btn_start_rec.setEnabled(False) 
            
            self.btn_manual.setEnabled(False)
            self.btn_auto.setEnabled(False)
            self.btn_glue_fwd.setEnabled(False)
            self.btn_glue_bwd.setEnabled(False)
            self.btn_vfd_fwd.setEnabled(False)
            self.btn_vfd_bwd.setEnabled(False)
            self.btn_motor_stop.setEnabled(False) 
            self.btn_vfd_stop.setEnabled(False)   
            self.btn_load_prof.setEnabled(False)
            
            self.log("Disconnected")
        else:
            try:
                port = self.port_combo.currentText()
                if not port: return
                self.ser = serial.Serial(port, 115200, timeout=0.1)
                
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                
                self.btn_connect.setText("DISCONNECT")
                self.btn_start_rec.setEnabled(True) 
                self.timer.start(30)
                
                self.log(f"Connected to {port}")
                
                self.btn_manual.setEnabled(True)
                self.btn_auto.setEnabled(True)
                self.btn_vfd_fwd.setEnabled(True)
                self.btn_vfd_bwd.setEnabled(True)
                self.btn_motor_stop.setEnabled(True) 
                self.btn_vfd_stop.setEnabled(True)   
                self.btn_glue_fwd.setEnabled(True)
                self.btn_glue_bwd.setEnabled(True)
                self.btn_load_prof.setEnabled(True)
                
                self.btn_manual.setChecked(True)
                self.send_cmd("MODE_MANUAL")
                
                self.read_nvs() 
                
            except Exception as e:
                self.show_modern_error("Connection Error", str(e))

    def send_cmd(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())
            self.log(f">> {cmd}")

    def adjust_value(self, edit, cmd, delta):
        current_val = int(edit.text() or 0)
        new_val = current_val + delta
        
        if cmd == "HZ":
            new_val = max(MIN_VFD_FREQ, min(MAX_VFD_FREQ, new_val))
        else:
            new_val = max(MIN_SPEED, min(MAX_SPEED, new_val))
            
        edit.setText(str(new_val))
        self.send_cmd(f"{cmd} {new_val}")
        
    def switch_to_manual(self):
        self.btn_manual.setChecked(True)
        if self.ser and self.ser.is_open:
            self.btn_glue_fwd.setEnabled(True)
            self.btn_glue_bwd.setEnabled(True)
            
        self.send_cmd("MODE_MANUAL")
        self.send_cmd("STOP")
        if self.ser and self.ser.is_open:
            self.send_cmd(f"forwardSpeed {self.fwd_speed.text() or 0}")
            self.send_cmd(f"backwardSpeed {self.bwd_speed.text() or 0}")

    def switch_to_auto(self):
        self.btn_auto.setChecked(True)
        self.btn_glue_fwd.setEnabled(False)
        self.btn_glue_bwd.setEnabled(False)
        self.send_cmd("MODE_AUTO")

    def stop_motor(self):
        self.send_cmd("STOP")
        if self.btn_auto.isChecked():
            self.switch_to_manual()

    def start_dispense(self):
        self.send_cmd(f"forwardSpeed {self.fwd_speed.text() or 0}")
        self.send_cmd("MOVE_FORWARD")

    def start_retract(self):
        self.send_cmd(f"backwardSpeed {self.bwd_speed.text() or 0}")
        self.send_cmd("MOVE_BACKWARD")

    def start_vfd_forward(self):
        # self.send_cmd(f"HZ {self.vfd_freq.text() or 0}")
        self.send_cmd("VFD_FORWARD")

    def start_vfd_reverse(self):
        # self.send_cmd(f"HZ {self.vfd_freq.text() or 0}")
        self.send_cmd("VFD_REVERSE")

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
                        
                        if len(parts) >= 4:
                            dist_rel = float(parts[0])
                            dist_abs = float(parts[1])
                            rpm = float(parts[2])
                            speed = float(parts[3])
                            freq = 0.0
                            
                            if len(parts) >= 5:
                                freq = float(parts[4])
                                self.lbl_vfd_freq.setText(f"{freq:.2f}")
                            
                            self.lbl_distance_rel.setText(f"{dist_rel:.2f}")
                            self.lbl_distance_abs.setText(f"{dist_abs:.2f}")
                            self.lbl_rpm.setText(f"{rpm:.2f}")
                            self.lbl_speed.setText(f"{speed:.2f}")
                            
                            self.data_distance.append(dist_rel)
                            self.data_speed.append(speed)
                            self.data_rpm.append(rpm)
                            self.curve_distance.setData(list(self.data_distance))
                            self.curve_speed.setData(list(self.data_speed))
                            self.curve_rpm.setData(list(self.data_rpm))
                            
                            if self.is_recording:
                                self.csv_writer.writerow([
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], 
                                    dist_rel, dist_abs, speed, rpm, freq
                                ])
                    except ValueError:
                        pass
                else:
                    self.log(f"<< {line}")
                    self.process_incoming_params(line)
        except Exception as e:
            self.log(f"UART ERR: {str(e)}")

    def process_incoming_params(self, line):
        if ":" in line and "==" not in line:
            try:
                parts = line.split(":", 1) 
                name = parts[0].strip()
                val = parts[1].strip()
                
                val_f = float(val)
                name_lower = name.lower()
                
                if name == "forwardSpeed": self.fwd_speed.setText(str(int(val_f)))
                elif name == "backwardSpeed": self.bwd_speed.setText(str(int(val_f)))
                elif name == "accGlue": self.glue_acc.setText(str(int(val_f)))
                elif name == "calibGlue": self.cal_glue.setText(f"{val_f:.4f}")
                elif name_lower in ["frequency", "freq", "hz", "vfd frequency"]: 
                    self.lbl_vfd_freq.setText(f"{val_f:.2f}")
                    
                    if float(self.vfd_freq.text() or 0) != val_f:
                        self.vfd_freq.blockSignals(True)
                        self.vfd_freq.setText(str(int(val_f)))
                        self.vfd_freq.blockSignals(False)
                    
                    self.send_cmd(f"HZ {val_f}")
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
            
            self.csv_writer.writerow(["Timestamp", "Distance_REL", "Distance_ABS", "Speed", "RPM", "Frequency"])
            self.is_recording = True
            self.send_cmd("START_RECORDING")
            
            self.btn_start_rec.setEnabled(False)
            self.btn_stop_rec.setEnabled(True)
            self.log(f"RECORDING STARTED: {os.path.basename(self.current_full_path)}")
        except Exception as e:
            self.show_modern_error("File Error", str(e))

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
        self.send_cmd(f"forwardSpeed {self.fwd_speed.text() or 0}")
        self.send_cmd(f"backwardSpeed {self.bwd_speed.text() or 0}")
        self.send_cmd(f"glueAcc {self.glue_acc.text() or 0}")
        self.send_cmd(f"calGlue {self.cal_glue.text()}")
        self.send_cmd(f"HZ {self.vfd_freq.text() or 0}")

    def read_nvs(self):
        self.send_cmd("READNVS")