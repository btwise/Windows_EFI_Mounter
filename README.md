# [Windows_EFI_Mounter](https://github.com/the-eric-kwok/Windows_EFI_Mounter)
A python GUI program to help you mount your EFI partition on Windows.

[简体中文](https://github.com/the-eric-kwok/Windows_EFI_Mounter/blob/master/README_zhCN.md)

## Usage
```
python3 EFI_Mounter.py
```

Or download release executable file from [here](https://github.com/the-eric-kwok/Windows_EFI_Mounter/releases)

**What is the difference of EFI_Mounter.zip and EFI_Mounter.exe?**
The EFI_Mounter.exe is a standalone file and need to extract itself before running, so the EFI_Mounter.zip has a better launch speed since it's pre-extracted. Just take your pick.

## Build
First install pyinstaller
```
pip3 install pyinstaller
```

then run `pyinstaller -F --uac-admin EFI_Mounter.py` for standalone executable file, or `pyinstaller -w --uac-admin EFI_Mounter.py` otherwise.

You will get your build in `dist` folder.