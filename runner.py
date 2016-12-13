import random
from collections import OrderedDict

from gui import GUI
from model.base import BaseMapper
from model.condition import Condition as C


class PC:
    def __init__(self, pk, title, adapters=None):
        self.pk = pk
        self.title = title
        self._adapters = adapters if adapters else []

    @property
    def adapters(self):
        return AdapterMapper().select(C("pc", self.pk))


class Adapter:
    def __init__(self, pk, ip, pc=None, _pc=None):
        self.pk = pk
        self.ip = ip
        _pc = pc or _pc
        if isinstance(_pc, PC):
            self._pc = _pc.pk
        else:
            self._pc = _pc

    @property
    def pc(self):
        pcs = PCMapper().select(C("pk", self._pc))
        if pcs:
            return pcs[0]

    @pc.setter
    def pc(self, value):
        self._pc = value.pk


def clean_pc(value):
    if value is not None:
        if isinstance(value, PC):
            return value.pk
        return int(value)


class AdapterMapper(BaseMapper):
    fields = OrderedDict([('pk', 'id'), ('ip', 'ip'), ('pc', 'pc_id')])
    table_name = 'model_adapter'
    model = Adapter
    validators = {'pc': clean_pc}


class PCMapper(BaseMapper):
    fields = OrderedDict([('pk', 'id'), ('title', 'title')])
    table_name = 'model_pc'
    model = PC


class App(object):
    pc_mapper = PCMapper()
    adapter_mapper = AdapterMapper()
    gui = GUI()

    def __init__(self):
        pcs = self.pc_mapper.select(order_by='+pk')
        choices = [x.title for x in pcs]
        self.gui.fill_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add)
        self.start()

    def start(self):
        self.gui.root.mainloop()

    def pc_add(self):
        pcs = self.pc_mapper.select(order_by='pk')
        if pcs:
            new_pk = pcs[-1].pk + 1
        else:
            new_pk = 1
        pc = PC(new_pk, '0.0.0.0', '')
        self.gui.edit_pc(pc, self.pc_edited, self.pc_deleted)

    def pc_deleted(self, pc):
        self.pc_mapper.delete(C("pk", pc.pk))
        pcs = self.pc_mapper.select()
        choices = [x.title for x in pcs]
        self.gui.clear_workspace()
        self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add)

    def pc_selected(self, *args, **kwargs):
        pc_title = self.gui.selected_pc.get()
        pcs = self.pc_mapper.select(C("title", pc_title))
        if pcs:
            pc = pcs[0]
            choices = [ad.ip for ad in pc.adapters]
        else:
            choices = []
            pc = None
        self.gui.add_adapters(choices, self.adapter_edit, self.adapter_status, self.add_adapter, pc=pc)

    def pc_edit(self, pc_title):
        if pc_title == "Select PC":
            return
        pc = self.pc_mapper.select(C('title', pc_title))[0]
        self.gui.edit_pc(pc, self.pc_edited, self.pc_deleted)

    def pc_ping(self, pc_title):
        if pc_title == "Select PC":
            self.gui.result("Не указан ПК!")
        elif random.random() > 0.1:
            self.gui.result("Удачно!")
        else:
            self.gui.result("Нет коннекта!")

    def pc_edited(self, pc, **new_params):
        for k, v in new_params.items():
            setattr(pc, k, v)
        self.pc_mapper.update(pc)
        pcs = self.pc_mapper.select()
        choices = [x.title for x in pcs]
        self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add, choose=pc.title)
        self.gui.clear_workspace()
        adapters = self.adapter_mapper.select(C("pc", pc.pk))
        self.gui.add_adapters(adapters, self.adapter_edit, self.adapter_status, self.add_adapter, pc=pc)

    def adaper_selected(self, adapter):
        pass

    def adapter_edit(self, adapter_ip):
        if adapter_ip == "Select Adapter":
            return
        lst = self.adapter_mapper.select(C('ip', adapter_ip))
        if lst:
            adapter = lst[0]
        else:
            self.gui.clear_workspace()
            pcs = self.pc_mapper.select()
            choices = [x.title for x in pcs]
            self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add)
            return
        self.gui.edit_adapter(adapter, self.adapter_edited, self.adapter_deleted)

    def adapter_edited(self, adapter, **new_params):
        for k, v in new_params.items():
            setattr(adapter, k, v)
        self.adapter_mapper.update(adapter)
        pcs = self.pc_mapper.select()
        choices = [x.title for x in pcs]
        self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add, choose=self.gui.selected_pc.get())
        self.gui.clear_workspace()

    def adapter_status(self, adapter):
        if adapter == "Select PC":
            self.gui.result("Не указан ПК!")
        elif random.random() > 0.1:
            self.gui.result("Удачно!")
        else:
            self.gui.result("Нет коннекта!")

    def add_adapter(self, pc):
        pcs = self.pc_mapper.select()
        choices = [x.title for x in pcs]
        self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add, choose=pc.title)
        self.gui.clear_workspace()

        adapters = self.adapter_mapper.select(order_by='pk')
        if adapters:
            new_pk = pcs[-1].pk + 1
        else:
            new_pk = 1
        new = Adapter(new_pk, '0.0.0.0', pc.pk)
        self.gui.edit_adapter(new, self.adapter_edited, self.adapter_deleted)

    def adapter_deleted(self, adapter):
        self.adapter_mapper.delete(C("pk", adapter.pk))
        self.gui.clear_workspace()
        pcs = self.pc_mapper.select()
        choices = [x.title for x in pcs]
        self.gui.update_info(choices, self.pc_selected, self.pc_edit, self.pc_ping, self.pc_add, choose=adapter.pc.title)


App()
