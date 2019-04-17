from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^faiss/', include('faiss.urls')),
    #url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),	
]

