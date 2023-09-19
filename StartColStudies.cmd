@ECHO OFF
REM
REM start the ColStudies Application Server
REM
ECHO --------------------------------------
ECHO --                                  --
ECHO -- ColStudies Application Server    --
ECHO --                                  --
ECHO --------------------------------------
ECHO.
ECHO Starting default browser with application address
explorer "http://127.0.0.1:5555/" 

ECHO Starting application server
cd web
python colstudies.py

ECHO finished.
pause
