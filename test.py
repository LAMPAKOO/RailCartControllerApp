import tkinter as tk
import subprocess
import os
import os
import platform

import os

def pokaz_klawiature(event):
    try:
        sciezka_tabtip = r"C:\Program Files\Common Files\microsoft shared\ink\TabTip.exe"
        os.startfile(sciezka_tabtip)
    except Exception as e:
        print(f"Nie udało się uruchomić klawiatury: {e}")
# Tworzenie głównego okna
root = tk.Tk()
root.title("Test klawiatury")
root.geometry("400x200")

# Etykieta
label = tk.Label(root, text="Kliknij w pole poniżej:")
label.pack(pady=10)

# Pole tekstowe
pole_tekstowe = tk.Entry(root, font=("Arial", 14))
pole_tekstowe.pack(pady=10)

# Bindowanie zdarzenia <FocusIn> (gdy pole staje się aktywne) 
# lub <Button-1> (kliknięcie lewym przyciskiem myszy)
pole_tekstowe.bind("<FocusIn>", pokaz_klawiature)

root.mainloop()