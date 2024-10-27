import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Journal, Souvenir
from .jurnalform import JournalForm
from django.http import JsonResponse
import json
from django.core import serializers

@login_required
def landing_page(request):
    return render(request, 'main/landing_page.html', {'user': request.user})


@login_required(login_url='/login')
def journal_home(request):
    journals = Journal.objects.all().order_by('-created_at')

    # Membaca data dari file JSON
    with open('main/DATASET.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Memasukkan data ke dalam model Souvenir
    for item in data:
        Souvenir.objects.get_or_create(
            name=item['Product Name'],
            defaults={
                'price': item['Price'],
                'description': item['Description Product'],
                'place_name': item['Place Name']
            }
        )

    # Ambil semua souvenir dari database
    souvenirs = Souvenir.objects.all()

    # Filter berdasarkan nama tempat
    place_name_filter = request.GET.get('place_name')
    if place_name_filter:
        souvenirs = souvenirs.filter(place_name=place_name_filter)

    # Filter berdasarkan harga
    price_filter = request.GET.get('price')
    if price_filter == 'low_to_high':
        souvenirs = souvenirs.order_by('price')
    elif price_filter == 'high_to_low':
        souvenirs = souvenirs.order_by('-price')

    # Ambil semua nama tempat untuk dropdown
    places = Souvenir.objects.values_list('place_name', flat=True).distinct()

    return render(request, 'main/journal_home.html', {
        'journals': journals,
        'souvenirs': souvenirs,
        'places': places,
    })
   
@login_required(login_url='/login')
def create_journal(request):
    # Ambil souvenir_id dari query parameter jika ada
    souvenir_id = request.GET.get('souvenir_id')

    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.author = request.user
            
            # Jika souvenir_id ada, kaitkan dengan jurnal
            if souvenir_id:
                souvenir = get_object_or_404(Souvenir, id=souvenir_id)
                journal.souvenir = souvenir  # Asumsikan ada field 'souvenir' di model Journal
            
            journal.save()
            return redirect('main:journal_home')
    else:
        form = JournalForm()
    
    return render(request, 'main/create_journal.html', {'form': form, 'souvenir_id': souvenir_id})

@login_required(login_url='/login')
def like_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if request.user.is_authenticated:
        if request.user in journal.likes.all():
            journal.likes.remove(request.user)  # Hapus like jika sudah ada
            liked = False
        else:
            journal.likes.add(request.user)  # Tambah like jika belum ada
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': journal.likes.count()})
    return JsonResponse({'error': 'User not authenticated'}, status=401)

def souvenir_list(request):
    souvenirs = Souvenir.objects.all()

    # Filter berdasarkan harga
    price_filter = request.GET.get('price')
    if price_filter == 'low_to_high':
        souvenirs = souvenirs.order_by('price')
    elif price_filter == 'high_to_low':
        souvenirs = souvenirs.order_by('-price')

    # Filter berdasarkan rating
    rating_filter = request.GET.get('rating')
    if rating_filter == 'high_to_low':
        souvenirs = souvenirs.order_by('-rating')
    elif rating_filter == 'low_to_high':
        souvenirs = souvenirs.order_by('rating')

    return render(request, 'main/souvenir_list.html', {'souvenirs': souvenirs})


@login_required(login_url='/login')
def journal_history(request):
    journals = Journal.objects.filter(author=request.user)
    return render(request, 'main/journal_history.html', {'journals': journals})

def specific_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/specific_journal.html', {'journal': journal})

@login_required(login_url='/login')
def edit_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)

    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            # Check if the "Clear Image" checkbox is checked
            if 'delete_image' in request.POST and request.POST['delete_image'] == 'on':
                if journal.image:
                    journal.image.delete(save=False)  # Delete image from filesystem
                journal.image = None  # Set image to None

            form.save()  # Save changes
            return JsonResponse({
                'title': journal.title,
                'content': journal.content,
                'image_url': journal.image.url if journal.image else None,
            })  # Return updated journal data as JSON
    elif request.method == 'GET':
        # Return journal data for editing
        data = {
            'title': journal.title,
            'content': journal.content,
            'image_url': journal.image.url if journal.image else None,
        }
        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
