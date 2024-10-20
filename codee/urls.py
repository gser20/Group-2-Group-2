from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *  # Import all views

urlpatterns = [
    # Admin and home routes
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('tweet/', include('tweets.urls')),
    # Album view route, placed first to avoid conflicts
    path('page/<str:username>/album.html', album_view, name='album'),

    # General page view route
    path('page/<str:first_name>/<str:last_name>/', page_view, name='page'),

    # Other routes
    path('logout/', custom_logout, name='logout'),
    path('captcha/', include('captcha.urls')),
    path('generate_captcha/', generate_captcha, name='generate_captcha'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]

# Serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)