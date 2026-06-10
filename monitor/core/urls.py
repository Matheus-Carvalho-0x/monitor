from django.urls import path
from . import views

app_name = "monitor"

urlpatterns = [
    path('/', views.index_view, name="home"),
    path('/stores/', views.stores_view, name="stores")
]
