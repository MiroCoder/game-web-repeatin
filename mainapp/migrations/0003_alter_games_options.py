# Generated by Django 5.1.6 on 2025-02-22 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_rename_genre_games_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='games',
            options={'verbose_name': 'Game', 'verbose_name_plural': 'Games'},
        ),
    ]
