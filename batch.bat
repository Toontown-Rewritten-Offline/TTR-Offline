set pathtofolder=__pycache__

for /f %%d in ('dir /b "*"') do rd  /s /q "__pycache__"

pause