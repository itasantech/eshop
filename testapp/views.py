import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .filters import SalesmanFilter
from .models import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics, permissions
from testapp.serializers import UserSerializer, CustomerSerializer, \
    OrderSerializer, ProductSerializer, SalesmanSerializer, SalesmanCommissionSerializer, \
    CustomerLessPurchaseSerializer, SalesmanMaxSalesSerializer, SalesmanSepOctCommissionSerializer, \
    SalesmanSepCommissionSerializer, CustomerCityHighestCommissionSerializer, CustomerUniqueGradesCommissionSerializer
from .tasks import *
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTl', DEFAULT_TIMEOUT)


# check celery
def celery(request):
    send_mail_task.delay()
    return HttpResponse("<h1>hello celery<h1>")


# Create your views here.
class Index(ListView):
    queryset = Salesman.objects.annotate(
        max_commission=Sum(F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100).order_by(
        '-max_commission')
    template_name = 'index.html'
    context_object_name = 'salesman'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SalesmanFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.filterset.form
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.all()
        context['total_customer'] = Customer.objects.all().count()
        context['max_com'] = Order.objects.values('Salesmen__full_name').annotate(
            commission=Sum(F('products__price') * F('quantity') * F('Salesmen__commission')) / 100).order_by(
            '-commission')[:1]
        context['less_pur'] = Order.objects.values('customer__name').annotate(
            purchase=Sum(F('products__price') * F('quantity'))).order_by('purchase')[:1]
        context['total_sales'] = Order.objects.values('Salesmen__full_name').annotate(
            sales=Sum(F('products__price') * F('quantity'))).order_by('-sales')
        context['order'] = Order.objects.all()
        context['total_order'] = Order.objects.all().count()
        context['total_salesmen'] = Salesman.objects.all().count()
        context['product'] = Product.objects.all()
        context['total_product'] = Product.objects.all().count()
        context['form'] = self.filterset.form
        return context


def max_val(request):
    customer_purchase = Order.objects.values('customer__name').annotate(
        purchase=Sum(F('products__price') * F('quantity'))).order_by('purchase')
    context = {'customer_purchase': customer_purchase}
    print(customer_purchase)
    data = json.dumps(context, indent=2, sort_keys=True, default=str)
    return JsonResponse(data, safe=False, )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = 'name', 'city'
    ordering_fields = '__all__'
    search_fields = 'name', 'city'
    # permission_classes = [permissions.IsAuthenticated]


class CustomerLessPurchase(generics.ListAPIView):
    queryset = Customer.objects.values('id').annotate(
        purchase=Sum(F('customers__products__price') * F('customers__quantity'))).order_by('purchase')[:1]
    serializer_class = CustomerLessPurchaseSerializer


class SalesmanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SalesmanFilter
    search_fields = 'id', 'full_name', 'city'

    # @method_decorator(cache_page(60 * 2))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class SalesmanCommission(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Salesman.objects.values('id').annotate(
        max_commission=Sum(
            F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
    serializer_class = SalesmanCommissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SalesmanFilter

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        print('check query params:', self.request.query_params)
        day = self.request.query_params.get('check_day')
        month = self.request.query_params.get('check_month')
        year = self.request.query_params.get('check_year')

        if day:
            if day and year:
                return status.HTTP_400_BAD_REQUEST
            elif day and month:
                return status.HTTP_400_BAD_REQUEST
            elif day and month and year:
                return status.HTTP_400_BAD_REQUEST
            else:
                queryset = Salesman.objects.filter(Salesmen__order_date__exact=day).values('id').annotate(
                    max_commission=Sum(
                        F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
            return queryset
        elif month and year:
            queryset = Salesman.objects.filter(Q(Salesmen__order_date__month=month) &
                                               Q(Salesmen__order_date__year=year)).values('id').annotate(
                max_commission=Sum(
                    F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
            return queryset
        elif month:
            queryset = Salesman.objects.filter(Salesmen__order_date__month=month).values('id').annotate(
                max_commission=Sum(
                    F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
            return queryset
        elif year:
            queryset = Salesman.objects.filter(Salesmen__order_date__year=year).values('id').annotate(
                max_commission=Sum(
                    F('Salesmen__products__price') * F('Salesmen__quantity') * F('commission')) / 100)
            return queryset
        else:
            return queryset


class SalesmanMaxSale(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Order.objects.filter(customer__city__exact='london').values('Salesmen_id').annotate(
        salesman_max_sale=Sum(F('products__price') * F('quantity'))).order_by('-salesman_max_sale')[:1]
    serializer_class = SalesmanMaxSalesSerializer


class SalesmanSepOctCommission(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Order.objects.filter(Q(order_date__month='9') | Q(order_date__month='10')).values(
        'Salesmen_id').annotate(
        september_october_commission=Sum(F('products__price') * F('quantity') * F('Salesmen__commission')) / 100)
    serializer_class = SalesmanSepOctCommissionSerializer


class SalesmanSepCommission(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Order.objects.filter(order_date__month='9').values('Salesmen_id') \
        .annotate(september_commission=Sum(F('products__price') * F('quantity') * F('Salesmen__commission')) / 100)
    serializer_class = SalesmanSepCommissionSerializer


class CustomerCityHighestCommission(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Order.objects.values('customer__city').annotate(
        customer_city_highest_commission=Sum(
            F('products__price') * F('quantity') * F('Salesmen__commission')) / 100).order_by(
        '-customer_city_highest_commission')[:1]
    serializer_class = CustomerCityHighestCommissionSerializer


class CustomerUniqueGradesCommission(generics.ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Order.objects.values('customer__grade').distinct() \
        .annotate(
        unique_grades_commission=Sum(F('products__price') * F('quantity') * F('Salesmen__commission')) / 100)
    serializer_class = CustomerUniqueGradesCommissionSerializer


# def list(self, request, *args, **kwargs):
#     # queryset = self.filter_queryset(self.get_queryset())
#     salesman_commission = Order.objects.values('Salesmen_id').annotate(
#         max_commission=Sum(F('products__price') * F('quantity') * F('Salesmen__commission')) / 100).order_by(
#         '-max_commission')
#     serializer = SalesmanCommissionSerializer(salesman_commission, many=True)
#     # page = self.paginate_queryset(queryset)
#     # if page is not None:
#     #     serializer = self.get_serializer(page, many=True)
#     #     return self.get_paginated_response(serializer.data)
#
#     # serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.queryset
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        # queryset = Order.objects.all()
        # print('query_params:', self.request.query_params)
        username = self.request.query_params.get('customer')
        salesmen = self.request.query_params.get('Salesmen')
        if username is not None:
            queryset = queryset.filter(customer_id=username)
        elif salesmen is not None:
            queryset = queryset.filter(Salesmen_id=salesmen)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #         queryset = Order.objects.all()
    #         # serializer = self.get_serializer(self.queryset, many=True)
    #         serializer = OrderSerializer(queryset)
    #         return Response(serializer.data)

    # def customer_list(self, request, pk):
    #     """
    #     List all code snippets, or create a new snippet.
    #     """
    #     try:
    #         customers = Customer.objects.get(pk=pk)
    #     except Customer.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     if request.method == 'GET':
    #         customer = Customer.objects.all()
    #         serializer = CustomerSerializer(customer, many=True)
    #         return Response(serializer.data)
    #
    #     elif request.method == 'POST':
    #         serializer = CustomerSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     elif request.method == 'PUT':
    #         serializer = CustomerSerializer(customers, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     elif request.method == 'DELETE':
    #         customers.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'salesmen-commission': reverse('accounts:salesmen-commission', request=request, format=format),
            'customer-less-purchase': reverse('accounts:customer-less-purchase', request=request, format=format),
            'salesmen-max-sales': reverse('accounts:salesmen-max-sales', request=request, format=format),
            'salesmen-sep-oct': reverse('accounts:salesmen-sep-oct', request=request, format=format),
            'salesmen-sep': reverse('accounts:salesmen-sep', request=request, format=format),
            'customer-city-highest-commission': reverse('accounts:customer-city-highest-commission', request=request,
                                                        format=format),
            'customer-unique-grades-commission': reverse('accounts:customer-unique-grades-commission', request=request,
                                                         format=format),
        })
