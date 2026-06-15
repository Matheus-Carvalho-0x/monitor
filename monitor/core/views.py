from django.shortcuts import render
from .models import TestStore, TestEnviroments, TestValues

# Create your views here.
def index_view(request):
    return render(request, 'core/index.html')

def stores_view(request):
    context = {
        "stores": TestStore.objects.all()
    }

    return render(request, 'core/stores.html', context)

def details_view(request, store_id):
    enviroment_list = TestEnviroments.objects.filter(test_store_id_id=store_id)
    context = {
        "env": enviroment_list
    }
    return render(request, 'core/enviroments.html', context)
