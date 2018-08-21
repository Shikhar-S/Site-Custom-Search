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
from dashboard import views as dashboard_views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^signup/login/$',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^$',dashboard_views.home,name='home'),
    url(r'^new_crawler/$',dashboard_views.new_crawler,name='new_crawler'),
    url(r'^crawler/(?P<pk>\d+)/$',dashboard_views.serp,name='serp'),
    url(r'crawldomain$',dashboard_views.crawldomain,name='crawldomain'),

]
