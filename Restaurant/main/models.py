from django.db import models

# Create your models here.

choice_field=(
    ('buf','buf'),
    ("veg","veg"),
    ("chicken","chicken")
)
class Momo(models.Model):
    category=models.CharField(choices=choice_field,max_length=200)
    title=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to="images") #pip install pillow