from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPageX

from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerForm,NewCrawlerFormX

# Create your views here.
from .crawler import crawl
from django.views.decorators.csrf import csrf_exempt
from .searcher import search
import threading

# Create your views here.
def home(request):

    crawlers=Crawler.objects.all()
    return render(request,'home.html',{'crawlers':crawlers})


def new_crawlerx(request):


    if request.method == 'POST':
        form = NewCrawlerFormX(request.POST,request.FILES)
        if form.is_valid():
            print("yessfdasdf")
            crawlerX = form.save(commit=False)

            crawlerX.save()
            resultPage = ResultPageX.objects.create(
                tagline=form.cleaned_data.get('tagline'),
                websitename=form.cleaned_data.get('websiteName'),
                headerTemplate=form.cleaned_data.get('headerTemplate'),
                companyLogo=form.cleaned_data.get('companyLogo'),
                bodyTemplate=form.cleaned_data.get('bodyTemplate'),

                crawler=crawlerX


            )
            return redirect('home')  # TODO: redirect to the created topic page
    else:
        form = NewCrawlerFormX()
    return render(request, 'newcrawlform.html', {'form': form})


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