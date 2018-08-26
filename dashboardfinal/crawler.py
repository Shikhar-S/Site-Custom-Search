import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as Soup
from datetime import datetime

from .schema import Article, SavedCrawler

from urllib.parse import urlparse
MAX_DEPTH=5
MAX_BREADTH=30

def add_to_elastic_search(soup,c_url,Crawler):
    obj=Article(title=soup.title.string,content=soup.get_text(),crawler_name=Crawler,url=c_url)
    jsn=requests.get('http://xtractor.reports.mn/api?app=APP&html=1&a=unique&url='+c_url).json()
    for di in jsn['meta_tags']:
        if('name' in di.keys() and di['name']=='keywords'):
            obj.keywords=di['content']
            break

    for di in jsn['meta_tags']:
        if('name' in di.keys() and di['name']=='Description'):
            obj.description=di['content']
            break

    obj.save()


def crawl(Crawler,base_url):
    crawled_set=set()
    if(base_url==""):
        return
    queue=[]
    queue.append((base_url,0))
    
    while(queue):
        url,depth=queue.pop(0)
        if(url in crawled_set or urlparse(url).netloc != urlparse(base_url).netloc):
            continue
        crawled_set.add(url)
        print("Crawling "+url + " at depth: "+str(depth))
        if(depth>MAX_DEPTH):
            continue

        try:
            response=requests.get(url)
            if(response.status_code!=200):
                print("Error for url :" +url)
                continue

            soup=Soup(response.text,'lxml')
            add_to_elastic_search(soup,url,Crawler)
            counter=0 # counter for branches

            for link in soup.find_all('a'):
                lnk=link.get('href')
                if(lnk is None):
                    continue

                if(not bool(urlparse(lnk).netloc)):
                    lnk=base_url+lnk
                
                if(lnk.startswith(base_url+"#")):
                    continue
                
                if(lnk is not None and lnk[:4]=='http'):
                    queue.append((lnk,depth+1))
                    counter+=1

                    if(counter>MAX_BREADTH):
                        counter=0
                        break

        except  RequestException:
            print("Can't index: "+url)
    Crawler_obj=SavedCrawler(name=Crawler,domain=base_url,crawled_urls=[x for x in crawled_set])
    Crawler_obj.save()

# crawl('test_crawler','https://www.webmd.com')
