from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models

# Define models for direct use in the command (not for migrations)
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'
        managed = False
        db_table = 'users'

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        app_label = 'octofit_tracker'
        managed = False
        db_table = 'teams'

class Activity(models.Model):
    user_email = models.EmailField()
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        managed = False
        db_table = 'activities'

class Leaderboard(models.Model):
    team = models.CharField(max_length=50)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        managed = False
        db_table = 'leaderboard'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'
        managed = False
        db_table = 'workouts'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from djongo.database import connect
        from pymongo import MongoClient

        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index('email', unique=True)

        # Teams
        teams = [
            {'name': 'Marvel'},
            {'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Users
        users = [
            {'email': 'tony@stark.com', 'name': 'Tony Stark', 'team': 'Marvel'},
            {'email': 'steve@rogers.com', 'name': 'Steve Rogers', 'team': 'Marvel'},
            {'email': 'bruce@wayne.com', 'name': 'Bruce Wayne', 'team': 'DC'},
            {'email': 'clark@kent.com', 'name': 'Clark Kent', 'team': 'DC'}
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user_email': 'tony@stark.com', 'activity_type': 'Running', 'duration': 30},
            {'user_email': 'steve@rogers.com', 'activity_type': 'Cycling', 'duration': 45},
            {'user_email': 'bruce@wayne.com', 'activity_type': 'Swimming', 'duration': 60},
            {'user_email': 'clark@kent.com', 'activity_type': 'Flying', 'duration': 120}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 75},
            {'team': 'DC', 'points': 180}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Super Strength', 'description': 'Heavy lifting and resistance training.'},
            {'name': 'Flight Training', 'description': 'Aerobic and altitude training.'}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
