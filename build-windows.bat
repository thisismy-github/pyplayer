:: This batch file compiles PyPlayer to an executable on Windows.
:: Make sure you have all appropriate libraries in requirements.txt installed.
:: Read the readme.txt in /executable for more information.

pip install --upgrade pyinstaller

pyinstaller executable/main.spec --noconfirm --distpath executable/compiled --workpath executable/build
pyinstaller executable/launcher.spec --noconfirm --distpath executable/compiled --workpath executable/build
pyinstaller executable/updater.spec --noconfirm --distpath executable/compiled --workpath executable/build

copy .\executable\include .\executable\compiled\release
copy .\bin\ffmpeg.exe .\executable\compiled\release\ffmpeg.exe
copy .\executable\compiled\launcher\pyplayer.exe .\executable\compiled\release\pyplayer.exe
copy .\executable\compiled\updater.exe .\executable\compiled\release\updater.exe

@RD /S /Q ".\executable\compiled\launcher"
del ".\executable\compiled\updater.exe"

del ".\executable\compiled\release\Qt5Network.dll"
del ".\executable\compiled\release\Qt5Qml.dll"
del ".\executable\compiled\release\Qt5QmlModels.dll"
del ".\executable\compiled\release\Qt5Quick.dll"
del ".\executable\compiled\release\Qt5WebSockets.dll"