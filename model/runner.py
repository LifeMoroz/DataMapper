from model.base import NewsMapper, News
from model.condition import Condition as C

news = News(3, 'dfgffff')
mapper = NewsMapper()
# mapper.insert(news)
condition = C('text', 'abc')
print(mapper.select(condition))
