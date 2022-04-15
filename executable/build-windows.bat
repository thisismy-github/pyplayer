:: This batch file compiles PyPlayer to an executable on Windows.
:: Make sure you have all appropriate libraries in requirements.txt installed.
:: View readme.txt for more information.

call ..\venv\scripts\activate.bat
pip install --upgrade pyinstaller

pyinstaller main.spec --noconfirm --distpath  compiled --workpath  build
pyinstaller updater.spec --noconfirm --distpath compiled --workpath  build

copy ..\bin\ffmpeg.exe compiled\release\plugins\ffmpeg.exe
copy compiled\release\certifi\cacert.pem compiled\release\PyQt5\cacert.pem
@RD /S /Q "compiled\release\certifi"
del compiled\release\PIL\_imagingtk* /s /q
del compiled\release\PIL\_webp* /s /q

for /F "tokens=*" %%A in (exclude.txt) do (
	IF EXIST "compiled\release\%%A\*" (rmdir "compiled\release\%%A" /s /q) ELSE (del "compiled\release\%%A" /s /q)
)

move compiled\updater.exe compiled\release\PyQt5\updater.exe
move compiled\release\*.pyd compiled\release\PyQt5
move compiled\release\*.dll compiled\release\PyQt5
move compiled\release\PyQt5\python*.dll compiled\release
move compiled\release\python3.dll compiled\release\PyQt5\python3.dll
ren compiled\release\PyQt5 pyqt5
