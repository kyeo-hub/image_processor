import os
import re
from PIL import Image
from PIL.ExifTags import TAGS
import argparse
from datetime import datetime


class ImageProcessor:
    def __init__(self, directory):
        self.directory = directory
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')

    def get_image_files(self):
        """获取目录中所有支持的图片文件"""
        image_files = []
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(self.supported_formats):
                image_files.append(filename)
        return sorted(image_files)

    def rename_images(self, pattern, start_number=1):
        """
        批量重命名图片
        
        Args:
            pattern: 命名模式，例如 "image_" 将文件重命名为 image_1, image_2, ...
            start_number: 起始编号
        """
        image_files = self.get_image_files()
        renamed_count = 0

        for i, filename in enumerate(image_files, start=start_number):
            old_path = os.path.join(self.directory, filename)
            file_extension = os.path.splitext(filename)[1].lower()
            
            # 根据模式生成新文件名
            new_filename = f"{pattern}{i}{file_extension}"
            new_path = os.path.join(self.directory, new_filename)
            
            # 如果新文件名已存在，则跳过
            if os.path.exists(new_path):
                print(f"跳过 {filename}，因为 {new_filename} 已存在")
                continue
                
            os.rename(old_path, new_path)
            print(f"重命名: {filename} -> {new_filename}")
            renamed_count += 1
            
        return renamed_count

    def rename_images_by_date(self):
        """
        根据图片的拍摄日期重命名图片
        """
        image_files = self.get_image_files()
        renamed_count = 0

        for filename in image_files:
            old_path = os.path.join(self.directory, filename)
            try:
                # 尝试获取拍摄日期
                date_str = self.get_capture_date(old_path)
                if date_str:
                    file_extension = os.path.splitext(filename)[1].lower()
                    new_filename = f"{date_str}{file_extension}"
                    new_path = os.path.join(self.directory, new_filename)
                    
                    # 检查文件名是否已存在
                    counter = 1
                    final_filename = new_filename
                    final_path = new_path
                    while os.path.exists(final_path) and final_path != old_path:
                        name_without_ext = os.path.splitext(new_filename)[0]
                        final_filename = f"{name_without_ext}_{counter}{file_extension}"
                        final_path = os.path.join(self.directory, final_filename)
                        counter += 1
                    
                    if final_path != old_path:
                        os.rename(old_path, final_path)
                        print(f"重命名: {filename} -> {final_filename}")
                        renamed_count += 1
                else:
                    print(f"无法获取 {filename} 的拍摄日期，跳过")
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")
                
        return renamed_count

    def get_capture_date(self, image_path):
        """
        从图片EXIF数据中获取拍摄日期
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            str: 格式化的日期字符串，如果无法获取则返回None
        """
        try:
            image = Image.open(image_path)
            exifdata = image.getexif()
            
            if exifdata is not None:
                for tag_id in exifdata:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal" or tag == "DateTime":
                        date_str = str(exifdata[tag_id])
                        # 转换为更友好的格式 YYYYMMDD_HHMMSS
                        dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                        return dt.strftime("%Y%m%d_%H%M%S")
            
            # 如果EXIF中没有日期信息，使用文件修改时间
            mtime = os.path.getmtime(image_path)
            dt = datetime.fromtimestamp(mtime)
            return dt.strftime("%Y%m%d_%H%M%S")
        except Exception:
            return None

    def compress_images(self, quality=85, max_width=1920, max_height=1080, output_dir=None):
        """
        批量压缩图片
        
        Args:
            quality: JPEG压缩质量 (1-100)
            max_width: 最大宽度
            max_height: 最大高度
            output_dir: 输出目录，如果为None则覆盖原文件
        """
        image_files = self.get_image_files()
        compressed_count = 0

        # 如果指定了输出目录但不存在，则创建它
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in image_files:
            try:
                old_path = os.path.join(self.directory, filename)
                file_extension = os.path.splitext(filename)[1].lower()
                
                # 获取原始文件大小
                old_size = os.path.getsize(old_path)
                
                # 确定输出路径
                if output_dir:
                    new_path = os.path.join(output_dir, filename)
                else:
                    new_path = old_path

                # 打开并处理图片
                with Image.open(old_path) as img:
                    # 获取原始尺寸
                    original_width, original_height = img.size
                    
                    # 计算新尺寸以保持宽高比
                    if original_width > max_width or original_height > max_height:
                        # 如果图片尺寸超过指定的最大尺寸，则进行缩放
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # 对于所有JPEG文件，强制重新压缩以确保文件大小减小
                    if file_extension in ['.jpg', '.jpeg']:
                        # 转换模式确保兼容性
                        if img.mode in ('RGBA', 'LA', 'P'):
                            # 如果有透明度，转换为RGB（会丢失透明度信息）
                            img = img.convert('RGB')
                        
                        # 保存压缩后的图片
                        img.save(new_path, 'JPEG', quality=quality, optimize=True)
                        
                    elif file_extension == '.png':
                        # PNG格式处理 - 转换为JPEG以实现更好的压缩效果
                        # 保存为PNG格式并尝试优化
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        
                        # 如果用户希望获得更小的文件大小，将PNG转换为JPEG
                        if quality < 100:  # 只有在指定压缩质量时才转换格式
                            # 处理透明背景 - 使用白色背景替换
                            if img.mode == 'RGBA':
                                # 创建白色背景
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                # 粘贴图像并使用alpha通道作为掩码
                                background.paste(img, mask=img.split()[-1])
                                img = background
                            
                            # 更改文件扩展名
                            new_filename = filename.replace('.png', '.jpg')
                            if output_dir:
                                new_path = os.path.join(output_dir, new_filename)
                            else:
                                new_path = os.path.join(os.path.dirname(new_path), new_filename)
                            
                            img.save(new_path, 'JPEG', quality=quality, optimize=True)
                        else:
                            # 保持PNG格式但进行优化
                            img.save(new_path, 'PNG', optimize=True)
                    else:
                        # 其他格式统一转换为JPEG以获得更好的压缩效果
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')
                        img.save(new_path, 'JPEG', quality=quality, optimize=True)
                
                # 获取新文件大小并计算压缩比
                new_size = os.path.getsize(new_path)
                ratio = (old_size - new_size) / old_size * 100 if old_size > 0 else 0
                
                # 显示压缩结果
                if old_path != new_path:
                    print(f"转换: {filename} -> {os.path.basename(new_path)} ({old_size} -> {new_size} 字节, 减少 {ratio:.1f}%)")
                else:
                    print(f"压缩: {filename} ({old_size} -> {new_size} 字节, 减少 {ratio:.1f}%)")
                compressed_count += 1
                    
            except Exception as e:
                print(f"压缩 {filename} 时出错: {e}")
        
        return compressed_count


