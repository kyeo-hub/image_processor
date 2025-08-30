from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="image-processor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个批量重命名和压缩图片的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image-processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "image-processor=image_processor:main",
            "image-processor-gui=image_processor_gui:main",
        ],
    },
    package_data={
        "": ["README.md", "requirements.txt"],
    },
    include_package_data=True,
)