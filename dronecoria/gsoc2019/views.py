from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage
from gsoc2019.models import *
from gsoc2019.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from braces.views import (
    AjaxResponseMixin,
    JSONResponseMixin,
    LoginRequiredMixin,
    SuperuserRequiredMixin,
)
import os
from gsoc2019.aux_functions import *
from gsoc2019.demo import *


def load_path(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('load_path')
    else:
        form = DocumentForm()
    return render(request, 'first_drone_path/load_path.html', {
        'form': form
    })


def pagination(request, item_list, elems_per_page):
    paginator = Paginator(item_list, elems_per_page)

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects


class documentList(ListView):
    model = Document
    template_name = "first_drone_path/all_path.html"

    def get_context_data(self, **kwargs):
        context = super(documentList, self).get_context_data(**kwargs)
        context['Documents'] = Document.objects.all()
        context['Documents'] = pagination(self.request, context['Documents'], 10)

        return context


class galleryList(ListView):
    model = Gallery
    template_name = "burnt_region/burnt.html"
    def get_context_data(self, **kwargs):
        context = super(galleryList, self).get_context_data(**kwargs)
        context['Galleries'] = Gallery.objects.all().order_by('name')
        context['Galleries'] = pagination(self.request, context['Galleries'], 10)
        return context


def new_gallery(request):
    if request.method == 'POST':
        form = NewGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('new_gallery')
    else:
        form = NewGalleryForm()
    return render(request, 'burnt_region/new_gallery.html', {
            'form': form
        })


def upload_images_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_images_gallery')
    else:
        form = GalleryForm()
    return render(request, 'burnt_region/upload_images_gallery.html', {
        'form': form
    })


def detect_zone(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    images = [image_gallery for image_gallery in Image.objects.all().filter(gallery_images=gallery)]
    detect_region(images)
    send_gallery_bubble(images)
    return HttpResponse(status=204)


def send_path_kml(request, kmlname):
    kml_file_path = Document.objects.get(name=kmlname).document.name
    send_kml(kml_file_path)
    return HttpResponse(status=204)


def send_gallery_images(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    images = [image_gallery for image_gallery in Image.objects.all().filter(gallery_images=gallery)]
    if len(images) == 0:
        return HttpResponse(status=204)
    else:
        send_gallery(images)
        return HttpResponse(status=204)


def view_clean_kml(request):
    clean_kml()
    return HttpResponse(status=204)


def view_stop_tour(request):
    stop_orbit()
    return HttpResponse(status=204)


def delete_gallery(request, galleryname):
    Gallery.objects.filter(name=galleryname).delete()
    for image_gallery in Image.objects.all().filter(gallery_images=galleryname):
        image_gallery.delete()
    return redirect('burnt')


def show_gallery(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    images = ["/" + image_gallery.img.name.replace("upload_images", "static") for image_gallery in Image.objects.all().filter(gallery_images=gallery)]
    print(images[0])
    if len(images) == 0:
        return HttpResponse(status=204)
    else:
        return render(request, "burnt_region/list_images.html", {'images': images})


def fly_to_forest(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    corners = {'fCorner':[0, 0, 0], 'sCorner':[0, 0, 0], 'tCorner':[0, 0, 0], 'ftCorner':[0, 0, 0]}

    for image_gallery in Image.objects.all().filter(gallery_images=galleryname):
        for corner in corners:
            coordinates = list(map(float,image_gallery.__dict__[corner].split(',')))
            for coor in range(0,3):
                corners[corner][coor] += coordinates[coor]
    num_images = len(Image.objects.all().filter(gallery_images=galleryname))
    for corner in corners:
        for coor in range(0,3):
            corners[corner][coor] /=  num_images
    fly_to_center_forest(corners)
    return HttpResponse(status=204)


def delete_path_kml(request, kmlname):
    Document.objects.filter(name=kmlname).delete()
    return redirect('document_list')


def reforest(request, galleryname):
    images = Image.objects.all().filter(gallery_images=galleryname)
    reforestation(images)

    return HttpResponse(status=204)


def clean_reforest(request, galleryname):
    images = Image.objects.all().filter(gallery_images=galleryname)
    stop_reforestation(images)
    return HttpResponse(status=204)

def clean_detect_zone(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    images = [image_gallery for image_gallery in Image.objects.all().filter(gallery_images=gallery)]
    detele_gallery_buuble(images)
    return HttpResponse(status=204)

def clean_send_gallery_images(request, galleryname):
    gallery =  Gallery.objects.get(name=galleryname).name
    images = [image_gallery for image_gallery in Image.objects.all().filter(gallery_images=gallery)]
    delete_image(images)
    return HttpResponse(status=204)

def demo(request):
    return render(request, 'demo.html')

def start_demo(request):
    main_demo()
    return HttpResponse(status=204)

def stop_demo(request):
    stop()
    return HttpResponse(status=204)
