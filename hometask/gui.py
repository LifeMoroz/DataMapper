import tkinter


class GUI:
    def __init__(self):
        self.width = 600
        self.height = 480
        self.root = self._create_root()
        self.info_frame = self._create_info_frame()
        self.work_frame = self._create_work_frame()
        self.selected_pc = tkinter.StringVar(self.info_frame)
        self.selected_adapter = tkinter.StringVar(self.info_frame)
        self._adapters_select = None

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

    def fill_info(self, choices, select_pc_callback, edit_pc_callback, ping_pc_callback, new_pc_callback, choose=None):
        var = self.selected_pc
        label = tkinter.Label(self.info_frame, text="Выберите действие")
        label.pack()
        var.set(choose or "Select PC")
        var.trace('w', select_pc_callback)
        if not choices:
            choices = ["Select PC"]
        option = tkinter.OptionMenu(self.info_frame, var, *choices)
        width = 114
        option.place(x=self.width / 2 - width - 5, y=20, width=width)
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")

        def edit():
            edit_pc_callback(self.selected_pc.get())

        tkinter.Button(self.info_frame, textvariable=buttontext, command=edit).place(x=self.width / 2 + 5, y=22)

        buttontext = tkinter.StringVar()
        buttontext.set("Ping")

        def ping():
            ping_pc_callback(self.selected_pc.get())

        tkinter.Button(self.info_frame, textvariable=buttontext, command=ping).place(x=self.width / 2 + 45, y=22)
        buttontext = tkinter.StringVar()

        buttontext.set("New")
        tkinter.Button(self.info_frame, textvariable=buttontext, command=new_pc_callback).place(x=self.width / 2 + 85, y=22)
        return var

    def add_adapters(self, choices, edit, ping, new, choose=None, pc=None):
        var = self.selected_adapter
        if self._adapters_select:
            self._adapters_select.destroy()
        var.set(choose or "Select Adapter")
        if not choices:
            choices = ["Select Adapter"]
        self._adapters_select = tkinter.OptionMenu(self.info_frame, var, *choices)
        width = 114
        self._adapters_select.place(x=self.width / 2 - width - 5, y=60, width=width)
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")

        def callback():
            edit(self.selected_adapter.get())

        tkinter.Button(self.info_frame, textvariable=buttontext, command=callback).place(x=self.width / 2 + 5, y=62)
        buttontext = tkinter.StringVar()
        buttontext.set("Ping")

        def callback():
            ping(self.selected_adapter.get())
        tkinter.Button(self.info_frame, textvariable=buttontext, command=callback).place(x=self.width / 2 + 45, y=62)
        buttontext = tkinter.StringVar()
        buttontext.set("New")

        def callback():
            if pc is not None:
                new(pc)
        tkinter.Button(self.info_frame, textvariable=buttontext, command=callback).place(x=self.width / 2 + 85, y=62)

    def edit_pc(self, pc, pc_edited, pc_deleted):
        self.clear_workspace()
        work_frame = self.work_frame
        label = tkinter.Label(work_frame, text="Укажите настройки")
        label.place(y=5, x=self.width / 2 - 60)
        p1 = tkinter.StringVar()
        p1.set(pc.title)

        # редактирование настройки №2
        label = tkinter.Label(work_frame, text="Title:", bg='gray')
        label.place(y=55, x=self.width / 2 - 97)

        def validate_title(x):
            if len(x) > 255:
                return False
            return True

        isOk = work_frame.register(validate_title)
        entry2 = tkinter.Entry(work_frame, textvariable=p1, validate='all', validatecommand=(isOk, '%P'))
        entry2.place(y=55, x=self.width / 2 - 65)

        # Отредактировали
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")

        def callback():
            pc_edited(pc, title=entry2.get())

        tkinter.Button(self.work_frame, textvariable=buttontext, command=callback).place(x=self.width / 2 - 40, y=80)
        # Отредактировали
        buttontext = tkinter.StringVar()
        buttontext.set("Delete")

        def callback():
            pc_deleted(pc)

        tkinter.Button(self.work_frame, textvariable=buttontext, command=callback).place(x=self.width / 2, y=80)

    def edit_adapter(self, adapter, edited, deleted):
        self.clear_workspace()
        work_frame = self.work_frame
        label = tkinter.Label(work_frame, text="Укажите настройки")
        label.place(y=5, x=self.width / 2 - 60)
        ip = tkinter.StringVar()
        ip.set(adapter.ip)

        # редактирование IP
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
        entry1 = tkinter.Entry(work_frame, textvariable=ip, validate='all', validatecommand=(isOk, '%P'))
        entry1.place(y=30, x=self.width / 2 - 65)

        # Отредактировали
        buttontext = tkinter.StringVar()
        buttontext.set("Edit")

        def callback():
            edited(adapter, ip=entry1.get(), pc=adapter.pc)

        tkinter.Button(self.work_frame, textvariable=buttontext, command=callback).place(x=self.width / 2 - 40, y=80)
        # Отредактировали
        buttontext = tkinter.StringVar()
        buttontext.set("Delete")

        def callback():
            deleted(adapter)

        tkinter.Button(self.work_frame, textvariable=buttontext, command=callback).place(x=self.width / 2, y=80)


    def clear_workspace(self):
        self.work_frame.destroy()
        self.work_frame = self._create_work_frame()

    def clear_infospace(self):
        self.info_frame.destroy()

    def update_info(self, choices, select_pc_callback, edit_pc_callback, ping_pc_callback, new_pc_callback, choose=None):
        self.clear_infospace()
        self.info_frame = self._create_info_frame()
        self.fill_info(choices, select_pc_callback, edit_pc_callback, ping_pc_callback, new_pc_callback, choose)

    def result(self, text):
        self.clear_workspace()
        label = tkinter.Label(self.work_frame, text=text)
        label.place(y=5, x=self.width / 2 - 60)

