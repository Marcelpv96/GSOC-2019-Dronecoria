"""dronecoria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic import TemplateView
from gsoc2019.views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),
    url(r'^load/upload/$', load_path, name="load_path"),
    url(r'^load/delete/(?P<kmlname>[\w|\W]+)/$', delete_path_kml, name="delete_path_kml"),
    url(r'^load/clean/$', view_clean_kml, name="clean_kml"),
    url(r'^load/(?P<kmlname>[\w|\W]+)/$', send_path_kml, name="send_path_kml"),
    url(r'^load/$',  documentList.as_view(), name="document_list"),
    url(r'^burnt/clean/$', view_clean_kml, name="clean_kml_gallery"),
    url(r'^burnt/stop/$', view_stop_tour, name="stop_tour_gallery"),
    url(r'^burnt/flytoforest/(?P<galleryname>[\w|\W]+)/$', fly_to_forest, name="fly_to_forest"),
    url(r'^burnt/gallery/(?P<galleryname>[\w|\W]+)/$', show_gallery, name="show_gallery"),
    url(r'^burnt/detect/(?P<galleryname>[\w|\W]+)/clean/$', clean_detect_zone, name='clean_images'),
    url(r'^burnt/detect/(?P<galleryname>[\w|\W]+)/$', detect_zone, name='send_images'),
    url(r'^burnt/delete/(?P<galleryname>[\w|\W]+)/$', delete_gallery, name="delete_gallery"),
    url(r'^burnt/reforest/(?P<galleryname>[\w|\W]+)/clean/$', clean_reforest, name="clean_reforest"),
    url(r'^burnt/reforest/(?P<galleryname>[\w|\W]+)/$', reforest, name="reforest"),
    url(r'^burnt/(?P<galleryname>[\w|\W]+)/clean/$', clean_send_gallery_images, name="clean_gallery"),
    url(r'^burnt/(?P<galleryname>[\w|\W]+)/$', send_gallery_images, name="send_gallery"),
    url(r'^burnt/$', galleryList.as_view(), name="burnt"),
    url(r'^burnt/gallery', new_gallery, name="new_gallery"),
    url(r'^burnt/images', upload_images_gallery, name="upload_images_gallery"),
    url(r'^demo/clean/$', view_clean_kml, name="clean_kml_demo"),
    url(r'^demo/stoptour/$', view_stop_tour, name="stop_tour_demo"),
    url(r'^demo/start/$', start_demo, name="start_demo"),
    url(r'^demo/stop/$', stop_demo, name="stop_demo"),
    url(r'^demo/$', demo, name="demo"),
    path('admin/', admin.site.urls)
]