# def edit_journal(request, journal_id):
#     journal = get_object_or_404(Journal, id=journal_id)

#     if request.method == 'POST':
#         form = JournalForm(request.POST, request.FILES, instance=journal)
#         if form.is_valid():
#             # Check if the "Clear Image" checkbox is checked
#             if 'delete_image' in request.POST:
#                 journal.image.delete(save=False)  # Delete image from filesystem
#                 journal.image = None  # Set image to None

#             form.save()  # Save changes
#             return JsonResponse({
#                 'title': journal.title,
#                 'content': journal.content,
#                 'image_url': journal.image.url if journal.image else None,
#             })  # Return updated journal data as JSON
#     elif request.method == 'GET':
#         # Return journal data for editing
#         data = {
#             'title': journal.title,
#             'content': journal.content,
#             'image_url': journal.image.url if journal.image else None,
#         }
#         return JsonResponse(data)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
    # journal = get_object_or_404(Journal, id=journal_id)

    # if request.method == 'POST':
    #     form = JournalForm(request.POST, request.FILES, instance=journal)
    #     if form.is_valid():
    #         # Check if the "Clear Image" checkbox is checked
    #         if 'delete_image' in request.POST:
    #             journal.image.delete(save=False)  # Delete image from filesystem
    #             journal.image = None  # Set image to None

    #         form.save()  # Save changes
    #         return JsonResponse({
    #             'title': journal.title,
    #             'content': journal.content,
    #             'image_url': journal.image.url if journal.image else None,
    #         })  # Return updated journal data as JSON
    # elif request.method == 'GET':
    #     # Return journal data for editing
    #     data = {
    #         'title': journal.title,
    #         'content': journal.content,
    #         'image_url': journal.image.url if journal.image else None,
    #     }
    #     return JsonResponse(data)

    # return JsonResponse({'error': 'Invalid request'}, status=400)
# def edit_journal(request, journal_id):
#     journal = get_object_or_404(Journal, id=journal_id)

#     if request.method == 'POST':
#         form = JournalForm(request.POST, request.FILES, instance=journal)
#         if form.is_valid():
#             # Cek apakah checkbox "Clear Image" dicentang
#             if 'clear_image' in request.POST:
#                 journal.image.delete(save=False)  # Hapus gambar dari filesystem
#                 journal.image = None  # Set gambar ke None

#             form.save()  # Simpan perubahan
#             return redirect('main:journal_history')  # Redirect setelah menyimpan
#     else:
#         form = JournalForm(instance=journal)

#     return render(request, 'main/edit_journal.html', {'form': form})


@login_required(login_url='/login')
def delete_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id, author=request.user)
    journal.delete()
    return redirect('main:journal_home')

@login_required
def save_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    SavedJournal.objects.get_or_create(journal=journal, user=request.user)
    return redirect('journal_home')

def journal_detail(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/spesific_journal.html', {'journal': journal})


def register(request):
    form = UserCreationForm()
    last_login = request.COOKIES.get('last_login', 'Never')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form, 'last_login': last_login}
    return render(request, 'register.html', context)

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('main:journal_home')  # Ganti 'home' dengan nama URL halaman utama Anda
#         else:
#             # Tambahkan pesan error jika login gagal
#             return render(request, 'login.html', {'error': 'Invalid username or password'})
#     return render(request, 'login.html')
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:journal_home')  # Arahkan ke journal_home setelah login
            else:
                form.add_error(None, "Invalid username or password.")  # Tambahkan error jika autentikasi gagal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def show_xml(request):
    # Get all journals for the current user
    data = Journal.objects.filter(author=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    # Get all journals for the current user
    data = Journal.objects.filter(author=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    # Get a specific journal by ID
    data = Journal.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    # Get a specific journal by ID
    data = Journal.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")