# -*- mode: python ; coding: utf-8 -*-


import os
version_file = 'version_info_main.txt'
block_cipher = None


a = Analysis(['..\\main.pyw'],
             pathex=[],
             binaries=[],
             datas=[('..\\themes', 'themes'),
                    ('include', 'plugins')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=['hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='pyplayer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          version=version_file if os.path.exists(version_file) else None,
          icon='..\\themes\\resources\\logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='release')
