from model.db import DataWrapper


class ValidateError(Exception):
    pass


class BaseMapper:
    data_wrapper = DataWrapper()
    validators = {}
    fields = {}
    table_name = None
    model = None

    def __validate(self, obj):
        clean_data = {}
        for field, db_field in self.fields.items():
            value = getattr(obj, field)
            if not (self.validators.get(field) is None or self.validators[field](value)):
                raise ValidateError
            clean_data[self.fields[field]] = value
        return clean_data

    def get_table_name(self):
        return self.table_name or __package__ + self.model.__class__.__name__.lower()

    def _insert(self):
        fields = ', '.join(self.fields.values())
        values = ':' + ', :'.join(self.fields.values())
        sql = "INSERT INTO {table_name} ({fields}) VALUES ({values})".format(
            table_name=self.get_table_name(), fields=fields, values=values)
        return sql

    def _select(self, condition):
        where_sql, where_params = condition.sql(self.fields)
        fields = ', '.join(self.fields.values())
        sql = "SELECT {fields} FROM {table_name} WHERE {where}".format(
            fields=fields, table_name=self.get_table_name(), where=where_sql)
        return sql, where_params

    def insert(self, obj):
        data = self.__validate(obj)
        sql = self._insert()
        self.data_wrapper.execute(sql, data)

    def select(self, condition):
        sql, params = self._select(condition)
        result = []
        for row in self.data_wrapper.execute(sql, params).fetchall():
            result.append(News(*row))
        return result

    def update(self, obj):
        self.__validate(obj)

    def delete(self, **params):
        pass


class News:
    def __init__(self, pk, content):
        self.pk = pk
        self.content = content


class NewsMapper(BaseMapper):
    fields = {'pk': 'id', 'content': 'text'}
    table_name = 'model_news'
    model = News
