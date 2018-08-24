from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPage
from .models import Image
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerForm
from .forms import NewImageUploadForm
# Create your views here.
from .crawler import crawl
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
    try:
        dummy_result = Crawler.objects.filter(name=form.cleaned_data.get('domain'))
        print('crawler with this domain already exists')
        return True
    except Crawler.DoesNotExist:
        try:
            dummy_result = Crawler.objects.filter(name=form.cleaned_data.get('name'))
            print('crawler with this name already exists')
            return True
        except Crawler.DoesNotExist:
            return False

def new_crawler(request):
    if request.method == 'POST':
        form = NewCrawlerForm(request.POST,request.FILES)
        if form.is_valid():
            crawlerX = form.save(commit=False)

            if not crawler_already_exists(form):
                print ("Crawler not in the database yet. Creating new crawler")
                resultPage = ResultPage.objects.create(
                adDisplayLeft=form.cleaned_data.get('adDisplayLeft'),
                adDisplayRight=form.cleaned_data.get('adDisplayRight'),
                adDisplayLeftCount=form.cleaned_data.get('adDisplayLeftCount'),
                adDisplayRightCount=form.cleaned_data.get('adDisplayRightCount'),
                companyLogo=form.cleaned_data.get('companyLogo'),
                crawler=crawlerX)
                crawlerX.save()
                #Adding message to Redis Q
                url=form.cleaned_data.get('domain')
                crawler=form.cleaned_data.get('name')
                while(redisQ.publish('messagequeue',crawler+" "+url)==0):
                    continue
            
            return redirect('home')
    else:
        form = NewCrawlerForm()
    
    return render(request, 'new_crawler.html', {'form': form})

def serp(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    #attr=Crawler.objects.get(pk=pk)
    res=crawler.resultpage.first()
    logopath=str(res.companyLogo)[7:]
    print(logopath)


    return render(request,'serp.html',{'name':crawler.name,'domain':crawler.domain,'adleftcount':range(res.adDisplayLeftCount),'adDisplayLeft':res.adDisplayLeft,
                                       'adDisplayRight':res.adDisplayRight,'adRightCount':range(res.adDisplayRightCount),'logo':logopath})


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
        res=search(crawler.name,search_term)
        print(res)
        print(len(res))
        if(len(res)==0):
            return HttpResponse("No results found for the search query")


        return render(request,'search_results.html',{'response':res})


def showImage(request):
        images=Image.objects.get(id=2)
        imagespath=str(images.image)[7:]
        return render(request,'test1.html',{'Image':imagespath})

def insertImage(request):
    if request.method=='POST':
        form=NewImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            formx=form.save(commit=False)
            formx.save()
        return redirect('showImage')
    else:
        form=NewImageUploadForm()

    return render(request,'formtest.html',{'form':form})

def doesitwork(request):
    print("YES!!!")
    return redirect('home')

