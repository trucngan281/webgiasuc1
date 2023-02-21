from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import UserForm
from .utils import user_exist
from .utils import valid_username

def signin_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if user_exist(form):
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                print(username, password)
                user = authenticate(username=username, password=password)

                if user is not None:
                    messages.add_message(request, messages.INFO, 'Logged in!')

                    return redirect('home')

                # A backend authenticated the credentials
                else:
                    # No backend authenticated the credentials
                    return redirect('error') #TODO: build error page



    context = {
        'form' : form
    }
    return render(request, 'signup/signin.html', context)


def signup_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and valid_username(form):
            form.save()
            return redirect('home')
    context = {
        'form' : form
    }
    return render(request, 'signup/signup.html', context)
