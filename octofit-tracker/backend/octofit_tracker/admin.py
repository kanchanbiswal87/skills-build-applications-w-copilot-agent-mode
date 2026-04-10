from django.contrib import admin
from .models import Team, Profile, Activity, Workout, Leaderboard

admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(Workout)
admin.site.register(Leaderboard)
