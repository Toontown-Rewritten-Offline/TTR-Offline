@echo off
title Astron Server
cd ../../astron
goto :main

:main
set /p answer="[DATABASE] Do you want to use YAML or MongoDB? (YML/MDB): "
if /i {%answer%}=={YML} (goto :YML)
if /i {%answer%}=={MDB} (goto :MDB)

echo [ERROR] Neither databse was chosen...
goto :main

:YML
start astrond --loglevel info config/astrond.yml
exit

:MDB
start mongo\Server\5.0\bin\mongod.exe --dbpath mongo\astrondb --logpath mongo\logs\mongodb.log --storageEngine wiredTiger
start astrond --loglevel info config/astrond-mongo.yml
exit