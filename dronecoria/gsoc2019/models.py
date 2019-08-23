from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=255, blank=True, primary_key=True)
    document = models.FileField(upload_to='kml_drone_path/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=255, blank=True, primary_key=True)
    def __unicode__(self):
        return self.name


class Image(models.Model):
    gallery_images = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    fCorner = models.CharField(max_length=400, blank=False)
    sCorner = models.CharField(max_length=400, blank=False)
    tCorner = models.CharField(max_length=400, blank=False)
    ftCorner = models.CharField(max_length=400, blank=False)
    burntArea =  models.FloatField(null=True, blank=True, default=0)
    img = models.ImageField(upload_to='upload_images/')
