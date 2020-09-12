import os
import sys
import ctypes
import tkinter as tk
import tkinter.messagebox as tkMessage


class root(tk.Tk):
    step = 0

    def __init__(self):
        super().__init__()
        self.title("EFI Mounter")
        diskinfo = self.list_disk()
        self.label_str = tk.StringVar()
        self.label_str.set(diskinfo[6])
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(fill='x')
        self.label = tk.Label(self.label_frame, textvariable=self.label_str)
        self.label.pack(side='left')
        self.listbox = tk.Listbox(
            self, height=10, width=50, selectmode=tk.SINGLE)
        self.listbox.pack()
        for item in diskinfo[8:]:
            self.listbox.insert("end", item)
        self.button = tk.Button(self, text="Next", command=self.onClick)
        self.button.pack()
        self.mainloop()

    def get_path(self, filename):
        real_path = base_path + '\\' + os.path.basename(filename)
        return real_path

    def execCmd(self, cmd):
        r = os.popen(cmd, close_fds=True)
        text = r.read()
        r.close()
        return text

    def relaunch_explorer(self):
        kill_cmd = "taskkill /F /IM explorer.exe"
        os.system(kill_cmd)
        os.startfile("explorer.exe")

    def list_disk(self):
        self.command = "list disk"
        if not os.path.exists(self.get_path("tmp.txt")):
            with open(self.get_path("tmp.txt"), 'w') as f:
                f.write(self.command)
            result = self.execCmd("diskpart /s %s" % self.get_path("tmp.txt"))
            os.system("del %s" % self.get_path("tmp.txt"))
        else:
            print(
                "tmp.txt exists, aborted! Please consider rename tmp.txt to something else.")
            exit(1)
        result = result.splitlines()
        return result

    def list_part(self):
        self.command = "sel disk %d\nlist part" % self.sel_disk
        if not os.path.exists(self.get_path("tmp.txt")):
            with open(self.get_path("tmp.txt"), 'w') as f:
                f.write(self.command)
            result = self.execCmd("diskpart /s %s" % self.get_path("tmp.txt"))
            os.system("del %s" % self.get_path("tmp.txt"))
        else:
            print(
                "tmp.txt exists, aborted! Please consider rename tmp.txt to something else.")
            exit(1)
        result = result.splitlines()
        return result

    def mount_part(self):
        self.command = """sel disk %d
        sel part %d
        set id=ebd0a0a2-b9e5-4433-87c0-68b6b72699c7
        assign letter=z
        """ % (self.sel_disk, self.sel_part)
        if not os.path.exists(self.get_path("tmp.txt")):
            with open(self.get_path("tmp.txt"), 'w') as f:
                f.write(self.command)
            result = self.execCmd("diskpart /s %s" % self.get_path("tmp.txt"))
            os.system("del %s" % self.get_path("tmp.txt"))
        else:
            print(
                "tmp.txt exists, aborted! Please consider rename tmp.txt to something else.")
            exit(1)
        result = result.splitlines()
        self.relaunch_explorer()
        return result

    def unmount(self):
        try:
            self.sel_part = self.listbox.curselection()[0] + 1
        except IndexError:
            self.step = 1
            tkMessage.showerror(
                "Error", "You haven't select anything yet.\n您还没有选择分区")
            return
        self.command = """sel disk %d
        sel part %d
        remove letter z
        set id=c12a7328-f81f-11d2-ba4b-00a0c93ec93b override
        """ % (self.sel_disk, self.sel_part)
        if not os.path.exists(self.get_path("tmp.txt")):
            with open(self.get_path("tmp.txt"), 'w') as f:
                f.write(self.command)
            result = self.execCmd("diskpart /s %s" % self.get_path("tmp.txt"))
            os.system("del %s" % self.get_path("tmp.txt"))
        else:
            print(
                "tmp.txt exists, aborted! Please consider rename tmp.txt to something else.")
            exit(1)
        result = result.splitlines()
        tkMessage.showinfo(
            title="Result", message=result[10]+'\n'+result[12])

    def onClick(self):
        self.step += 1
        if self.step == 1:
            try:
                self.sel_disk = self.listbox.curselection()[0]
            except IndexError:
                self.step = 0
                tkMessage.showerror(
                    "Error", "You haven't select anything yet.\n您还没有选择磁盘")
                return
            part_info = self.list_part()
            self.label_str.set(part_info[8][2:])
            self.listbox.delete(0, "end")
            for item in part_info[10:]:
                self.listbox.insert("end", item)
            self.button.config(text="Mount")
            self.unmount_btn = tk.Button(
                self, text="Unmount", command=self.unmount)
            self.unmount_btn.pack()
        if self.step >= 2:
            try:
                self.sel_part = self.listbox.curselection()[0] + 1
            except IndexError:
                self.step = 1
                tkMessage.showerror(
                    "Error", "You haven't select anything yet.\n您还没有选择分区")
                return
            result = self.mount_part()
            tkMessage.showinfo(
                title="Result", message=result[10]+'\n'+result[12])


if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This script only works on Windows")

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        app = root()

    elif is_admin():
        base_path = os.path.dirname(__file__)
        app = root()

    else:
        # Get administrator permission
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
        else:  # in python2.x
            print("Python 2 is not supported.")
