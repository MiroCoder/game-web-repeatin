from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import SignUpForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from wheel.metadata import _
from .models import ProfileModel, Games
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def games(request):
    all_games = Games.objects.all()
    return render(request, 'games.html', {'games': all_games})

@login_required
def buy_game(request, game_id):
    game = get_object_or_404(Games, id=game_id)
    profile = ProfileModel.objects.get(user=request.user)

    if game in profile.games_lib.all():
        messages.warning(request, "You already own this game!")
    else:
        profile.games_lib.add(game)
        profile.save()
        messages.success(request, f"You have successfully purchased {game.name}!")

    return redirect('games')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()

            if not ProfileModel.objects.filter(user=user).exists():
                profile = ProfileModel.objects.create(
                    user=user,
                    full_name=form.cleaned_data['full_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    location=form.cleaned_data['location'],
                    gender=form.cleaned_data['gender'],
                    contact_number=form.cleaned_data['contact_number']
                )
                profile.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, "Completed!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = ProfileModel.objects.get(user=user)
        games_in_lib = user_profile.games_lib.all()
        # games = user_profile.games_lib.all()
        # medical_record = MedicalRecordModel.objects.get(patient=user_profile)
        context = {
            'user': user,
            'profile': user_profile,
            # 'medical_record': medical_record,
            'additional_info': {
                'full_name': user_profile.full_name,
                'birth_date': user_profile.birth_date,
                'gender': user_profile.get_gender_display(),
                'location': user_profile.location,
                'contact_number': user_profile.contact_number,
                'games': games_in_lib,
                # 'my games': user_profile.games_lib

            }
        }
        return render(request, 'profile.html', context)
    except ProfileModel.DoesNotExist:
        return HttpResponse("Профиль не существует.")
    # except MedicalRecordModel.DoesNotExist:
    #     return HttpResponse("Медицинская карта не существует.")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def delete_game(request, game_id):
    game = Games.objects.get(id=game_id)
    if game in request.user.additional_info.games.all():
        request.user.additional_info.games.remove(game)
    return redirect('profile')