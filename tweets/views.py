from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tweet

# Create your views here.
def tweet_detail_view(request, pk=None):
    obj = Tweet.objects.get(pk=pk)
    print(obj)
    context = {
        'object': obj,
    }
    return render(request, 'tweets/detail_view.html', {})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    print(qs)
    context = {
        'query': qs,
    }
    return render(request, 'tweets/list_view.html', {})




class TweetListView(ListView):
    queryset = Tweet.objects.all()
    template_name = 'tweets/list_view.html'




class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()
    template_name = 'tweets/detail_view.html'

    def get_object(self, queryset=Tweet.objects.all()):
        print(self.kwargs)
        pk=self.kwargs.get('pk')
        print(pk)
        return Tweet.object.get(id=pk)

def home(request):
    return render(request, 'auth/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # If everything is fine, create a new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'register.html')