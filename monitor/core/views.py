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
