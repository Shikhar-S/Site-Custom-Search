from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPage,ResultPageX
from .models import Image
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerForm,NewCrawlerFormX
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

def new_crawler(request):
    if request.method == 'POST':
        form = NewCrawlerForm(request.POST,request.FILES)
        if form.is_valid():
            

            if not crawler_already_exists(form):
                crawlerX = form.save(commit=False)
                crawlerX.save()
                print ("Crawler not in the database yet. Creating new crawler")
                resultPage = ResultPage.objects.create(
                adDisplayLeft=form.cleaned_data.get('adDisplayLeft'),
                adDisplayRight=form.cleaned_data.get('adDisplayRight'),
                adDisplayLeftCount=form.cleaned_data.get('adDisplayLeftCount'),
                adDisplayRightCount=form.cleaned_data.get('adDisplayRightCount'),
                companyLogo=form.cleaned_data.get('companyLogo'),
                crawler=crawlerX)
                
                #Adding message to Redis Q
                url=form.cleaned_data.get('domain')
                crawler=form.cleaned_data.get('name')
                    #while(redisQ.publish('messagequeue',crawler+" "+url)==0):
                    #continue
                print('added to redis Queue')
            
            return redirect('home')
    else:
        form = NewCrawlerForm()
    
    return render(request, 'new_crawler.html', {'form': form})


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
                adDisplayLeftCount=form.cleaned_data.get('adDisplayLeftCount'),
                adDisplayRightCount=form.cleaned_data.get('adDisplayRightCount'),
                adDisplayCenterTopCount=form.cleaned_data.get('adDisplayCenterTopCount'),
                adDisplayCenterBottomCount=form.cleaned_data.get('adDisplayCenterBottomCount'),
                companyLogo=form.cleaned_data.get('companyLogo'),
                crawler=crawlerX)
                
                #Adding message to Redis Q
                url=form.cleaned_data.get('domain')
                crawler=form.cleaned_data.get('name')
                #while(redisQ.publish('messagequeue',crawler+" "+url)==0):
                #continue
                print('added to redis Queue')
            
            return redirect('home')
    else:
        form = NewCrawlerFormX()
    return render(request, 'test3.html', {'form': form})

def serp(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)

    res=crawler.resultpagex.first()
    logopath=str(res.companyLogo)[7:]
    leftadcount=res.adDisplayLeftCount
    rightadcount=res.adDisplayRightCount
    centertadcount=res.adDisplayCenterTopCount
    centerbadcount=res.adDisplayCenterBottomCount
    tagline=res.tagline

    print(logopath)


    return render(request,'serppage.html',{'name':crawler.name,'domain':crawler.domain,'logo':logopath,'leftc':range(leftadcount),
                                        'rightc':range(rightadcount),'ctc':range(centertadcount),'cbc':range(centerbadcount),'tagline':tagline
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



@csrf_exempt
def savehtml(request):
    print('yes')
    if request.method=='POST':
        htmlcontent=request.POST.get('html')
        print(htmlcontent)
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        file = open("./templates/" + name + ".html", 'w')
        file.write(htmlcontent)
        file.close()
        return HttpResponse('OK')

    return render(request,'draganddrop.html')


@csrf_exempt
def getelement(request):
    if request.method=='POST':
        element_req=request.POST.get('type')
        return HttpResponse("<div class='ad_smallsquare'>small square ad</div>")
    return render(request,'test4.html')
