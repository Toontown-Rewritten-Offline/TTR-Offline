@echo off
title Toontown Rewritten Dedicated Server
cd ../../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

%PPYTHON_PATH% -m toontown.toonbase.DedicatedServerStart
pause
