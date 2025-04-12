from django.contrib import admin
from .models import Games, ProfileModel


class GamesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'genre', 'regular_price', 'release_date', 'company', 'games_lib', 'image']
    list_editable = ['name', 'genre', 'regular_price', 'release_date', 'company', 'games_lib', 'image']
    list_filter = ['name', 'genre', 'release_date']

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'contact_number')
    filter_horizontal = ('games_lib',)

# Register your models here.
admin.site.register(Games)
admin.site.register(ProfileModel, ProfileModelAdmin)
