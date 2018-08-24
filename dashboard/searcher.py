from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json

def search(Crawler,user_query,num_results):
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=(Crawler))
    q=Q("multi_match",query=user_query,fields=['title^2','content'])
    s=s.query(q)
    s=s.highlight('content',fragment_size=50)
    count=s.count()
    if num_results>count:
        num_results=count
    s=s[0:num_results]
    response=s.execute()
    return [{"title":hit.title,"description":hit.meta.highlight.content,"url":hit.url} for hit in s]


def getCount(Crawler):
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=Crawler)
    return s.count()
    


