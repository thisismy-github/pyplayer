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