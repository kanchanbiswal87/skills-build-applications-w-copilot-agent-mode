from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection

from djongo import models

# Define models for test data (if not already defined in models.py)
# For demonstration, we use Django's built-in User and create simple models for Team, Activity, Leaderboard, Workout

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()
        app_models.Profile.objects.all().delete()
        User.objects.all().exclude(is_superuser=True).delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Team Marvel')
        dc = app_models.Team.objects.create(name='Team DC')

        # Create Users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            # Ensure profile exists and assign team
            profile = app_models.Profile.objects.get(user=user)
            profile.team = u['team']
            profile.save()
            user_objs.append(user)

        # Create Activities
        for user in user_objs:
            app_models.Activity.objects.create(user=user, type='run', duration=30)
            app_models.Activity.objects.create(user=user, type='cycle', duration=45)

        # Create Workouts
        for user in user_objs:
            app_models.Workout.objects.create(user=user, name='Morning Cardio', description='Cardio session', duration=40)

        # Create Leaderboard
        app_models.Leaderboard.objects.create(team=marvel, points=100)
        app_models.Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
