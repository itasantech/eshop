from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Sum, F, Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from decimal import Decimal

from rest_framework.response import Response

from testapp.models import Customer, Salesman, Order, OrderProduct, Product
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class OrderSerializer(serializers.ModelSerializer):
    # products = serializers.StringRelatedField(many=True, read_only=True)
    # Salesmen = serializers.PrimaryKeyRelatedField(read_only=True)
    # customer = serializers.SlugRelatedField(read_only=True, slug_field='name')
    order_id = serializers.SerializerMethodField(read_only=True)

    # total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    # def get_total_price(self, obj):
    #     tax = Decimal(10.5)
    #     return obj.total_price + tax

    def get_order_id(self, obj):
        prefix_num = 'xpg600j#'
        return f'{obj}{prefix_num}'


class OrderCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_date']


class SalesmanSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Salesman.objects.all())
    orders = OrderSerializer(many=True, read_only=True, source='Salesmen')

    class Meta:
        model = Salesman
        fields = ['id', 'full_name', 'city', 'commission', 'orders']


class SalesmanCustomSerializer(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(queryset=Salesman.objects.all())
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = Salesman
        fields = ['full_name', 'city']

    # def get_full_name(self, obj):
    #     return obj.full_name.upper()


class SalesmanCommissionSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    max_commission = serializers.FloatField(read_only=True)

    # salesman_september_commission = serializers.SerializerMethodField(read_only=True)
    # customer_city_highest_commission = serializers.SerializerMethodField(read_only=True)
    # unique_grades_commission = serializers.SerializerMethodField(read_only=True)
    def get_id(self, obj):
        # obj['Salesmen_id'] = obj['Salesmen_id']
        query = Salesman.objects.get(pk=obj['id'])
        qs = SalesmanCustomSerializer(many=True, read_only=True, instance=[query]).data
        return obj['id'], qs


class SalesmanMaxSalesSerializer(serializers.Serializer):
    Salesmen_id = serializers.SerializerMethodField(read_only=True)
    salesman_max_sale = serializers.FloatField(read_only=True)

    def get_Salesmen_id(self, obj):
        query = Salesman.objects.get(pk=obj['Salesmen_id'])
        qs = SalesmanCustomSerializer(many=True, read_only=True, instance=[query]).data
        return obj['Salesmen_id'], qs


class SalesmanSepOctCommissionSerializer(serializers.Serializer):
    Salesmen_id = serializers.SerializerMethodField(read_only=True)
    september_october_commission = serializers.FloatField(read_only=True)

    def get_Salesmen_id(self, obj):
        query = Salesman.objects.get(pk=obj['Salesmen_id'])
        qs = SalesmanCustomSerializer(many=True, read_only=True, instance=[query]).data
        return obj['Salesmen_id'], qs


class SalesmanSepCommissionSerializer(serializers.Serializer):
    Salesmen_id = serializers.SerializerMethodField(read_only=True)
    september_commission = serializers.FloatField(read_only=True)

    def get_Salesmen_id(self, obj):
        query = Salesman.objects.get(pk=obj['Salesmen_id'])
        qs = SalesmanCustomSerializer(many=True, read_only=True, instance=[query]).data
        return obj['Salesmen_id'], qs


class CustomerCityHighestCommissionSerializer(serializers.Serializer):
    customer__city = serializers.CharField(read_only=True)
    customer_city_highest_commission = serializers.FloatField(read_only=True)

    # def get_id(self, obj):
    #     query = Customer.objects.get(pk=obj['id'])
    #     qs = CustomerCustomSerializer(many=True, read_only=True, instance=[query]).data
    #     return obj['id'], qs


class CustomerUniqueGradesCommissionSerializer(serializers.Serializer):
    customer__grade = serializers.CharField(read_only=True)
    unique_grades_commission = serializers.FloatField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    orders = OrderSerializer(many=True, read_only=True, source='customers')

    class Meta:
        model = Customer
        fields = 'id', 'name', 'city', 'grade', 'orders'


class CustomerCustomSerializer(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = 'name', 'city', 'grade'


class CustomerLessPurchaseSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    purchase = serializers.FloatField(allow_null=False)

    def get_id(self, obj):
        query = Customer.objects.get(pk=obj['id'])
        qs = CustomerCustomSerializer(many=True, read_only=True, instance=[query]).data
        return obj['id'], qs
        # def get_grade(self, instance):


#     if instance.grade < 20:
#         return "less then 20"
#     elif instance.grade < 60:
#         return "less then 60"


class EventSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    summary = serializers.CharField(max_length=250)
    description = serializers.CharField(required=False)
    attendees = serializers.ListField(allow_null=True)
    # start = serializers.DateTimeField()
    # end = serializers.DateTimeField()


from datetime import datetime, timedelta


class EventsSerializer(serializers.Serializer):
    summary = serializers.CharField()
    start_time = serializers.DateTimeField(input_formats=['iso-8601'])
    end_time = serializers.DateTimeField(input_formats=['iso-8601'])

    def create(self, validated_data):
        summary = validated_data['summary']
        start_time = validated_data['start_time'].replace(tzinfo=None)
        end_time = validated_data['end_time'].replace(tzinfo=None)
        return {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': True,
            },
        }
