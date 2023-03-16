from django.db import models

# Create your models here.
from datetime import date
from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _


class Salesman(models.Model):
    full_name = models.CharField(_('full_name'), max_length=100)
    city = models.TextField(_('city'))
    commission = models.DecimalField(_('commission'), max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.full_name


class Customer(models.Model):
    name = models.CharField(_('name'), max_length=200)
    city = models.TextField(_('city'))
    grade = models.IntegerField(_('grade'))

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(_('title'), max_length=100)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Order(models.Model):
    order_id = models.AutoField(_('order_id'), primary_key=True)
    order_date = models.DateField(_('order_date'), default=date.today)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)
    total_price = models.DecimalField(_('total_price'), max_digits=20, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    Salesmen = models.ForeignKey(Salesman, related_name='Salesmen', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='order_detail', through='OrderProduct')

    def __str__(self):
        return str(self.order_id)

    # @property
    # def total_price(self):
    #     for p in self.products.all():
    #         total = p.price * self.quantity
    #         return total

    def product(self):
        return "\n".join([p.title for p in self.products.all()])


class OrderProduct(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
