from django.shortcuts import render
from recipe.models import recipe

# Create your views here.

def recepie_list(request):
    recepies = recipe.objects.all()
    context = {
        'recepie_list': recepies,
    }
    return render(request, 'base.html', context)