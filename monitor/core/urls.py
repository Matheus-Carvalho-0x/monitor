from django.urls import path
from . import views

app_name = "monitor"

urlpatterns = [
    path('/', views.index_view, name="home"),
    path('/stores/', views.stores_view, name="stores"),
    path('/stores/<int:store_id>/', views.details_view, name="details")
]
