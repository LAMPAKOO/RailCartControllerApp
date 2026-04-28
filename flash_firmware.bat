@echo off
title ESP32 Auto Flash Tool (Auto COM Detect)
color 0A

echo ==========================================
echo        ESP32 AUTO FLASH TOOL
echo        (Auto COM Port Detection)
echo ==========================================
echo.

set BAUD=921600
set FILE=RailCartController.ino.merged.bin

if not exist "%FILE%" (
    echo [ERROR] Firmware file not found: %FILE%
    pause
    exit /b
)

echo Searching for ESP32 COM port...
echo.

set PORT=

for /f "tokens=1,2 delims=:" %%A in ('wmic path Win32_SerialPort get DeviceID^,Name ^| findstr /i "USB CH340 CP210 FTDI ESP32"') do (
    set PORT=%%A
)

if "%PORT%"=="" (
    echo [ERROR] No ESP32 COM port found!
    echo Make sure device is connected.
    pause
    exit /b
)

echo Detected Port: %PORT%
echo Firmware: %FILE%
echo Baud: %BAUD%
echo.

echo ------------------------------------------
echo Step 1: Erasing flash memory...
echo ------------------------------------------
esptool --chip esp32 --port %PORT% --baud %BAUD% erase_flash

if errorlevel 1 (
    echo.
    echo [ERROR] Flash erase failed!
    pause
    exit /b
)

echo.
echo ------------------------------------------
echo Step 2: Uploading firmware...
echo ------------------------------------------
esptool --chip esp32 --port %PORT% --baud %BAUD% write_flash 0x0 "%FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] Flash upload failed!
    pause
    exit /b
)

echo.
echo ==========================================
echo        FLASH COMPLETED SUCCESSFULLY
echo ==========================================
pause