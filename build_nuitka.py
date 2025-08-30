import subprocess
import sys
import os

def build_with_nuitka():
    try:
        # 构建命令行版本
        print("正在构建命令行版本...")
        subprocess.run([
            sys.executable, "-m", "nuitka", 
            "--standalone",           # 独立模式
            "--onefile",              # 单文件
            "--enable-plugin=tk-inter", # 启用tkinter插件
            "--windows-disable-console", # 对于GUI版本需要禁用控制台
            "image_processor.py"
        ], check=True)
        print("命令行版本构建成功")
        
        # 构建GUI版本
        print("正在构建GUI版本...")
        subprocess.run([
            sys.executable, "-m", "nuitka",
            "--standalone",           # 独立模式
            "--onefile",              # 单文件
            "--enable-plugin=tk-inter", # 启用tkinter插件
            "--windows-disable-console", # 禁用控制台窗口
            "image_processor_gui.py"
        ], check=True)
        print("GUI版本构建成功")
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    except FileNotFoundError:
        print("未找到Nuitka，请先安装: pip install nuitka")
        return False
        
    return True

if __name__ == "__main__":
    build_with_nuitka()