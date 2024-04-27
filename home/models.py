from django.db import models
from djrichtextfield.models import RichTextField
from uuid import uuid4

class BaseModel(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     is_active = models.BooleanField(default=True)

     class Meta:
        abstract = True


CHOICE_ABOUT = (
     ('OURGOALS', 'Our Goals'),
     ('OURWORK', 'Our Work'),
     ('OURPASSION', 'Our Passion'),
)

DISTRICT_CHOICES=(
     ('YUNUSOBOD', 'Yunusobod'),
     ('CHILONZOR', 'Chilonzor'),
)


PAYMENT_CHOICES=(
     ('CARD', 'KARTA'),
     ('CASH', 'NAXT')
)



class About(BaseModel):
     title = models.CharField(max_length=100)
     body = RichTextField()
     image = models.ImageField(upload_to='images/')
     menu = models.CharField(max_length=10, choices=CHOICE_ABOUT)


     def __str__(self):
          return self.title

     
class Contact(BaseModel):
     name = models.CharField(max_length=50)
     email = models.EmailField()
     subject = models.CharField(max_length=200)
     message = models.TextField()


     def __str__(self):
          return self.name



class Product(BaseModel):
     title = models.CharField(max_length=100)
     description = models.TextField()
     price = models.FloatField(default=0)
     percentage = models.FloatField(default=0)


     def __str__(self):
          return self.title

     
     @property
     def get_new_price(self):
          if not self.percentage:
               return self.price
          return self.price * (100 - self.percentage)/100

     

class ProductImage(BaseModel):
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
     image = models.ImageField(upload_to='products/')


     def __str__(self):
          return self.product

     
class Order(BaseModel):
     status = models.BooleanField(default=False)
     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
     quantity = models.IntegerField(default=1)
     name = models.CharField(max_length=50, null=True, blank=True)
     email = models.EmailField(null=True, blank=True)
     phone = models.CharField(max_length=15, null=True, blank=True)
     address = models.CharField(max_length=500, null=True, blank=True)
     district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, null=True, blank=True)
     payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True)


     @property
     def get_all_price(self):
          result = self.product.get_new_price() * self.quantity
          return result



     def __str__(self):
          return self.name


class Blog(BaseModel):
     title = models.CharField(max_length=150)
     body = RichTextField()
     description = models.TextField()
     views = models.IntegerField(default=0)
     image = models.ImageField(upload_to='news/')
