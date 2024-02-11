@echo off
set MULTIFILE=phase_3.5

goto :main

:main
set /p MULTIFILE="[ENTER] Multifile Name (Default: "phase_3.5.mf"): "
set /p answer="[CHOOSE] Do you want to extract or compile these phase files? (EXT/COM): "
if /i {%answer%}=={ext} (goto :ext)
if /i {%answer%}=={com} (goto :com)
echo [ERROR] You typed in something other than EXT or COM!
timeout 5
exit
echo.

:com
set /p answer="[ENTER] So this is "%MULTIFILE%" which will be compiled, right? (Y/N)? "
if /i {%answer%}=={y} (goto :yescomp)
if /i {%answer%}=={n} (goto :wrong)

:ext
set /p answer="[ENTER] So this is "%MULTIFILE%" which will be extracted, right? (Y/N)? "
if /i {%answer%}=={y} (goto :yesext)
if /i {%answer%}=={n} (goto :wrong)


echo [ERROR] You typed in something other than Y or N!
timeout 5

:wrong
set /p MULTIFILE="[ENTER] Ok, please enter the correct multifile name (Default: "phase_3.5.mf"): "

:yescomp
multify -c -f %MULTIFILE%.mf %MULTIFILE%
set /p answer="[ENTER] Finished! Would you like to compile/extract another multifile? (Y/N)? "
echo.
if /i {%answer%}=={y} (goto :main)
if /i {%answer%}=={n} (goto :done)

:yesext
multify -x -f %MULTIFILE%.mf
set /p answer="[ENTER] Finished! Would you like to compile/extract another multifile? (Y/N)? "
echo.
if /i {%answer%}=={y} (goto :main)
if /i {%answer%}=={n} (goto :done)

:next
set /p MULTIFILE="[ENTER] Ok, What is the name of your next multifile? (Default: "phase_3.5.mf"): "
echo.
set /p answer="[ENTER] So this is "%MULTIFILE%" which will be compiled, right? (Y/N)? "
if /i {%answer%}=={y} (goto :yes)
if /i {%answer%}=={n} (goto :done)

:done
echo [INFO] Exiting...
timeout 5