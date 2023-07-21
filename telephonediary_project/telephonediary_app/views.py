from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import auth
from .forms import RegisterForm, PhoneForm
from .models import Contact

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        try:
            User.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'error': 'email is already taken!'})
        except User.DoesNotExist:
            User.objects.create_user(request.POST['username'], password=request.POST['password'],
                                     email=request.POST['email'])

            return redirect('login')
    else:
        return render(request, 'signup.html', {'error': 'password does not match!'})

def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('telephone_diary')
        else:
            return render(request, 'login.html', {'error': 'email or password is incorrect!'})
    else:
        return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('telephone_diary')

@login_required(login_url='/login')
def telephone_diary(request):
    search_query = request.GET.get('search')
    if search_query:
        contacts = Contact.objects.filter(
            Q(name__icontains=search_query) |
            Q(state__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(number__icontains=search_query),
            user=request.user
        )
    else:
        contacts = Contact.objects.filter(user=request.user)

    return render(request, 'telephone_diary.html', {'contacts': contacts})

def add_phone_number(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.save(commit=False)
            phone_number.user = request.user
            phone_number.save()
            return redirect('telephone_diary')
    else:
        form = PhoneForm()
    return render(request, 'add_telephonediary.html', {'form': form})


def edit_phone_number(request, pk):
    phone_number = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=phone_number)
        if form.is_valid():
            form.save()
            return redirect('telephone_diary')
    else:
        form = PhoneForm(instance=phone_number)
    return render(request, 'edit_telephonediary.html', {'form': form, 'phone_number': phone_number})