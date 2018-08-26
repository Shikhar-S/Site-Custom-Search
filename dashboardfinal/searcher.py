from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .models import Metrics, Crawler
import json
from django.db.models import F
from django.db import transaction
import random

def search(Crawler,user_query,num_results):
    
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=(Crawler))
    q=Q("multi_match",query=user_query,fields=['title^3','content'])
    s=s.query(q)
    s=s.highlight('content',fragment_size=50)
    count=s.count()
    unique_list=[]
    ret_list=[]
    total_matches=s.count()
    batch_size=20
    current_pos=0
    while len(unique_list)<num_results and current_pos<total_matches:
        s=s[current_pos:current_pos + batch_size]
        response=s.execute()
        for hit in response:
            if hit.title not in unique_list:
                unique_list.append(hit.title)
                ret_list.append({"title":hit.title,"description":hit.meta.highlight.content,"url":hit.url})
                if len(unique_list)>=num_results:
                    break
        current_pos+=batch_size
        
        if current_pos>=num_results*num_results:
            ret_list=[]
            break

#    storeMetric(Crawler,user_query)
#    if(random.randint(1,10000)<=10):
#       compactMetrics(Crawler)
    return ret_list


def getCount(Crawler):
    s=Search(using=Elasticsearch(),index=('articles'),doc_type=Crawler)
    return s.count()

def storeMetric(crawler,user_query):
    try:
        Metrics.objects.get_or_create(crawlerName=crawler,userQuery=user_query)
        Metrics.objects.filter(userQuery=user_query,crawlerName=crawler).update(queryCount=F('queryCount')+1)
    except :
        print('row deleted  by Metrics compactor')

@transaction.atomic
def compactMetrics(crawler):
    records=Metrics.objects.filter(crawlerName=crawler).order_by('-queryCount')[:100].values_list("id", flat=True)
    Metrics.objects.exclude(pk__in=list(records)).delete()








        

