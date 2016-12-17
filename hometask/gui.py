import copy
import tkinter
from tkinter.ttk import Separator


class GUI:
    def __init__(self):
        self.width = 600
        self.height = 480
        self.root = self._create_root()
        self.info_frame = self._create_info_frame()
        self.work_frame = self._create_work_frame()
        self.detail_frame = self._create_detail_info_frame()

    def _create_root(self):
        root = tkinter.Tk()
        root.wm_title("Журнал событий")
        root.resizable(width=False, height=False)
        root.geometry('{}x{}'.format(self.width, self.height))
        return root

    def _create_info_frame(self):
        work_frame = tkinter.Frame(self.root)
        work_frame.place(width=self.width/2, height=180)
        Separator(self.root, orient=tkinter.HORIZONTAL).place(y=180, width=self.width, height=1)
        for i in range(10):
            work_frame.grid_columnconfigure(i, weight=1)
        return work_frame

    def _create_work_frame(self):
        work_frame = tkinter.Frame(self.root)
        work_frame.place(width=self.width, height=299, y=self.height-299)
        return work_frame

    def _create_detail_info_frame(self):
        work_frame = tkinter.Frame(self.root, bg='white')
        work_frame.place(width=self.width/2, height=180, x=self.width/2)
        return work_frame

    def fill_info(self, filters, current=None):
        for nrow, item in enumerate(filters):
            filter_name, values, callback = item
            b = tkinter.Label(self.info_frame, text=filter_name).grid(row=nrow, column=0)
            self.type = tkinter.StringVar(self.info_frame)
            self.type.set(current or 'ALL')
            tkinter.OptionMenu(self.info_frame, self.type,  'ALL', *values, command=callback).grid(row=nrow, column=1, columnspan=2, sticky='we')

    def fill_worker(self, events, fields):
        self.clear_workspace()
        for j, attr in enumerate(fields):  # Columns
            b = tkinter.Label(self.work_frame, text=attr)
            b.grid(row=0, column=2*j)
            Separator(self.work_frame, orient=tkinter.VERTICAL).grid(row=0, column=2 * j + 1, sticky='ns')
        b = tkinter.Label(self.work_frame, text='Info')
        b.grid(row=0, column=12)
        Separator(self.work_frame, orient=tkinter.HORIZONTAL).grid(row=1, columnspan=15, sticky='ew')

        # Поскольку прокинуть извне в контекст можно только ссылку, то сделать колбэк на месте лямбдой мы не можем
        # Выходом оказался такой вот класс, который инициализруется объектом, но делает на него deepcopy, тем самым
        # отделяя объект от локального контекста.
        _self = self
        class Callback:
            def __init__(self, obj):
                self.obj = copy.deepcopy(obj)

            def __call__(self, *args, **kwargs):
                 _self.fill_created_frame(self.obj)

        for i, event in enumerate(events, start=2):  # Rows
            for j, attr in enumerate(fields):  # Columns
                vl = getattr(event, attr)
                if isinstance(vl, str):
                    # Не более 24 символов в колонке, почему 24? Просто так
                    vl = vl[:24]
                b = tkinter.Label(self.work_frame, text=vl)
                b.grid(row=i, column=2*j)
                Separator(self.work_frame, orient=tkinter.VERTICAL).grid(row=i, column=2*j + 1, sticky='ns')

            tkinter.Button(self.work_frame, text="Info", command=Callback(event)).grid(row=i, column=2 * j + 2, padx=35)

    def fill_created_frame(self, obj):
        self.clear_detail_view()
        labels = {
            'pk': "PK:",
            'type': "Тип:",
            "source": "Источник:",
            "journal": "Журнал:",
            "created": "Дата:",
            "message": "Текст:"
        }
        for j, item in enumerate(obj.__dict__.items()):
            attr, value = item
            ru_attr = labels.get(attr)
            if not ru_attr:
                continue
            tkinter.Label(self.detail_frame, text=ru_attr, bg='white').grid(row=j, column=0)
            tkinter.Label(self.detail_frame, text=value, bg='white').grid(row=j, column=1, columnspan=3, sticky='we')

    def clear_detail_view(self):
        self.detail_frame.destroy()
        self.detail_frame = self._create_detail_info_frame()

    def clear_workspace(self):
        self.work_frame.destroy()
        self.work_frame = self._create_work_frame()

    def clear_infospace(self):
        self.info_frame.destroy()
