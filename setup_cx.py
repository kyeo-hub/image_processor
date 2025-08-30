import sys
import os
from cx_Freeze import setup, Executable

# 应用程序信息
app_name = "ImageProcessor"
app_description = "一个批量重命名和压缩图片的工具"

# 根据平台设置不同的基础配置
if sys.platform == "win32":
    base_cli = None  # Windows控制台应用程序
    base_gui = "Win32GUI"  # Windows GUI应用程序（无控制台窗口）
    extension = ".exe"
elif sys.platform == "darwin":  # macOS
    base_cli = None  # macOS控制台应用程序
    base_gui = None  # macOS GUI应用程序通常也需要控制台以显示错误
    extension = ""
else:  # Linux和其他Unix系统
    base_cli = None
    base_gui = None
    extension = ""

# 获取当前Python版本信息
python_version = f"{sys.version_info.major}{sys.version_info.minor}"

# 构建选项
build_exe_options = {
    "packages": ["tkinter", "PIL", "os", "re", "argparse", "datetime"],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": include_files,
    "optimize": 1,
    "silent": False,
}

# 对于Windows平台，查找并包含Python DLL
if sys.platform == "win32":
    python_dir = os.path.dirname(sys.executable)
    python_dll = f"python{python_version}.dll"
    python_dll_path = os.path.join(python_dir, python_dll)
    
    if os.path.exists(python_dll_path):
        include_files.append((python_dll_path, python_dll))
        print(f"包含Python DLL: {python_dll}")
    else:
        print(f"未找到Python DLL: {python_dll_path}")

# 构建设置
setup(
    name=app_name,
    version="1.0.0",
    description=app_description,
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "image_processor.py",
            base=base_cli,
            target_name=f"image_processor{extension}"
        ),
        Executable(
            "image_processor_gui.py",
            base=base_gui,
            target_name=f"image_processor_gui{extension}"
        )
    ]
)