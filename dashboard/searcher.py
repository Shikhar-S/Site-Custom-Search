from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .article import Article
import json

def search(Crawler,user_query):
    s=Search(using=Elasticsearch())
    q=Q("multi_match",query=user_query,fields=['title^3','keywords^2','description','content'])
    s=s.query(q)
    s=s.filter('term',crawler_name=Crawler)
    response=s.execute()
    print(type(s))
    for h in response:
        print(h.title, h.description,h.url)
    return [{"title":hit.title,"description":hit.description,"url":hit.url} for hit in s]
