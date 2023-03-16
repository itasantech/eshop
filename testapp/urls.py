from django.urls import path, include
from testapp import views

app_name = 'accounts'
urlpatterns = [
    path('', views.ApiRoot.as_view(), name='root'),
    path('celery', views.celery, name='celery'),
    path('index', views.Index.as_view(), name='index'),
    path('salesmen-commission', views.SalesmanCommission.as_view(), name='salesmen-commission'),
    path('customer-less-purchase', views.CustomerLessPurchase.as_view(), name='customer-less-purchase'),
    path('salesmen-max-sales', views.SalesmanMaxSale.as_view(), name='salesmen-max-sales'),
    path('salesmen-sep-oct', views.SalesmanSepOctCommission.as_view(), name='salesmen-sep-oct'),
    path('salesmen-sep', views.SalesmanSepCommission.as_view(), name='salesmen-sep'),
    path('customer-city-highest-commission', views.CustomerCityHighestCommission.as_view(),
         name='customer-city-highest-commission'),
    path('customer-unique-grades-commission', views.CustomerUniqueGradesCommission.as_view(),
         name='customer-unique-grades-commission'),
    path('maxval', views.max_val, name='maxval'),
    path('datacache', views.TestCacheView.as_view(), name='datacache'),
    path('event', views.GoogleCalendarEvents.as_view(), name='event'),
    path('create-event/', views.create_event),
]
