from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPageX
from .models import Metrics
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerFormX
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from .searcher import search
import threading
import asyncio
import redis
redisQ=redis.StrictRedis(host='localhost',port=6379,db=0)

def home(request):

    crawlers=Crawler.objects.all()
    return render(request,'home.html',{'crawlers':crawlers})

def crawler_already_exists(form):
        dummy_result = Crawler.objects.filter(name=form.cleaned_data.get('domain'))
        if(dummy_result.count()>0):
            print('crawler with this domain already exists')
            return True
        else:
            dummy_result = Crawler.objects.filter(name=form.cleaned_data.get('name'))
            if dummy_result.count()>0:
                print('crawler with this name already exists')
                print(dummy_result)
                return True
        return False


def new_crawlerx(request):
    if request.method == 'POST':
        form = NewCrawlerFormX(request.POST,request.FILES)
        if form.is_valid():
            
            
            if not crawler_already_exists(form):
                crawlerX = form.save(commit=False)
                crawlerX.save()
                print ("Crawler not in the database yet. Creating new crawler")
                resultPage = ResultPageX.objects.create(
                tagline=form.cleaned_data.get('tagline'),
                websitename=form.cleaned_data.get('websiteName'),
                headerTemplate=form.cleaned_data.get('headerTemplate'),
                companyLogo=form.cleaned_data.get('companyLogo'),
                bodyTemplate=form.cleaned_data.get('bodyTemplate'),
                
                crawler=crawlerX
                
                
                )
                
                #Adding message to Redis Q
                url=form.cleaned_data.get('domain')
                crawler=form.cleaned_data.get('name')
                #while(redisQ.publish('messagequeue',crawler+" "+url)==0):
                #continue
                print('added to redis Queue')
            
            return redirect('home')
    else:
        form = NewCrawlerFormX()
    return render(request, 'newcrawlform.html', {'form': form})

def serp(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    
    res=crawler.resultpagex.first()
    logopath=str(res.companyLogo)[7:]
    tagline=res.tagline
    websitename=res.websitename
    headerTemplate=res.headerTemplate+".html"
    bodyTemplate='body_'+crawler.name+'.html'
    
    print(logopath)
    
    
    return render(request,'searchlandingpage.html',{'name':crawler.name,'domain':crawler.domain,'logo':logopath,'tagline':tagline,'websitename':websitename,
                  'headerTemplate':headerTemplate,'bodyTemplate':bodyTemplate
                  })


@csrf_exempt
def crawldomain(request):
    if request.method=='POST' :
        domain=request.POST.get("domain")
        crawler=request.POST.get("crawler")
        crawl(crawler,domain)
        return HttpResponse("OK")

@csrf_exempt
def getresult(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    if request.method=='POST':
        search_term=request.POST.get('search_term')
        res=search(crawler.name,search_term,15)
        # print(res[1]['content'])
        # print(len(res))
        if(len(res)==0):
            return HttpResponse("No results found for the search query")
        
        
        return render(request,'search_results.html',{'response':res})

@csrf_exempt
def getheader(request):
    if request.method=='POST':
        template=request.POST.get('header')
        if template=='header1':
            return render(request,'header1.html')
        if template=='header2':
            return render(request,'header2.html')
    return render(request,'header3.html')


def show_metrics(request,crawler_name):
    if(request.method=='GET'):
        try:
            result=Metrics.objects.filter(crawlerName=crawler_name)
            print(result)
            result=result.order_by('-queryCount')[:10]
            print(result)
            res=[]
            for entry in result:
                res.append({'Query':entry.userQuery,'Count':entry.queryCount})
            return render(request,'metrics.html',{'response':res})
        except:
            return HttpResponse("No metrics to show yet")

@csrf_exempt
def savehtml(request):
    print('yes')
    if request.method=='POST':
        htmlcontent=request.POST.get('html')
        print(htmlcontent)
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        
        file = open("./templates/body_" + name + ".html", 'w')
        file.write(htmlcontent)
        file.close()
        return HttpResponse('OK')


@csrf_exempt
def getelement(request):
    if request.method=='POST':
        element_req=request.POST.get('type')
        return HttpResponse("<div class='ad_smallsquare'>small square ad</div>")
    return render(request,'test4.html')
