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

    def _replace(self):
        fields = ', '.join(self.fields.values())
        values = ':' + ', :'.join(self.fields.values())
        sql = "REPLACE INTO {table_name} ({fields}) VALUES ({values})".format(
            table_name=self.get_table_name(), fields=fields, values=values)
        return sql

    def _select(self, condition=None):
        fields = ', '.join(self.fields.values())
        sql = "SELECT {fields} FROM {table_name}"
        where_params, where_sql = [], None
        if condition is not None:
            where_sql, where_params = condition.sql(self.fields)
            sql += " WHERE {where}"
        sql = sql.format(fields=fields, table_name=self.get_table_name(), where=where_sql)
        return sql, where_params

    def _delete(self, condition=None):
        where_params, where_sql = [], None
        sql = "DELETE FROM {table_name}"
        if condition:
            where_sql, where_params = condition.sql(self.fields)
            sql += " WHERE {where}"
        sql = sql.format(table_name=self.get_table_name(), where=where_sql)
        return sql, where_params

    def insert(self, obj):
        data = self.__validate(obj)
        sql = self._insert()
        return self.data_wrapper.execute(sql, data).rowcount

    def select(self, condition=None):
        sql, params = self._select(condition)
        result = []
        for row in self.data_wrapper.execute(sql, params).fetchall():
            result.append(self.model(*row))
        return result

    def update(self, obj):
        data = self.__validate(obj)
        sql = self._replace()
        print(sql, data)
        return self.data_wrapper.execute(sql, data).rowcount

    def delete(self, condition):
        sql, params = self._delete(condition)
        return self.data_wrapper.execute(sql, params).rowcount
