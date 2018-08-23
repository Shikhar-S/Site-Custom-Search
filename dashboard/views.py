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

def home(request):

    crawlers=Crawler.objects.all()
    return render(request,'home.html',{'crawlers':crawlers})


def new_crawler(request):
    # board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewCrawlerForm(request.POST,request.FILES)
        if form.is_valid():
            crawlerX = form.save(commit=False)
            # topic.board = board
            # topic.starter = user

            crawlerX.save()
            resultPage = ResultPage.objects.create(
                # message=form.cleaned_data.get('message'),

                adDisplayLeft=form.cleaned_data.get('adDisplayLeft'),
                adDisplayRight=form.cleaned_data.get('adDisplayRight'),
                adDisplayLeftCount=form.cleaned_data.get('adDisplayLeftCount'),
                adDisplayRightCount=form.cleaned_data.get('adDisplayRightCount'),
                companyLogo=form.cleaned_data.get('companyLogo'),

                crawler=crawlerX
            )
            return redirect('home')  # TODO: redirect to the created topic page
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
        res=search(crawler.name,search_term,15)
        print(res[1]['content'])
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


def savehtml(request):
    print('yes')
    if request.method=='POST':
        htmlcontent=request.POST.get('html')
        print(htmlcontent)
        file=open("./templates/xyz.html",'w')
        file.write(htmlcontent)
        file.close()
        return HttpResponse('OK')

    return render(request,'draganddrop.html')

@csrf_exempt
def savexxx(request):
    if request.method=='POST':
        htmlcontent=request.POST.get('html')
        print(htmlcontent)
        file=open("./templates/xyz.html",'w')
        file.write(htmlcontent)
        file.close()
        return HttpResponse('OK')


@csrf_exempt
def getelement(request):
    if request.method=='POST':
        element_req=request.POST.get('type')
        return HttpResponse("<div class='ad_smallsquare'>small square ad</div>")
    return render(request,'test4.html')