# -*- mode: python -*-
block_cipher = None
a = Analysis(['frevo/__init__.py'],
             pathex=['frevo'],
             binaries=[],
             datas=[
                    ('icon/*.png','icon')
                ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='Frevo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Frevo')
app = BUNDLE(coll,
             name='Frevo.app',
             icon='icon/icon.icns',
             info_plist={
                'LSUIElement': '1',
                'NSHighResolutionCapable': 'True',
                'CFBundleDisplayName': 'Frevo',
                'CFBundleDisplayName': 'Frevo',
                'CFBundleShortVersionString': '1.0.1',
                'NSHumanReadableCopyright': '2019, Mat Muller'
             },
             )
