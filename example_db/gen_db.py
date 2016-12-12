import random
import string

from runner import News, NewsMapper

mapper = NewsMapper()
for i in range(1, 1000):
    news = News(i, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1, 128))))
    mapper.insert(news)
