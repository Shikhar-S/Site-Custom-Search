from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .article import Article

def search(Crawler,user_query):
    s=Search(using=Elasticsearch())
    q=Q("multi_match",query=user_query,fields=['title^3','keywords^2','description','content'])
    s=s.query(q)
    s=s.filter('term',crawler_name=Crawler)
    response=s.execute()
    for hit in s:
        print(hit.title)
    return [(hit.title,hit.description,hit.url) for hit in s]

search('test_crawler','algorithms')
