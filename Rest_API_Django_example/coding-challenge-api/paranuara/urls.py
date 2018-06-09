from django.urls import path
from django.urls import include, re_path
from django.conf.urls import url
from . import views

app_name = 'paranuara'

# URLs for different views
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('q1/', views.GetCompanyEmployees.as_view(), name='q1'),
    path('q2/', views.GetCommonFriends.as_view(), name='q2'),
    path('q3/', views.GetFavFruitsVegetables.as_view(), name='q3'),
]