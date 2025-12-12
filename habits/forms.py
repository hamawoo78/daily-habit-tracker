from django import forms
from .models import Habit, HabitEntry, MOOD_CHOICES
from datetime import date

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "category"]


class HabitEntryForm(forms.ModelForm):
    date = forms.DateField(initial=date.today, widget=forms.HiddenInput())

    class Meta:
        model = HabitEntry
        fields = ["mood", "note", "date"]
        widgets = {
            "mood": forms.RadioSelect(choices=MOOD_CHOICES),
            "note": forms.Textarea(attrs={"rows": 2}),
        }
