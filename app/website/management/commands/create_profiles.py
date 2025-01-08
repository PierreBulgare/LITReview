from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import Profile

class Command(BaseCommand):
    help = 'Crée les profils pour les utilisateurs existants'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f'Profil créé pour l\'utilisateur {user.username}')
        self.stdout.write('Tous les profils manquants ont été créés.')
