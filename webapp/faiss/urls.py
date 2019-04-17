
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'faiss'
urlpatterns = [
	url(r'^simple_upload/$', views.simple_upload, name='simple_upload'),
	url(r'^mongodRequest/$', views.mongodRequest, name='mongodRequest'),
	url(r'^search$', views.search, name='search'),
	url(r'^add/$', views.add, name='add'),
	url(r'^$', views.index, name='index'),
#    url(r'^hello$', views.IndexView.as_view(), name='index'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
