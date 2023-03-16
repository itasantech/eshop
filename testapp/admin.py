from django.contrib import admin
from django.db.models import Count, Sum, F
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
# Register your models here.
from .models import Customer, Salesman, Order, Product, OrderProduct


# @admin.register(Salesman)
class SalesmanAdmin(TranslationAdmin):
    model = Salesman


# @admin.register(Customer)
class CustomerAdmin(TranslationAdmin):
    model = Customer


# @admin.register(Product)
class ProductAdmin(TranslationAdmin):
    model = Product


class OrderInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


class CustomerOrderInline(admin.TabularInline):
    model = Order
    extra = 1
    readonly_fields = ('products',)


@admin.register(Salesman)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'commission']
    inlines = [
        CustomerOrderInline,
    ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'grade']
    inlines = [
        CustomerOrderInline,
    ]

    def products(self, obj):
        return obj.get_value()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'quantity', 'total_price', 'order_date', 'customer', 'Salesmen', 'product']
    inlines = [
        OrderInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    inlines = [
        OrderInline,
    ]
