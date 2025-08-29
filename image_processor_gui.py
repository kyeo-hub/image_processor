import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from image_processor import ImageProcessor


class ImageProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("图片批量处理工具")
        self.root.geometry("600x500")
        
        self.directory = tk.StringVar()
        self.rename_pattern = tk.StringVar(value="image_")
        self.start_number = tk.IntVar(value=1)
        self.quality = tk.IntVar(value=85)
        self.max_width = tk.IntVar(value=1920)
        self.max_height = tk.IntVar(value=1080)
        self.output_dir = tk.StringVar()
        
        self.rename_by_date = tk.BooleanVar()
        self.rename_enabled = tk.BooleanVar()
        self.compress_enabled = tk.BooleanVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 目录选择
        dir_frame = ttk.LabelFrame(main_frame, text="选择目录", padding="10")
        dir_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Entry(dir_frame, textvariable=self.directory, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(dir_frame, text="浏览", command=self.browse_directory).grid(row=0, column=1)
        
        # 重命名选项
        rename_frame = ttk.LabelFrame(main_frame, text="重命名选项", padding="10")
        rename_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        
        ttk.Checkbutton(rename_frame, text="启用重命名", variable=self.rename_enabled).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(rename_frame, text="命名模式:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Entry(rename_frame, textvariable=self.rename_pattern, state=tk.DISABLED).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(rename_frame, text="起始编号:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(rename_frame, textvariable=self.start_number, state=tk.DISABLED, width=10).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Checkbutton(rename_frame, text="根据拍摄日期重命名", variable=self.rename_by_date, state=tk.DISABLED).grid(row=5, column=0, sticky=tk.W)
        
        # 压缩选项
        compress_frame = ttk.LabelFrame(main_frame, text="压缩选项", padding="10")
        compress_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), pady=(0, 10), padx=(10, 0))
        
        ttk.Checkbutton(compress_frame, text="启用压缩", variable=self.compress_enabled).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(compress_frame, text="质量 (1-100):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Entry(compress_frame, textvariable=self.quality, state=tk.DISABLED, width=10).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(compress_frame, text="最大宽度:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(compress_frame, textvariable=self.max_width, state=tk.DISABLED, width=10).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(compress_frame, text="最大高度:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(compress_frame, textvariable=self.max_height, state=tk.DISABLED, width=10).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(compress_frame, text="输出目录:").grid(row=7, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Entry(compress_frame, textvariable=self.output_dir, state=tk.DISABLED).grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        ttk.Button(compress_frame, text="浏览", command=self.browse_output_directory, state=tk.DISABLED).grid(row=9, column=0, sticky=tk.W)
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="开始处理", command=self.process_images).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="退出", command=self.root.quit).grid(row=0, column=1)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        dir_frame.columnconfigure(0, weight=1)
        rename_frame.columnconfigure(0, weight=1)
        compress_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 绑定事件
        self.rename_enabled.trace('w', self.toggle_rename_options)
        self.compress_enabled.trace('w', self.toggle_compress_options)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)
            
    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)
            
    def toggle_rename_options(self, *args):
        state = 'normal' if self.rename_enabled.get() else 'disabled'
        self.rename_pattern.set("image_" if not self.rename_pattern.get() else self.rename_pattern.get())
        # 注意：在实际的tkinter中，需要通过配置每个控件的状态来实现
        # 这里简化处理，实际应用中需要逐个设置控件状态
        
    def toggle_compress_options(self, *args):
        state = 'normal' if self.compress_enabled.get() else 'disabled'
        # 同上，简化处理
        
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def process_images(self):
        if not self.directory.get():
            messagebox.showerror("错误", "请选择图片目录")
            return
            
        if not os.path.isdir(self.directory.get()):
            messagebox.showerror("错误", "选择的目录不存在")
            return
            
        if not self.rename_enabled.get() and not self.compress_enabled.get():
            messagebox.showwarning("警告", "请选择至少一个操作（重命名或压缩）")
            return
            
        try:
            processor = ImageProcessor(self.directory.get())
            
            # 执行重命名操作
            if self.rename_enabled.get():
                if self.rename_by_date.get():
                    count = processor.rename_images_by_date()
                    self.log(f"根据日期成功重命名 {count} 个文件")
                else:
                    count = processor.rename_images(self.rename_pattern.get(), self.start_number.get())
                    self.log(f"成功重命名 {count} 个文件")
                    
            # 执行压缩操作
            if self.compress_enabled.get():
                output_dir = self.output_dir.get() if self.output_dir.get() else None
                count = processor.compress_images(
                    quality=self.quality.get(),
                    max_width=self.max_width.get(),
                    max_height=self.max_height.get(),
                    output_dir=output_dir
                )
                self.log(f"成功压缩 {count} 个文件")
                
            messagebox.showinfo("完成", "图片处理完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出现错误:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()