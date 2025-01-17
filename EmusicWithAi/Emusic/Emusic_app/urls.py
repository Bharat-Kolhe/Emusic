from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('subscription/', views.subscription, name='subscription'),
    # path('songs/', views.songs_view, name='songs'),
    # path('callback/', views.callback, name='callback'),
    # path('dashboard/search/', views.search, name='search'),
    path('spotify/dashboard/', views.spotify_dashboard,name='spotify_dashboard'),
    path('spotifylogin/',views.spotify_login,name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
   
    
    path('profile/', views.update_profile, name='profile'),
    path("update-password/", views.update_password, name="update_password"),
    path('notification/', views.notification, name='notification'),
    path('search/', views.search, name='search'),  # Handles search functionality
    path('category/', views.category, name='category'),
    
  
]   
