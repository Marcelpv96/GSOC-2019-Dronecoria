from django import forms
from gsoc2019.models import *

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', )


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('gallery_images' , 'img', 'fCorner', 'sCorner', 'tCorner', 'ftCorner',)


class NewGalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('name', )