def main():
    parser = argparse.ArgumentParser(description='批量重命名和压缩图片工具')
    parser.add_argument('directory', help='图片目录路径')
    parser.add_argument('--rename', help='重命名模式，例如 "image_"')
    parser.add_argument('--start-number', type=int, default=1, help='重命名起始编号')
    parser.add_argument('--rename-by-date', action='store_true', help='根据拍摄日期重命名')
    parser.add_argument('--compress', action='store_true', help='压缩图片')
    parser.add_argument('--quality', type=int, default=85, help='JPEG压缩质量 (1-100)')
    parser.add_argument('--max-width', type=int, default=1920, help='最大宽度')
    parser.add_argument('--max-height', type=int, default=1080, help='最大高度')
    parser.add_argument('--output-dir', help='压缩图片输出目录')

    args = parser.parse_args()

    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        return

    processor = ImageProcessor(args.directory)

    # 执行重命名操作
    if args.rename:
        count = processor.rename_images(args.rename, args.start_number)
        print(f"成功重命名 {count} 个文件")

    if args.rename_by_date:
        count = processor.rename_images_by_date()
        print(f"根据日期成功重命名 {count} 个文件")

    # 执行压缩操作
    if args.compress:
        count = processor.compress_images(
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
            output_dir=args.output_dir
        )
        print(f"成功压缩 {count} 个文件")


if __name__ == "__main__":
    main()