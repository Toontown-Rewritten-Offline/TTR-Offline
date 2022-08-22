@echo off
title Toontown Rewritten AI Service
cd ../../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set MAX_CHANNELS=999999
set STATE_SERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENT_LOGGER_IP=127.0.0.1:7197
set DISTRICT_NAME=Developers Dreams
set BASE_CHANNEL=420000000

:main
%PPYTHON_PATH% -m toontown.ai.ServiceStartAI --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATE_SERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENT_LOGGER_IP% ^
               --district-name "%DISTRICT_NAME%"
goto :main
pause