@echo off

REM Open the first command prompt window and store its PID
start /B cmd /C "python MTserver.py"
set "PID1=%ERRORLEVEL%"

REM Open the second command prompt window and store its PID
start /B cmd /C "python MTclient.py"
set "PID2=%ERRORLEVEL%"

REM Wait for all command prompt windows to close
:LOOP
timeout /t 1 /nobreak >nul
tasklist /FI "PID eq %PID1%" | find /i "cmd.exe" >nul && goto LOOP
tasklist /FI "PID eq %PID2%" | find /i "cmd.exe" >nul && goto LOOP

REM All windows are closed, exit the batch file
exit
