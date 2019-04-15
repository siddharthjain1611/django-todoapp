from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def login(request):
    print('The login page')

    return render(request, 'login.html')


@login_required
def logout(request):
    print('Logging Out')
    auth.logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


def authenticate(request):
    print('The authenticate request')
    # Get the form data from the request.
    username = request.POST.get('username')
    password = request.POST.get('password')

    print('Authenticating the user')
    user = auth.authenticate(request, username=username, password=password)

    # If authentication failed redirect back to the form
    # with messages.
    if not user:
        print('Login error')
        messages.error(request, 'Login failed. Please try again.')
        return redirect_back(request)

    # If authentication was successful
    auth.login(request, user)
    print('Login successful')

    # Add save success message
    messages.info(request, 'You are now logged in as {}.'.format(username))
    return redirect('index')

def signup(request):
    return render(request, 'signup.html')


def signup_submit(request):
    # Get the form data from the request.
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    # Validate username is not already taken.
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username {} is already taken.'.format(username))
        return redirect_back(request)

    # Validate email is not already taken.
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email {} is already taken.'.format(email))
        return redirect_back(request)

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
    except:
        user = None

    if not user:
        messages.error(request, 'Error creating a new user.')
        return redirect_back(request)

    messages.info(request, 'User has been created, you can login now.')
    return redirect('login')

def redirect_back(request):
    return redirect(request.META.get('HTTP_REFERER'))
