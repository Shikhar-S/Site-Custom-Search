
from django.http import HttpResponse
from django.shortcuts import render
from .models import Crawler
from .models import ResultPageX
from .models import Metrics
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewCrawlerFormX
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
# Create your views here.
from django.http import JsonResponse

import random

from django.views.decorators.csrf import csrf_exempt
from .searcher import search, storeMetric, compactMetrics
import threading
import asyncio
subkey='dcf13da58d784c3ab9bc479dcdd55e8a'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
search_term = "Azure Cognitive Services"

jstop="""$( function() {
    $( "#dialog" ).dialog({
    autoOpen: false,
    show: {
    effect: "blind",
    duration: 1000
    },
    hide: {
    effect: "explode",
    duration: 1000
    },
    width: "90%",
    maxWidth: "768px",
   
    });
    })
    
    
    
    window.onload = function() {
    // setup the button click
    
    document.getElementById("search_query").onsubmit=function(){getsearchresults();};
    }
    
    
    function getsearchresults() {
    event.preventDefault();
    
    var query=document.getElementById("search_term").value;
    console.log(query);
    
    
    """
jsbottom="""
    event.preventDefault();
    $.post("getresultpop", data, function(resp){
    console.log("hello");
    var content=$(resp);
    $("#searchresults").empty().append(resp);
    $( "#dialog" ).dialog( "open" );
    
    
    
    
    });
    
    event.preventDefault();
    }
    
    """





import requests
import redis
redisQ=redis.StrictRedis(host='localhost',port=6379,db=0)

def home(request):
    
    crawlers=Crawler.objects.all()
    # return render(request, 'xyz.html')
    return render(request,'hometemplate.html',{'crawlers':crawlers})

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
                numberOfResults=form.cleaned_data.get('numberOfResults'),
                
                crawler=crawlerX
                
                
                )

                #Adding message to Redis Q
                url=form.cleaned_data.get('domain')
                crawler=form.cleaned_data.get('name')
#                while(redisQ.publish('messagequeue3',crawler+" "+url)==0):
#                    continue
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
    
#    print(logopath)

    
    return render(request,'searchlandingpage.html',{'name':crawler.name,'domain':crawler.domain,'logo':logopath,'tagline':tagline,'websitename':websitename,
                  'headerTemplate':headerTemplate,'bodyTemplate':bodyTemplate
                  })




@csrf_exempt
def getresult(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    if request.method=='POST':
        search_term=request.POST.get('search_term')
        search_term=search_term.lower()
        search_loc=request.POST.get('searchloc')
        numres=crawler.resultpagex.first().numberOfResults
        
        if search_loc=='p':
            res=search(crawler.name,search_term,numres)
            # print(res[1]['content'])
            # print(len(res))
            if(len(res)==0):
                return HttpResponse("No results found for the search query")
            
            
            return render(request,'search_results.html',{'response':res})
        # q="site:"+crawler.domain+" "+search_term
        q=search_term
        headers = {"Ocp-Apim-Subscription-Key": subkey}
        params = {"q": q, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
#        print(search_results)
        # print(search_results['webPages']['value'][0:numres])
        storeMetric(Crawler,search_term)
        if(random.randint(1,10000)<=10):
            compactMetrics(Crawler)
        return render(request, 'search_results_bing.html', {'response': search_results['webPages']['value'][0:numres]})


@csrf_exempt
def getresultpop(request):
    
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        search_term = search_term.lower()
        crawlername = request.POST.get('crawlername')
        numres = 10
        res = search(crawlername.strip(), search_term, numres)
        if (len(res) == 0):
            return HttpResponse("No results found for the search query")
        return render(request, 'search_results.html', {'response': res})
#        headers = {"Ocp-Apim-Subscription-Key": subkey}
#        params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
#        response = requests.get(search_url, headers=headers, params=params)
#        response.raise_for_status()
#        search_results = response.json()
#
#        # print(search_results['webPages']['value'][0:numres])
#        return render(request, 'search_results_bing1.html', {'response': search_results['webPages']['value'][0:numres]})

@csrf_exempt
def getheader(request):
    if request.method=='POST':
        template=request.POST.get('header')
        if template=='header1':
            return render(request,'header1.html')
        if template=='header2':
            return render(request,'header2.html')
    return render(request,'header3.html')


def show_metrics(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    if(request.method=='GET'):
        try:
            result=Metrics.objects.filter(crawlerName=crawler.name)
#            print(result)
            result=result.order_by('-queryCount')[:10]
#            print(result)
            res=[]
            for entry in result:
                res.append({'Query':entry.userQuery,'Count':entry.queryCount})
            return render(request,'metrics.html',{'response':res})
        except:
            return HttpResponse("No metrics to show yet")

@csrf_exempt
def savehtml(request):
#    print('yes')
    if request.method=='POST':
        htmlcontent=request.POST.get('html')
#        print(htmlcontent)
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        
        file = open("./templates/body_" + name + ".html", 'w')
        file.write(htmlcontent)
        file.close()
        
        # print(name)
        file=open("./static/js/"+name+".js",'w');
        data= """ var data = { "search_term":query, csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),'crawlername':' """+name+""" '}; """
        
        finaldata=jstop+data+jsbottom
        file.write(finaldata)
        file.close()
        
        
        
        
        return HttpResponse('OK')

@csrf_exempt
def getelement(request):
    if request.method=='POST':
        element_req=request.POST.get('type')
        return HttpResponse("<div class='ad_smallsquare'>small square ad</div>")
    return render(request,'test4.html')



@csrf_exempt
def searchs(request):
    if request.method=='POST':
        id=request.POST.get('crawler_id')
        crawler=get_object_or_404(Crawler,pk=id)
        search_term=request.POST.get('search_term')
        numres=int(request.POST.get('numres'))
        res=search(crawler.name,search_term,numres)
        # print(res)
        #res=[{"hello":"bc","jhskjdf":"gan"},{"hello":"bc","jhskjdf":"gan"}]
        # print(res)
        return JsonResponse(res,safe=False);



def crawldesc(request,pk):
    crawler=get_object_or_404(Crawler,pk=pk)
    return render(request,"crawlerdescription.html",{'crawler':crawler})


@csrf_exempt
def autocomplete(request,pk):
    query=request.POST.get("search")
    crawler=get_object_or_404(Crawler,pk=pk)
    s=Search(using=Elasticsearch(),index=crawler.name.lower()+"_",doc_type="articles")
    s=s.suggest("title_suggester",query, completion={'field': 'completion_suggester'})
    suggestions=s.execute()
    ret_list=list(set([opt.text+"..." for opt in suggestions.suggest.title_suggester[0].options]))
    return JsonResponse({'data':ret_list})

def testsite(request):
    return render(request,"testingsite.html")


