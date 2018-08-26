from datetime import datetime
from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl import connections
connections.create_connection()

class Article(Document):
    title=Text()
    created_at=Date()
    content=Text()
    keywords=Text()
    crawler_name=Text()
    description=Text()
    url=Text()
    class Index():
        name='article'
    def save(self,** kwargs):
        self.created_at=datetime.now()
        if(self.keywords is None):
            self.keywords=""
        if(self.description is None):
            self.description=""
        if(self.title is None):
            self.title=""
        return super().save(**kwargs)

class SavedCrawler(Document):
    name=Text()
    created_at=Date()
    domain=Text()
    crawled_urls=Text() #list of text fields
    class Index():
        name='saved_crawlers'
    def save(self,** kwargs):
        self.created_at=datetime.now()
        return super().save(**kwargs)


