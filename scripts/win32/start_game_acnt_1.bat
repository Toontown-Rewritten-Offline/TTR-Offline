@echo off
title Toontown Rewritten Client
cd ../../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set TTR_PLAYCOOKIE=Username1
set TTR_GAMESERVER=127.0.0.1

%PPYTHON_PATH% -O -m toontown.toonbase.ToontownStart

pause
