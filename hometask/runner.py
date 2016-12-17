import random

from condition import Condition as C
from gui import GUI
from mapper import EventMapper, TYPE_CHOICES, JOURNAL_CHOICES


class App(object):
    gui = GUI()

    def __init__(self):
        self.conditions = {}
        self.event_mapper = EventMapper()
        self.gui.fill_info(self.get_filters())
        events = self.event_mapper.select()
        self.gui.fill_worker(events, self.event_mapper.field_map().keys())
        self.start()

    def get_filters(self):
        # Не оптимально, но для дз пойдет.
        full_event_list = self.event_mapper.select()
        sources = set()
        dates = set()
        for event in full_event_list:
            sources.add(event.source)
            dates.add(event.created)
        return [
            ("Тип", TYPE_CHOICES.values(), self.update_by_type),
            ("Источник", sources, self.update_by_source),
            ("Дата", dates, self.update_by_date),
            ("Журнал", JOURNAL_CHOICES.values(), self.update_by_journal),
        ]

    def start(self):
        self.gui.root.mainloop()

    def get_current_condition(self):
        c = C("1", 1)
        for cond in self.conditions.values():
            c &= cond
        return c

    def update_by(self, filter, value, get_from_dict=None):
        if value != 'ALL':
            # У нас есть всякие поля, которые в базе хранятся в виде инта,
            # а в приложении для кажого инта заведена текстовая интерпретация
            if get_from_dict:
                value = get_from_dict[value]
            self.conditions[filter] = C(filter, value)
        elif self.conditions.get(filter):
            self.conditions.pop(filter)
        events = self.event_mapper.select(self.get_current_condition())
        self.gui.fill_worker(events, self.event_mapper.field_map().keys())

    def update_by_type(self, value):
        # Инвертируем, что бы по текстовому значению получить ключ в базе
        inv = {v: k for k, v in TYPE_CHOICES.items()}
        self.update_by("type", value, inv)

    def update_by_journal(self, value):
        # Инвертируем, что бы по текстовому значению получить ключ в базе
        inv = {v: k for k, v in JOURNAL_CHOICES.items()}
        self.update_by("journal", value, inv)

    def update_by_source(self, value):
        self.update_by("source", value)

    def update_by_date(self, value):
        self.update_by("created", value)


App()
