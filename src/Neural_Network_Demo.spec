# Neural_Network_Demo.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\brian\\OneDrive\\Desktop\\WRTG_3030_Neural_Net\\src'],
    binaries=[
        ('C:\\Users'\brian\\OneDrive\\Desktop\\WRTG_3030_Neural_Net\\src\\dist\\Neural_Network_Demo\\_internal\\python311.dll', '.')
    ],
    datas=[
        ('components\\mainMenu.html', 'components'),
        ('components\\thePlan.html', 'components'),
        ('components\\whyCare.html', 'components'),
        ('components\\trainingSim.html', 'components'),
        ('components\\transformerSim.html', 'components'),
        ('components\\gptSimUI.html', 'components'),
        ('components\\takeaways.html', 'components'),
        ('data\\foodCritera.txt', 'data'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Neural_Network_Demo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Neural_Network_Demo'
)
