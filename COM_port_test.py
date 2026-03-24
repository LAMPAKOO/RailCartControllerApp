import serial
import time

# Lista portów do sprawdzenia
porty_do_sprawdzenia = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6']
BAUD_RATE = 9600
wiadomosc_testowa = b"HELLO_RS232"

print("🔍 Rozpoczynam automatyczne poszukiwanie portu ze zwartymi pinami TX i RX...")
print("-" * 50)

znaleziony_port = None

for port in porty_do_sprawdzenia:
    print(f"Testuję {port}...", end=" ")
    
    try:
        # Próbujemy otworzyć port. Timeout=0.5s żeby test szedł szybko.
        ser = serial.Serial(port, BAUD_RATE, timeout=0.5)
        
        # Czyszczenie buforów
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wysyłamy wiadomość
        ser.write(wiadomosc_testowa)
        time.sleep(0.3) # Krótka pauza na powrót sygnału
        
        # Sprawdzamy czy coś wróciło
        if ser.in_waiting > 0:
            odebrane_dane = ser.read(ser.in_waiting)
            
            if odebrane_dane == wiadomosc_testowa:
                print("✅ SUKCES! Pętla zwrotna działa.")
                znaleziony_port = port
                ser.close()
                break # Zatrzymujemy pętlę - znaleźliśmy właściwy port!
            else:
                print("⚠️ Odebrano błędne dane (zakłócenia).")
        else:
            print("❌ Brak odpowiedzi (cisza).")
            
        ser.close()
        
    except serial.SerialException:
        print("❌ Niedostępny (nie istnieje lub jest używany przez inny program).")

print("-" * 50)

# Podsumowanie wyników
if znaleziony_port:
    print(f"🎉 GOTOWE! Twój port sprzętowy to: {znaleziony_port}")
    print("Możesz teraz usunąć zworkę i podłączyć swój konwerter do tego portu.")
else:
    print("Nie znaleziono żadnego portu działającego w pętli zwrotnej.")
    print("Upewnij się, że:")
    print("1. Zworka (kabelek) między pinami TX i RX na pewno dobrze styka.")
    print("2. Żaden inny program (np. PuTTY) nie blokuje portów w tle.")