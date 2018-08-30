from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .models import Metrics, Crawler
import json
from django.db.models import F
from django.db import transaction
import random

def search(Crawler,user_query,num_results):
    print(Crawler, user_query)
    idx='articlef'
    if Crawler=="PetrMitrichev":
        idx='article_other'
    s=Search(using=Elasticsearch(),index=Crawler.lower(),doc_type="articles")
    q=Q("multi_match",query=user_query,fields=['title^3','content','headings'])
    s=s.query(q)
    print(s.to_dict())
    s=s.highlight('title',fragment_size=30)
    count=s.count()
    unique_list=[]
    ret_list=[]
    total_matches=s.count()
    batch_size=20
    current_pos=0
    c=0
    while len(unique_list)<num_results and current_pos<total_matches:
        c+=1
        s=s[current_pos:current_pos + batch_size]
        response=s.execute()

        for hit in response:
            if hit.title not in unique_list:
                unique_list.append(hit.title)
                print(hit.meta)
                print()
                print()
                highlight="..."+hit.meta.highlight.title[0]+"..."
                ret_list.append({"title":hit.title,"description":highlight,"url":hit.url})
                if len(unique_list)>=num_results:
                    break
        current_pos+=batch_size
        print(current_pos)
        if current_pos>=max(num_results*num_results,200):
            print(len(ret_list))
            ret_list=[]
            break
    print("done in :"+str(c)+" iterations")
    storeMetric(Crawler,user_query)
    if(random.randint(1,10000)<=10):
        compactMetrics(Crawler)
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








        

