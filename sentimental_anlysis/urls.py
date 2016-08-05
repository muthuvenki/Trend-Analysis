"""sentimental_anlysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from sentimental_anlysis.views import home,querysearch,youtube,ytubesearch,twitter,twsearch,pinterest,ptsearch,loadOverall,querysearchreturn

urlpatterns = [
    url(r'^$', home),
    url(r'^querysearch/$', querysearch),
    url(r'^youtube/$', youtube),
    url(r'^ytubesearch/$', ytubesearch),
    url(r'^twitter/$', twitter),
    url(r'^twsearch/$', twsearch),
    url(r'^pinterest/$', pinterest),
    url(r'^ptsearch/$', ptsearch),
    url(r'^loadOverall/$', loadOverall), 
    url(r'^querysearchreturn/$', querysearchreturn), 
] 

urlpatterns += staticfiles_urlpatterns()