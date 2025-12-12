from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Action, MoodEntry
from datetime import date
import calendar
import json

def habits_tracker(request):
    """Main mood tracker page"""
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Check if any users exist in the system (first time app usage)
        if not User.objects.exists():
            # First time using the app - redirect to signup
            messages.info(request, 'Welcome to Do Your Best! 🌟 Create your account to start your wellness journey.')
            return redirect('signup_view')
        else:
            # Users exist but this one isn't logged in - redirect to login
            messages.info(request, 'Please log in to access your habit tracker.')
            return redirect('login_view')
    
    # Get or create the default habit for this user
    action, created = Action.objects.get_or_create(
        user=request.user,
        name="Daily Mood"
    )
    
    if request.method == 'POST':
        mood = request.POST.get('mood')
        sleep_duration = request.POST.get('sleep_duration')
        yoga = request.POST.get('yoga')
        note = request.POST.get('note', '')
        
        # Validation
        if not mood or not sleep_duration or not yoga:
            messages.error(request, 'Please complete all required fields!')
            return redirect('habits_tracker')
        
        # Convert yoga to boolean
        yoga_bool = True if yoga == 'yes' else False
        
        # Get today's date
        today = date.today()
        
        # Check if entry already exists for today
        existing_entry = MoodEntry.objects.filter(
            habit=action,
            date=today
        ).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.mood = int(mood)
            existing_entry.sleep_duration = int(sleep_duration)
            existing_entry.yoga = yoga_bool
            existing_entry.note = note
            existing_entry.save()
            messages.success(request, '🌟 Entry updated! You\'re doing your best! 🌟')
        else:
            # Create new mood entry
            MoodEntry.objects.create(
                habit=action,
                date=today,
                mood=int(mood),
                sleep_duration=int(sleep_duration),
                yoga=yoga_bool,
                note=note
            )
            messages.success(request, '🌟 Entry saved! You\'re doing your best! 🌟')
        
        return redirect('habits_tracker')
    
    # Get today's date
    today = date.today()
    
    # Check if user already has an entry for today
    today_entry = MoodEntry.objects.filter(
        habit=action,
        date=today
    ).first()
    
    context = {
        'username': request.user.first_name or request.user.username,
        'today': today,
        'today_entry': today_entry,
    }
    
    return render(request, 'index.html', context)


