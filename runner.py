from model.base import BaseMapper
from model.condition import Condition as C


class News:
    def __init__(self, pk, content):
        self.pk = pk
        self.content = content


class NewsMapper(BaseMapper):
    fields = {'pk': 'id', 'content': 'text'}
    table_name = 'model_news'
    model = News

news = News(1, 'abc')
mapper = NewsMapper()
# mapper.insert(news)
condition = C('content', ['dfgffff', 'abc'], action='IN') | C('content', 'W%')
print("Row number ", mapper.delete(condition))
