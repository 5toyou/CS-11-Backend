from django.shortcuts import render
from recipe.models import Recipies

# Create your views here.

def recepie_list(request):
    recepies = Recipies.objects.all()
    context = {
        'recepie_list': recepies,
    }
    return render(request, 'base.html', context)