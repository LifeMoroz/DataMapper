from collections import OrderedDict
from datetime import datetime

from db.db import Database


SYSTEM_JOURNAL = (0, 'Системный журнал')
USER_JOURNAL = (1, 'Пользовательский журнал')
JOURNAL_CHOICES = dict([SYSTEM_JOURNAL, USER_JOURNAL])

ERROR = (0, 'Ошибка')
WARNING = (1, 'Предупреждение')
INFO = (2, 'Сведения')
SUCCESS = (3, 'Аудит успеха')
FAIL = (4, 'Аудит отказа')
TYPE_CHOICES = dict([ERROR, WARNING, INFO, SUCCESS, FAIL])


class Event:
    def __init__(self, pk, type, source, journal, date, message):
        if isinstance(date, int):
            date = datetime.fromtimestamp(date/1000)
        self.pk = pk
        self.type = type
        self.source = source
        self.journal = journal
        self.created = date
        self.message = message


class EventMapper:
    model = Event

    @staticmethod
    def field_map():
        d = OrderedDict()
        d['pk'] = 'id'
        d['type'] = 'type'
        d['message'] = 'text'
        d['source'] = 'source'
        d['journal'] = 'journal'
        d['created'] = 'date'
        return d

    def _map_fields(self, obj):
        # Кроме маппинга еще приводит типы
        inv_type = {v: k for k, v in TYPE_CHOICES.items()}
        inv_journal = {v: k for k, v in JOURNAL_CHOICES.items()}
        return {
            "id": obj.pk,
            "type": inv_type[obj.type],
            "source": obj.source,
            "journal": inv_journal[obj.journal],
            "date": obj.created,
            "text": obj.message
        }

    def insert(self, obj):
        sql = "INSERT INTO events (id, type, source, journal, date) VALUES (:id, :type, :source, :journal, :date)"
        _map = self._map_fields(obj)
        return Database.execute(sql, _map).rowcount

    def update(self, obj):
        sql = "REPLACE INTO events (id, type, source, journal, date) VALUES (:id, :type, :source, :journal, :date)"
        _map = self._map_fields(obj)
        return Database.execute(sql, _map).rowcount

    def select(self, condition=None):
        sql = "SELECT id, type, source, journal, date, text FROM events"
        where_params, where_sql = [], None
        if condition is not None:
            where_sql, where_params = condition.sql(self.field_map())
            sql += " WHERE {where}".format(where=where_sql)
        result = []
        for row in Database.execute(sql, where_params).fetchall():
            row = list(row)
            row[1] = TYPE_CHOICES[row[1]]
            row[3] = JOURNAL_CHOICES[row[3]]
            result.append(self.model(*row))
        return result
