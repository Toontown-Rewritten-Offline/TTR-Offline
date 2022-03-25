@echo off
title MongoDB Server
cd ../../astron

"mongo\Server\5.0\bin\mongod.exe" --dbpath mongo\astrondb --logpath mongo\logs\mongodb.log --storageEngine wiredTiger
pause
