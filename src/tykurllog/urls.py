from django.conf.urls import include, url
from django.contrib import admin
from tykurllog import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^$', views.UrlSearchView.as_view(), name='search'),
]
