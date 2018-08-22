from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .schema import Article
import json

def search(Crawler,user_query,num_results):
    s=Search(using=Elasticsearch())
    q=Q("multi_match",query=user_query,fields=['title^3','keywords^2','description','content'])
    s=s.query(q)
    s=s.filter('term',crawler_name=Crawler)
    count=s.count()
    if num_results>count:
        num_results=count
    s=s[0:num_results]
    response=s.execute()


    return [{"title":hit.title,"description":hit.description,"url":hit.url} for hit in s]


