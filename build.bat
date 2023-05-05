@echo off

:: Compila los archivos de código fuente en un archivo ejecutable
pyinstaller --onefile --clean main.py

:: Copia el archivo ejecutable a una ubicación específica
xcopy dist\main.exe C:\Program Files\MyProgram\ /y

:: Limpia los archivos intermedios
rmdir build /s /q
rmdir dist /s /q
del main.spec

:: Finaliza el script
echo Done.
pause