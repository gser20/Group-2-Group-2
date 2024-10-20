import string
import random
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render

def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request.session['captcha'] = captcha_text  # Save the CAPTCHA text in the session

    # Create CAPTCHA image
    img = Image.new('RGB', (250, 80), color='white')
    d = ImageDraw.Draw(img)

    # Set font size and load a font
    font_size = 30  # Increase font size here
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Adjust font size and type as needed
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if specific font cannot be loaded

    d.text((10, 20), captcha_text, fill=(0, 0, 0), font=font)

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

last_registered_email = ""
last_registered_password = ""
last_registered_first_name = ""
last_registered_last_name = ""

def home(request):
    global last_registered_email, last_registered_password, last_registered_first_name, last_registered_last_name

    if request.method == 'POST':
        if request.POST['captcha'] != request.session['captcha']:
            messages.error(request, 'Invalid Captcha, Please try again!')
            return render(request, 'auth/home.html')  # Re-render the page with error message
        else:
            last_registered_email = request.POST['email']
            last_registered_password = request.POST['password']
            last_registered_first_name = request.POST['first_name']
            last_registered_last_name = request.POST['last_name']

            hide_last_name = request.POST.get('hide_last_name') is not None
            request.session['hide_last_name'] = hide_last_name  # Store in session

            username = last_registered_email.split('@')[0]  # Extract the username

            while User.objects.filter(username=username).exists():
                username += str(random.randint(1, 1000))  # Append a random number if the username exists

            User.objects.create_user(username=username, email=last_registered_email, password=last_registered_password)
            return redirect('login')

    return render(request, 'auth/home.html')

def login_view(request):
    global last_registered_email, last_registered_password, last_registered_first_name, last_registered_last_name

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == last_registered_email and password == last_registered_password:
            return redirect('page', first_name=last_registered_first_name, last_name=last_registered_last_name)
        else:
            error = 'Invalid email or password'

    return render(request, 'auth/login.html', {'error': error})

def custom_logout(request):
    logout(request)
    return redirect('login')

def page_view(request, first_name, last_name):
    hide_last_name = request.session.get('hide_last_name', False)
    return render(request, 'homep/page.html', {
        'first_name': first_name,
        'last_name': last_name,
        'hide_last_name': hide_last_name,
    })

def forgot_password(request):
    if request.method == 'POST':
        # Handle form submission and security question verification here
        pass
    return render(request, 'auth/forgot.html')

def forgot_password_view(request):
    return render(request, 'auth/forgot.html')


def album_view(request, username):
    return render(request, 'auth/album.html', {'username': username})