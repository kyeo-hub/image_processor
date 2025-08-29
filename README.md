# 图片批量处理工具

这个工具可以批量重命名和压缩图片文件。

## 功能特性

1. 批量重命名图片文件（支持按序号或拍摄日期命名）
2. 批量压缩图片以减小文件大小
3. 支持多种图片格式（JPEG, PNG, BMP, TIFF, WebP）
4. 提供命令行和图形界面两种使用方式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行版本

#### 基本语法

```bash
python image_processor.py [目录路径] [选项]
```

#### 重命名功能

1. 按序号重命名图片：
```bash
python image_processor.py ./images --rename "photo_"
```
这会将图片重命名为 photo_1.jpg, photo_2.jpg, ...

2. 按拍摄日期重命名图片：
```bash
python image_processor.py ./images --rename-by-date
```
这会根据图片的拍摄日期将其重命名为 20231201_123045.jpg 格式

#### 压缩功能

1. 压缩图片：
```bash
python image_processor.py ./images --compress
```

2. 指定压缩质量和其他参数：
```bash
python image_processor.py ./images --compress --quality 75 --max-width 1280 --max-height 720
```

3. 压缩后保存到指定目录：
```bash
python image_processor.py ./images --compress --output-dir ./compressed
```

#### 组合操作

重命名并压缩：
```bash
python image_processor.py ./images --rename "IMG_" --compress
```

### 图形界面版本

运行图形界面版本：
```bash
python image_processor_gui.py
```

## 选项说明

- `directory`: 图片目录路径（必需）
- `--rename PATTERN`: 重命名模式，例如 "image_" 将文件重命名为 image_1, image_2, ...
- `--start-number NUMBER`: 重命名起始编号，默认为1
- `--rename-by-date`: 根据拍摄日期重命名
- `--compress`: 压缩图片
- `--quality QUALITY`: JPEG压缩质量 (1-100)，默认为85
- `--max-width WIDTH`: 最大宽度，默认为1920
- `--max-height HEIGHT`: 最大高度，默认为1080
- `--output-dir DIRECTORY`: 压缩图片输出目录

## 压缩效果说明

压缩功能会对图片进行以下处理以减小文件大小：

1. 对尺寸超过指定大小的图片进行缩放
2. 对JPEG图片重新编码以优化压缩率
3. 对PNG图片进行特殊处理：
   - 当指定质量参数小于100时，将PNG转换为JPEG格式以获得更好压缩效果
   - 当质量参数为100时，保持PNG格式但进行优化
4. 其他格式图片转换为JPEG以获得更好压缩效果

如果发现压缩后文件大小没有明显变化，请尝试：
1. 降低质量参数(--quality)，例如设置为75或更低
2. 减小最大宽高限制(--max-width 和 --max-height)
3. 检查原图是否已经是高度压缩的格式

## 注意事项

- PNG文件在转换为JPEG时会丢失透明度信息，透明区域将变为白色
- 压缩是不可逆的，请在重要图片上使用前先备份
- 对于已经高度压缩的图片，进一步压缩可能不会显著减小文件大小

## 发布到PyPI

1. 安装打包工具：
```bash
pip install setuptools wheel twine
```

2. 构建发布包：
```bash
python setup.py sdist bdist_wheel
```

3. 上传到PyPI：
```bash
twine upload dist/*
```

## GitHub Actions 自动发布

当您在GitHub上推送一个以`v`开头的标签（如`v1.0.0`）时，GitHub Actions会自动：

1. 创建GitHub Release
2. 在Windows、macOS和Linux上构建可执行文件
3. 将构建的可执行文件作为Release Assets上传

### 创建新版本的步骤：

1. 更新代码并提交所有更改
2. 创建并推送标签：
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Actions会自动开始构建和发布流程