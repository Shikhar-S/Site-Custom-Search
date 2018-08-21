from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPage
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerForm
# Create your views here.
from .crawler import crawl
from django.views.decorators.csrf import csrf_exempt
import threading
import asyncio

def home(request):

    crawlers=Crawler.objects.all()
    return render(request,'home.html',{'crawlers':crawlers})


def new_crawler(request):
    # board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewCrawlerForm(request.POST)
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



    return render(request,'serp.html',{'name':crawler.name,'domain':crawler.domain,'adleftcount':range(res.adDisplayLeftCount),'adDisplayLeft':res.adDisplayLeft,
                                       'adDisplayRight':res.adDisplayRight,'adRightCount':range(res.adDisplayRightCount)})


@csrf_exempt
def crawldomain(request):
    if request.method=='POST' :
        domain=request.POST.get("domain")
        crawler=request.POST.get("crawler")
        crawl(crawler,domain)
        return HttpResponse("OK")


def getresult(request):
    if request.method=='POST':
        domain=request.POST.get('')
