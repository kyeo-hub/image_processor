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
        """根据拍摄日期重命名图片"""
        image_files = self.get_image_files()
        renamed_count = 0

        for filename in image_files:
            old_path = os.path.join(self.directory, filename)
            
            try:
                # 获取图片的EXIF信息
                image = Image.open(old_path)
                exifdata = image.getexif()
                
                if exifdata is not None:
                    # 查找拍摄日期
                    for tag_id in exifdata:
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == "DateTime":
                            date_taken = exifdata.get(tag_id)
                            if date_taken:
                                # 解析日期并格式化为文件名
                                dt = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
                                new_filename = dt.strftime("%Y%m%d_%H%M%S") + os.path.splitext(filename)[1].lower()
                                new_path = os.path.join(self.directory, new_filename)
                                
                                # 如果新文件名已存在，则添加序号
                                counter = 1
                                original_new_filename = new_filename
                                while os.path.exists(new_path):
                                    name, ext = os.path.splitext(original_new_filename)
                                    new_filename = f"{name}_{counter}{ext}"
                                    new_path = os.path.join(self.directory, new_filename)
                                    counter += 1
                                    
                                os.rename(old_path, new_path)
                                print(f"根据日期重命名: {filename} -> {new_filename}")
                                renamed_count += 1
                                break
                    else:
                        print(f"跳过 {filename}，未找到拍摄日期信息")
                else:
                    print(f"跳过 {filename}，无EXIF信息")
                    
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")
                continue
                
        return renamed_count

    def compress_images(self, quality=85, max_width=1920, max_height=1080, output_dir=None):
        """
        批量压缩图片
        
        Args:
            quality: 压缩质量 (1-100)
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
            old_path = os.path.join(self.directory, filename)
            file_extension = os.path.splitext(filename)[1].lower()
            
            # 确定输出路径
            if output_dir:
                new_path = os.path.join(output_dir, filename)
            else:
                new_path = old_path

            try:
                # 打开图片
                with Image.open(old_path) as image:
                    # 转换RGBA和P模式的图片以支持JPEG格式
                    if image.mode in ('RGBA', 'P') and file_extension in ('.jpg', '.jpeg'):
                        # 创建白色背景
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        if image.mode == 'P':
                            # 如果是调色板模式，先转换为RGBA
                            image = image.convert('RGBA')
                        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                        image = background

                    # 计算新尺寸以保持宽高比
                    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # 保存压缩后的图片
                    if file_extension in ('.jpg', '.jpeg'):
                        image.save(new_path, 'JPEG', quality=quality, optimize=True)
                    elif file_extension == '.webp':
                        image.save(new_path, 'WebP', quality=quality, method=6)
                    else:
                        # 对于PNG等其他格式，使用默认设置
                        image.save(new_path, optimize=True)
                    
                print(f"压缩: {filename}")
                compressed_count += 1
                
            except Exception as e:
                print(f"压缩 {filename} 时出错: {e}")
                continue
                
        return compressed_count


def main():
    parser = argparse.ArgumentParser(description='图片批量处理工具')
    parser.add_argument('directory', help='图片目录路径')
    parser.add_argument('--rename', action='store_true', help='启用重命名功能')
    parser.add_argument('--pattern', default='image_', help='重命名模式')
    parser.add_argument('--start-number', type=int, default=1, help='起始编号')
    parser.add_argument('--rename-by-date', action='store_true', help='根据拍摄日期重命名')
    parser.add_argument('--compress', action='store_true', help='启用压缩功能')
    parser.add_argument('--quality', type=int, default=85, help='压缩质量 (1-100)')
    parser.add_argument('--max-width', type=int, default=1920, help='最大宽度')
    parser.add_argument('--max-height', type=int, default=1080, help='最大高度')
    parser.add_argument('--output-dir', help='输出目录')

    args = parser.parse_args()

    if not args.rename and not args.compress:
        print("请至少选择一个操作（重命名或压缩）")
        return

    if not os.path.isdir(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        return

    processor = ImageProcessor(args.directory)

    # 执行重命名操作
    if args.rename:
        if args.rename_by_date:
            count = processor.rename_images_by_date()
            print(f"根据日期成功重命名 {count} 个文件")
        else:
            count = processor.rename_images(args.pattern, args.start_number)
            print(f"成功重命名 {count} 个文件")

    # 执行压缩操作
    if args.compress:
        output_dir = args.output_dir if args.output_dir else None
        count = processor.compress_images(
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
            output_dir=output_dir
        )
        print(f"成功压缩 {count} 个文件")


if __name__ == "__main__":
    main()