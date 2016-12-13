from collections import OrderedDict

from gui import GUI
from model.base import BaseMapper
from model.condition import Condition as C


class PC:
    def __init__(self, pk, ip):
        self.pk = pk
        self.ip = ip


class PCMapper(BaseMapper):
    fields = OrderedDict([('pk', 'id'), ('ip', 'ip')])
    table_name = 'model_pc'
    model = PC


# news = News(1, 'abc')
# mapper = NewsMapper()
# # mapper.insert(news)
# condition = C('content', ['dfgffff', 'abc'], action='IN') | C('content', 'W%')
# print("Row number ", mapper.delete(condition))


def edit_pc(pc, **params):
    pc


class App(object):
    pc_mapper = PCMapper()
    gui = GUI()

    def __init__(self):
        pcs = self.pc_mapper.select()
        choices = [x.ip for x in pcs]
        self.selected_pc = self.gui.fill_info(choices, select_pc_callback=self.pc_selected)
        self.start()

    def start(self):
        self.gui.root.mainloop()

    def pc_selected(self):
        if self.selected_pc.get() == "Select PC":
            return
        pc = self.pc_mapper.select(C('ip', self.selected_pc.get()))[0]
        self.gui.edit_pc(pc, self.pc_edited)

    def pc_edited(self, pc, **new_params):
        for k, v in new_params.items():
            setattr(pc, k, v)
        self.pc_mapper.update(pc)
        pcs = self.pc_mapper.select()
        choices = [x.ip for x in pcs]
        self.gui.update_info(choices, select_pc_callback=self.pc_selected, choose=pc.ip)
        self.gui.clear_workspace()


App()