@login_required
def mood_history(request):
    """View mood history with monthly calendar"""
    # Get the user's Daily Mood habit
    try:
        habit = Action.objects.get(user=request.user, name="Daily Mood")
    except Action.DoesNotExist:
        habit = None
    
    # Get year and month from request, default to current
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            year = date.today().year
            month = date.today().month
    else:
        year = date.today().year
        month = date.today().month
    
    # Validate month
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    
    # Get all entries for this user (for overall stats)
    all_entries = []
    if habit:
        all_entries = MoodEntry.objects.filter(habit=habit).order_by('-date')
    
    # Get entries for the current month
    month_entries = []
    if habit:
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        month_entries = MoodEntry.objects.filter(
            habit=habit,
            date__gte=first_day,
            date__lte=last_day
        ).order_by('date')
    
    # Calculate statistics (based on all entries)
    stats = {
        'total_entries': len(all_entries),
        'avg_mood': 0,
        'avg_sleep': 0,
        'yoga_count': 0,
    }
    
    if all_entries:
        stats['avg_mood'] = sum(e.mood for e in all_entries) / len(all_entries)
        stats['avg_sleep'] = sum(e.sleep_duration for e in all_entries) / len(all_entries)
        stats['yoga_count'] = sum(1 for e in all_entries if e.yoga)
    
    # Calculate previous and next month
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1
    
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    # Serialize entries to JSON for JavaScript
    entries_json = json.dumps([
        {
            'date': entry.date.strftime('%Y-%m-%d'),
            'mood': entry.mood,
            'sleep': entry.sleep_duration,
            'yoga': entry.yoga,
            'note': entry.note
        }
        for entry in all_entries
    ])
    
    month_entries_json = json.dumps([
        {
            'date': entry.date.strftime('%Y-%m-%d'),
            'mood': entry.mood,
            'sleep': entry.sleep_duration,
            'yoga': entry.yoga,
            'note': entry.note
        }
        for entry in month_entries
    ])
    
    # Create Django data for JavaScript
    django_data = {
        'currentYear': year,
        'currentMonth': month,
        'prevYear': prev_year,
        'prevMonth': prev_month,
        'nextYear': next_year,
        'nextMonth': next_month,
        'avgMood': round(stats['avg_mood'], 1) if stats['avg_mood'] else 0,
        'avgSleep': round(stats['avg_sleep'], 1) if stats['avg_sleep'] else 0,
        'yogaCount': stats['yoga_count'],
        'hasEntries': len(all_entries) > 0,
        'allEntries': [
            {
                'date': entry.date.strftime('%Y-%m-%d'),
                'mood': entry.mood,
                'sleep': entry.sleep_duration,
                'yoga': entry.yoga,
                'note': entry.note
            }
            for entry in all_entries
        ],
        'monthEntries': [
            {
                'date': entry.date.strftime('%Y-%m-%d'),
                'mood': entry.mood,
                'sleep': entry.sleep_duration,
                'yoga': entry.yoga,
                'note': entry.note
            }
            for entry in month_entries
        ]
    }
    
    context = {
        'entries': all_entries,
        'month_entries': month_entries,
        'entries_json': entries_json,
        'month_entries_json': month_entries_json,
        'django_data_json': django_data,
        'username': request.user.first_name or request.user.username,
        'stats': stats,
        'current_year': year,
        'current_month': month,
        'current_month_name': calendar.month_name[month],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    
    return render(request, 'habits/history.html', context)

@login_required
def all_entries(request):
    """View all mood entries with search and filter"""
    # Get the user's Daily Mood habit
    try:
        habit = Action.objects.get(user=request.user, name="Daily Mood")
        entries = MoodEntry.objects.filter(habit=habit).order_by('-date')
    except Action.DoesNotExist:
        entries = []
    
    context = {
        'entries': entries,
        'username': request.user.first_name or request.user.username,
    }
    
    return render(request, 'habits/entries.html', context)

@login_required
def delete_entry(request, entry_id):
    """Delete a mood entry"""
    if request.method == 'POST':
        try:
            entry = MoodEntry.objects.get(id=entry_id, habit__user=request.user)
            entry.delete()
            messages.success(request, 'Entry deleted successfully!')
        except MoodEntry.DoesNotExist:
            messages.error(request, 'Entry not found!')
    
    return redirect('all_entries')


@login_required
def edit_entry(request, entry_id):
    """Edit an existing mood entry"""
    entry = get_object_or_404(MoodEntry, id=entry_id, habit__user=request.user)
    
    if request.method == 'POST':
        mood = request.POST.get('mood')
        sleep_duration = request.POST.get('sleep_duration')
        yoga = request.POST.get('yoga')
        note = request.POST.get('note', '')
        
        if mood and sleep_duration and yoga:
            entry.mood = int(mood)
            entry.sleep_duration = int(sleep_duration)
            entry.yoga = True if yoga == 'yes' else False
            entry.note = note
            entry.save()
            
            messages.success(request, '✨ Entry updated successfully!')
            return redirect('all_entries')
    
    context = {
        'entry': entry,
        'username': request.user.first_name or request.user.username,
        'editing': True,
        'today': entry.date,
        'today_entry': entry,
    }
    
    return render(request, 'index.html', context)


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('habits_tracker')
    
    # Check if this is the first user (first time app usage)
    is_first_user = not User.objects.exists()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(first_name)
        
        # Validation
        if not all([username, first_name, password1, password2]):
            messages.error(request, 'Please fill in all required fields!')
            context = {'is_first_user': is_first_user}
            return render(request, 'habits/signup.html', context)
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            context = {'is_first_user': is_first_user}
            return render(request, 'habits/signup.html', context)
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            context = {'is_first_user': is_first_user}
            return render(request, 'habits/signup.html', context)
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password1
            )
            
            # Set first name explicitly
            user.first_name = first_name
            user.save()
            
            # Log the user in
            login(request, user)
            if is_first_user:
                messages.success(request, f'Welcome to Do Your Best, {first_name}! 🎉 Let\'s start your wellness journey!')
            else:
                messages.success(request, f'Welcome {first_name}! 🎉')
            return redirect('habits_tracker')
            
        except IntegrityError:
            messages.error(request, 'Username already exists!')
            context = {'is_first_user': is_first_user}
            return render(request, 'habits/signup.html', context)
    
    context = {
        'is_first_user': is_first_user
    }
    return render(request, 'habits/signup.html', context)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('habits_tracker')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            name = user.first_name or user.username
            messages.success(request, f'Welcome back {name}! 👋')
            
            # Redirect to next page or habits tracker
            next_page = request.GET.get('next', 'habits_tracker')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'habits/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You\'ve been logged out. See you soon! 👋')
    return redirect('login_view')

