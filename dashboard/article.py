from datetime import datetime
from elasticsearch_dsl import Document, Text, Keyword, Date
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



Article.init()