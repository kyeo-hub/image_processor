import sys
from cx_Freeze import setup, Executable

# 应用程序信息
app_name = "ImageProcessor"
app_description = "一个批量重命名和压缩图片的工具"

# 依赖项
build_exe_options = {
    "packages": ["tkinter", "PIL", "os", "re", "argparse", "datetime"],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": [],
    "optimize": 1
}

# GUI应用程序的基类
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 这将隐藏控制台窗口

# 构建设置
setup(
    name=app_name,
    version="1.0.0",
    description=app_description,
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "image_processor.py",
            base=None,  # 控制台应用程序
            target_name="image_processor.exe"
        ),
        Executable(
            "image_processor_gui.py",
            base=base,  # GUI应用程序
            target_name="image_processor_gui.exe"
        )
    ]
)