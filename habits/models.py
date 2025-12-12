from django.db import models
from django.contrib.auth.models import User

MOOD_CHOICES = [
    (1, "😞"),
    (2, "😐"),
    (3, "🙂"),
    (4, "😄"),
    (5, "🤩"),
]

SLEEP_DURATION_CHOICES = [
    (1, "4h-"),
    (2, "5h"),
    (3, "6h"),
    (4, "7h"),
    (5, "8h"),
    (6, "9h+"),
]


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100) 
    # for future use incase I want to add more activities rather than mood
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class MoodEntry(models.Model):
    habit = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="entries", null=True, blank=True)
    date = models.DateField()
    
    # mood tracking
    mood = models.IntegerField(choices=MOOD_CHOICES)
    
    # wellness metrics
    yoga = models.BooleanField(default=False)
    sleep_duration = models.IntegerField(
        choices=SLEEP_DURATION_CHOICES,
        null=True,
        blank=True
    )

    # notes
    note = models.TextField(blank=True)


    class Meta:
        unique_together = ("habit", "date")

    def __str__(self):
        return f"{self.habit.name} @ {self.date}"
