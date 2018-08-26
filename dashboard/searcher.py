from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .models import Metrics, Crawler
import json
from django.db.models import F

def search(Crawler,user_query,num_results):
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=(Crawler))
    q=Q("multi_match",query=user_query,fields=['title^2','content'])
    s=s.query(q)
    s=s.highlight('content',fragment_size=50)
    count=s.count()
    unique_list=[]
    ret_list=[]
    total_matches=s.count()
    batch_size=20
    current_pos=0
    while len(unique_list)<num_results and current_pos<=total_matches:
        s=s[current_pos:current_pos + batch_size]
        response=s.execute()
        for hit in response:
            if hit.title not in unique_list:
                unique_list.append(hit.title)
                ret_list.append({"title":hit.title,"description":hit.meta.highlight.content,"url":hit.url})
                if len(unique_list)>=num_results:
                    break
        current_pos+=batch_size
        if current_pos>total_matches:
            current_pos=total_matches

    storeMetric(Crawler,user_query)
#add condition for reducing metric size
    return ret_list


def getCount(Crawler):
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=Crawler)
    return s.count()

def storeMetric(crawler,user_query):
    Metrics.objects.get_or_create(crawlerName=crawler,userQuery=user_query)
    Metrics.objects.filter(userQuery=user_query,crawlerName=crawler).update(queryCount=F('queryCount')+1)

def reduceMetric(crawler):
    pass






        

