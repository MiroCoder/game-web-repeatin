from django.urls import path
from mainapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.home, name='home'),
        path('login', views.login_view, name='login'),
        path('profile', views.profile_view, name='profile'),
        path('signup', views.signup, name='signup'),
        path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
        path('games', views.games, name='games'),
        path('login', views.login_view, name='login'),
        path('buy_game/<uuid:game_id>/', views.buy_game, name='buy_game'),
        path('delete_game/<uuid:game_id>/', views.delete_game, name='delete_game'),
]
