@echo off
echo Building EXE...
pyinstaller --onefile --windowed --icon="assets/icon.ico" __main__.spec
echo Build Complete!
echo Check dist/ for PyTris.exe
pause