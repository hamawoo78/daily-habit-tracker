import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from habits.models import MoodEntry, Action


User = get_user_model()

# Your choices from models.py
SLEEP_CHOICES = [1, 2, 3, 4, 5, 6]  # 4h-, 5h, 6h, 7h, 8h, 9h+
MOOD_CHOICES = [1, 2, 3, 4, 5]      # 😞 😐 🙂 😄 🤩


def clamp(n, low, high):
    return max(low, min(high, n))


class Command(BaseCommand):
    help = "Seed mock MoodEntry data for the last N days for a given user."

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, required=True, help="Username to seed data for")
        parser.add_argument("--days", type=int, default=90, help="How many days back (default: 90)")
        parser.add_argument("--overwrite", action="store_true", help="Delete existing entries in range first")

    @transaction.atomic
    def handle(self, *args, **options):
        username = options["username"]
        days = options["days"]
        overwrite = options["overwrite"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User '{username}' not found. Create it first."))
            return

        # Get or create the default habit for this user
        habit, created = Action.objects.get_or_create(
            user=user,
            name="Daily Mood"
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created 'Daily Mood' habit for user '{username}'"))

        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        if overwrite:
            deleted, _ = MoodEntry.objects.filter(habit=habit, date__range=(start_date, end_date)).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing entries in range."))

        created_count = 0
        skipped_count = 0

        # Optional: add a very simple repeating "cycle" effect (~28 days)
        # This is NOT medical accuracy—just a realistic-looking pattern for mock data.
        cycle_length = 28
        cycle_low_mood_days = set(range(0, 3))  # first 3 days of cycle slightly lower mood

        for i in range(days):
            d = start_date + timedelta(days=i)

            # Skip if already exists
            if MoodEntry.objects.filter(habit=habit, date=d).exists():
                skipped_count += 1
                continue

            weekday = d.weekday()  # 0=Mon ... 6=Sun
            is_weekend = weekday >= 5

            # Yoga probability: more likely on weekends
            yoga = random.random() < (0.45 if is_weekend else 0.25)

            # Sleep duration: a bit higher on weekends
            sleep = random.choices(
                population=SLEEP_CHOICES,
                weights=[5, 12, 20, 25, 22, 16] if not is_weekend else [3, 8, 15, 25, 28, 21],
                k=1
            )[0]

            # Base mood around neutral
            mood = random.choices(
                population=MOOD_CHOICES,
                weights=[8, 18, 34, 26, 14],
                k=1
            )[0]

            # Correlate mood with sleep and yoga a bit (makes it look realistic)
            if sleep >= 5:  # 8h or 9h+
                mood += 1
            elif sleep <= 2:  # 4h- or 5h
                mood -= 1

            if yoga:
                mood += 1

            # Add small weekly pattern (Mondays slightly harder)
            if weekday == 0:
                mood -= 1

            # Add simple cycle pattern
            cycle_day = i % cycle_length
            if cycle_day in cycle_low_mood_days:
                mood -= 1

            mood = clamp(mood, 1, 5)

            # Optional notes (keep light so it’s not repetitive)
            note = ""
            if yoga and mood >= 4:
                note = "Good energy today. Yoga helped."
            elif mood <= 2 and sleep <= 2:
                note = "Low energy day. Sleep was short."
            elif mood >= 4 and sleep >= 4:
                note = "Felt productive and calm."
            elif weekday == 0 and mood <= 3:
                note = "Monday reset. Taking it step by step."

            MoodEntry.objects.create(
                habit=habit,
                date=d,
                mood=mood,
                yoga=yoga,
                sleep_duration=sleep,
                note=note,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeding complete for '{username}'. Created: {created_count}, Skipped: {skipped_count} "
            f"({start_date} → {end_date})"
        ))
