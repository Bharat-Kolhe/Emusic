from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

from Emusic_app.models import Artist, Song

from .forms import SearchForm
from django.db.models import Q 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import default_storage




# Create your views here.
def home(request):
    return render(request,'home.html')

def user_login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
             messages.error(request, "Username already exist! Please try another username!")
             return redirect('signup')
        
        if User.objects.filter(email=email):
             messages.error(request, "Email alrady Registered")
             return redirect('signup')
        
        if len(username)>15:
             messages.error(request, "Username must be under 15 characters")
            
        if pass1 != pass2:
             messages.error(request, "Password didn't match")

        if not username.isalpha():
             messages.error(request, "Username must be Alpha-Numeric!")
             return redirect('signup')
    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created succesfully.")
        return redirect('login')

    return render(request,"signup.html")

def signout(request):
        logout(request)
        messages.success(request, "Logged out Successfully")
        return redirect('home')



def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required

def update_profile(request):
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            
            # Define a path for saving the uploaded profile picture
            profile_pic_path = os.path.join('profile_pictures', profile_picture.name)
            
            # Save the file to the media folder
            file_path = default_storage.save(profile_pic_path, profile_picture)
            user.profile.profile_picture = file_path  # Assuming `profile` is a related model for user profile
            
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Replace 'profile' with your profile page URL name

    # Prepopulate user information in the template
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'profile.html', context)


@login_required
def update_password(request):
    """View for updating the user's password."""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Keep the user logged in after changing the password
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "update_password.html", {"form": form})
def subscription(request):
    return render(request, 'subscription_plans.html')

def dashboard(request):
    return render(request, 'dashboard.html')
from django.conf import settings
from django.shortcuts import render, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


# def songs_view(request):
#     # Get the Spotify client
#     sp = get_spotify_client()
    
#     # Fetch data from Spotify (for example, popular tracks)
#     results = sp.current_user_top_tracks(limit=10)  # Fetch top 10 tracks
#     tracks = results['items']

#     return render(request, 'songs.html', {'tracks': tracks})

# def callback(request):
#     # Spotify OAuth callback handler
#     sp_oauth = SpotifyOAuth(client_id=settings.SPOTIPY_CLIENT_ID,
#                              client_secret=settings.SPOTIPY_CLIENT_SECRET,
#                              redirect_uri=settings.SPOTIPY_REDIRECT_URI,
#                              scope="user-library-read")
#     token_info = sp_oauth.get_access_token(request.GET['code'])
#     sp = Spotify(auth=token_info['access_token'])

#     return redirect('/songs/')

def search(request):
    return render(request,'search.html')


def notification(request):
    return render(request,'notification.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings



def category(request):
    return render(request, 'category.html')





# import requests
# from django.shortcuts import redirect, render
# from django.conf import settings

def spotify_dashboard(request):
    """Displays a simple Spotify dashboard."""
    access_token = request.session.get('spotify_access_token')
    if not access_token:
        return redirect('spotify_login')

    # Fetch user's Spotify data
    user_profile_url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_profile_url, headers=headers)
    user_data = user_response.json()

    redirect_url = f"https://open.spotify.com?access_token={access_token}"
    return HttpResponseRedirect(redirect_url)

def spotify_login(request):
    """Redirects to Spotify for user authorization."""
    scope = "user-read-private user-read-email"  # Add scopes as required
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code"
        f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
        f"&scope={scope}"
    )
    return redirect(auth_url)

def spotify_callback(request):
    """Handles Spotify callback and fetches an access token."""
    code = request.GET.get('code')
    if not code:
        return render(request, 'error.html', {"message": "Authorization failed."})

    # Exchange the authorization code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()

    access_token = response_data.get('access_token')
    if not access_token:
        return render(request, 'error.html', {"message": "Failed to get access token."})
    print(access_token)
    # Save the access token in the session
    request.session['spotify_access_token'] = access_token
    return redirect('spotify_dashboard')  # Redirect to a page to browse Spotify contentfrom django.shortcuts import render

from django.shortcuts import render
from .forms import SearchForm
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Setup Spotify authentication
def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(client_id='3822ebda03344da681e15f1f382eb1d0', client_secret='')
    sp = Spotify(client_credentials_manager=client_credentials_manager)
    return sp

# Create a view for the search results
def search(request):
    """Handles searching for songs and artists from Spotify."""
    results = None
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Retrieve the access token from session
            access_token = request.session.get('spotify_access_token')
            if not access_token:
                return redirect('spotify_login')  # If there's no access token, redirect to login

            # Use the access token to authenticate the Spotify API
            sp = spotipy.Spotify(auth=access_token)

            # Search Spotify for songs and artists
            try:
                results = sp.search(q=query, limit=10)  # Adjust the limit as needed
            except spotipy.exceptions.SpotifyException as e:
                return render(request, 'error.html', {"message": f"Error: {str(e)}"})
    else:
        form = SearchForm()

    return render(request, 'search_results.html', {'form': form, 'results': results})
    