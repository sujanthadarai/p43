from django.contrib import admin
from .models import Momo
# Register your models here.
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','category','price','title','image']
