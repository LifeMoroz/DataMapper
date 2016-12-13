import tkinter


class GUI:
    def __init__(self):
        self.width = 600
        self.height = 480
        self.root = self._create_root()
        self.info_frame = self._create_info_frame()
        self.work_frame = self._create_work_frame()
        self.pc_selected = tkinter.StringVar(self.info_frame)

    def _create_root(self):
        root = tkinter.Tk()
        root.wm_title("GUI стенд")
        root.resizable(width=False, height=False)
        root.geometry('{}x{}'.format(self.width, self.height))
        return root

    def _create_info_frame(self):
        work_frame = tkinter.Frame(self.root)
        work_frame.place(width=self.width, height=180)
        return work_frame

    def _create_work_frame(self):
        work_frame = tkinter.Frame(self.root, bg='gray')
        work_frame.place(width=self.width, height=300, y=self.height-300)
        return work_frame

    def fill_info(self, choices, select_pc_callback, choose=None):
        var = self.pc_selected
        label = tkinter.Label(self.info_frame, text="Выберите действие")
        label.pack()
        var.set(choose or "Select PC")
        option = tkinter.OptionMenu(self.info_frame, var, *choices)
        width = 114
        option.place(x=self.width / 2 - width - 5, y=20, width=width)
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")
        tkinter.Button(self.info_frame, textvariable=buttontext, command=select_pc_callback).place(x=self.width / 2 + 5, y=22)
        return var

    def edit_pc(self, pc, pc_edited):
        self.clear_workspace()
        work_frame = self.work_frame
        label = tkinter.Label(work_frame, text="Укажите настройки")
        label.place(y=5, x=self.width / 2 - 60)
        ip = tkinter.StringVar()
        ip.set(pc.ip)

        label = tkinter.Label(work_frame, text="IP:", bg='gray')
        label.place(y=30, x=self.width / 2 - 85)

        def validate_ipv4(x):
            match = tkinter.re.match('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', x)
            if match is None:
                return False
            for ip_part in match.groups():
                if int(ip_part) > 255:
                    return False
            return bool(match)

        isOk = work_frame.register(validate_ipv4)
        entry = tkinter.Entry(work_frame, textvariable=ip, validate='all', validatecommand=(isOk, '%P'))
        entry.place(y=30, x=self.width / 2 - 65)
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")

        def callback():
            pc_edited(pc, ip=entry.get())

        tkinter.Button(self.root, textvariable=buttontext, command=callback).place(x=self.width / 2 -20, y=50)

    def clear_workspace(self):
        self.work_frame.destroy()
        self.work_frame = self._create_work_frame()

    def clear_infospace(self):
        self.info_frame.destroy()

    def update_info(self, choices, select_pc_callback, choose=None):
        self.clear_infospace()
        self.info_frame = self._create_info_frame()
        self.fill_info(choices, select_pc_callback, choose)
