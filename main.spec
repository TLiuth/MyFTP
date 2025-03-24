# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all PIL-related files and dependencies
pil_datas, pil_binaries, pil_hiddenimports = collect_all('PIL')

a = Analysis(
    ['main.py'],
    pathex=['/Documents/Redes de Computadores/MyFTP'],  # Add your project path here
    binaries=[] + pil_binaries,  # Include PIL binaries
    datas=[('images/*', 'images'), ('gui/*', 'gui'), ('users/user_data.bin', 'users')] + pil_datas,  # Include PIL data files
    hiddenimports=[] + pil_hiddenimports,  # Include PIL hidden imports
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MyFTP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
