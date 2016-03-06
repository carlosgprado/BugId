@ECHO OFF
SETLOCAL
NET SESSION >nul 2>&1
IF ERRORLEVEL 1 (
  ECHO - Must be run as administrator.
  EXIT /B 1
)
IF NOT "%GFlags:~0,0%" == "" (
  IF "%PROCESSOR_ARCHITECTURE%" == "AMD64" (
    SET GFlags=C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\gflags.exe
  ) ELSE (
    SET GFlags=C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\gflags.exe
  )
)
SET GFlags=%GFlags:"=%
IF NOT EXIST "%GFlags%" (
  ECHO - Cannot find Global Flags at "%GFlags%", please set the "GFlags" environment variable to the correct path.
  EXIT /B 1
)
IF "%~2" == "OFF" (
  ECHO * Disabling page heap for %1...
  "%GFlags%" -i %1 -FFFFFFFF >nul
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE (
  ECHO * Enabling page heap for %1...
  "%GFlags%" -i %1 -FFFFFFFF >nul
  IF ERRORLEVEL 1 GOTO :ERROR
  "%GFlags%" -i %1 +02109870 >nul
  IF ERRORLEVEL 1 GOTO :ERROR
)
EXIT /B 0

:ERROR
  ECHO - Error code %ERRORLEVEL%.
  EXIT /B %ERRORLEVEL%
