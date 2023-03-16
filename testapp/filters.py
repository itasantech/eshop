from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Case, When, Value
from django.forms import DateInput
from django.utils.timezone import now
from django_filters import rest_framework as filters
from .models import *


class SalesmanFilter(filters.FilterSet):
    full_name = filters.CharFilter(field_name='full_name', label=_('full name'), lookup_expr='icontains')
    less_commission = filters.NumberFilter(field_name='max_commission', label=_('less than commission'),
                                           lookup_expr='lte')
    greater_commission = filters.NumberFilter(field_name='max_commission', label=_('greater than commission'),
                                              lookup_expr='gte')
    # check_day = filters.DateFilter(label='check_day',
    #                                widget=DateInput(attrs={'type': 'date'}))
    # check_month = filters.NumberFilter(label='check_month')
    # check_year = filters.NumberFilter(label='check_year')

# class DateFunction:
#     def __init__(self, day, month, year):
#         self.day = day
#         self.month = month
#         self.year = year

#
#     def execute(self):
#         return Salesman.objects.filter(Q(Salesmen__order_date__month=self.month) |
#                                        Q(Salesmen__order_date__year=self.year) |
#                                        Q(Salesmen__order_date__exact=self.day)).values(
#             'id').annotate(
#             max_commission=Sum(F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
