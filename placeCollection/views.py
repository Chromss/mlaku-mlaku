from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CollectionForm
from .models import Collection


def show_collections(request):
    collection = Collection.objects.all()
    context = {
        'collection': collection,  # Mengirimkan daftar koleksi ke template
    }
    return render(request, "collection.html", context)


def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            collection = Collection.objects.create(name=name)
            return JsonResponse({
                'success': True,
                'name': collection.name,
                'created_at': date_format(collection.created_at, format='M d, Y'),
                'id': collection.id
            })
        return JsonResponse({'success': False, 'error': 'Name is required'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})