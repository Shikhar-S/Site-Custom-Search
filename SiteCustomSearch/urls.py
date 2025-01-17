"""SiteCustomSearch URL Configuration
    
    The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
    Examples:
    Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from dashboardfinal import views as dviews
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#    url(r'^signup/$', accounts_views.signup, name='signup'),
#    url(r'^signup/login/$',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
#    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
#    url(r'^$',dashboard_views.home,name='home'),
#    url(r'^new_crawler/$',dashboard_views.new_crawlerx,name='new_crawler'),
#    url(r'^crawler/(?P<pk>\d+)/$',dashboard_views.serp,name='serp'),
#    url(r'crawldomain$',dashboard_views.crawldomain,name='crawldomain'),
#    url(r'crawler/(?P<pk>\d+)/getresult$',dashboard_views.getresult,name='getresult'),
#    url(r'formimage/$',dashboard_views.insertImage,name='insertImage'),
#    url(r'image/$',dashboard_views.showImage,name='showImage'),
#    url(r'new_crawler/savehtml$',dashboard_views.savehtml,name='savehtml'),
#    url(r'getelement$',dashboard_views.getelement,name='getelement'),
#
#]

urlpatterns=[
             path('admin/', admin.site.urls),
             url(r'^$',dviews.home,name='home'),
             url(r'^new_crawler/$',dviews.new_crawlerx,name='new_crawler'),
             url(r'new_crawler/savehtml$',dviews.savehtml,name='savehtml'),
             url(r'^crawler/(?P<pk>\d+)/$',dviews.serp,name='serp'),
             url(r'crawler/(?P<pk>\d+)/getresult$',dviews.getresult,name='getresult'),
             url(r'crawler/(?P<pk>\d+)/metric/$',dviews.show_metrics,name='metrics_page'),
             url(r'new_crawler/getheader$',dviews.getheader,name='getheader'),
             url(r'search/$',dviews.searchs,name='search'),
             url(r'getresultpop$',dviews.getresultpop,name='getresultpop'),
             url(r'crawlerdescription/(?P<pk>\d+)$',dviews.crawldesc,name='crawlerdescription'),
             url(r'crawler/(?P<pk>\d+)/autocomplete_page$',dviews.autocomplete,name='autocomplete_page'),
             url(r'testsite/$',dviews.testsite,name="testsite")
             ]
