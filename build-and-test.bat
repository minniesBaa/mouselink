@echo off
echo ---    build mouselink    ---
start /WAIT /MIN CMD /C "py -m build"
echo --- uninstall old version ---
start /WAIT /MIN CMD /C "py -m pip uninstall mouselink -y"
echo ---  finding wheel file   ---
set "SEARCH_DIR=dist"
for /f "delims=" %%F in ('dir /b /a-d /od "%SEARCH_DIR%\*.whl" 2^>nul') do (
    set "latest_file=%%F"
)
echo --- installing wheel file ---
start /WAIT /MIN CMD /C "py -m pip install dist\%latest_file% --no-deps --force-reinstall"
pause