# [Windows_EFI_Mounter](https://github.com/the-eric-kwok/Windows_EFI_Mounter)
一个 Python 编写的在 Windows 下挂载 EFI 分区的小工具。

## 用法
```
python3 EFI_Mounter.py
```

或者在[此页面](https://github.com/the-eric-kwok/Windows_EFI_Mounter/releases)中下载可执行文件来运行。

**EFI_Mounter.zip 和 EFI_Mounter.exe 有什么区别吗？**
EFI_Mounter.exe 是一个压缩过的单个可执行文件，需要先把自己解压缩到临时文件夹才能运行，所以 EFI_Mounter.zip 解压缩后实际上有更快的启动速度，但是会占用更多的磁盘空间。请自行选择。

## 构建
首先安装 pyinstaller
```
pip3 install pyinstaller
```

然后运行 `pyinstaller -F --uac-admin EFI_Mounter.py` 来构建单个可执行文件，或 `pyinstaller -w --uac-admin EFI_Mounter.py` 来构建非压缩版程序。

你将会在 `dist` 文件夹中找到你构建的程序。