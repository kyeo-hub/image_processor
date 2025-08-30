import subprocess
import sys
import os

def build_with_pyinstaller():
    # 为命令行版本创建spec文件
    cli_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['image_processor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='image_processor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX压缩以减少误报
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    # 为GUI版本创建spec文件
    gui_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['image_processor_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='image_processor_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX压缩以减少误报
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI应用不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    # 写入spec文件
    with open('image_processor_cli.spec', 'w') as f:
        f.write(cli_spec)
        
    with open('image_processor_gui.spec', 'w') as f:
        f.write(gui_spec)

    # 使用PyInstaller构建
    try:
        # 构建命令行版本
        subprocess.run([sys.executable, '-m', 'PyInstaller', 'image_processor_cli.spec'], check=True)
        print("命令行版本构建成功")
        
        # 构建GUI版本
        subprocess.run([sys.executable, '-m', 'PyInstaller', 'image_processor_gui.spec'], check=True)
        print("GUI版本构建成功")
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    except FileNotFoundError:
        print("未找到PyInstaller，请先安装: pip install pyinstaller")
        return False
        
    return True

if __name__ == "__main__":
    build_with_pyinstaller()