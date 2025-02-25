from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django import forms
from django.contrib import messages
from django.http import *
from .models import ExerciseLog, Exercise

def home(request):
    if not request.user.is_authenticated:
        return redirect('app:login')
    else:
        context = {
            'exercise_logs' : ExerciseLog.objects.filter(user=request.user.id).order_by('-date', '-id'),
            'exercises' : Exercise.objects.all(),
            'title' : 'Exercise Log',
            'user_id' : request.user.id,
        }

        if not context['exercise_logs'].count():
            return render(request,'Exercise_tracker/get_started.html')

        return render(request, 'Exercise_tracker/home.html', context)

# Add Exercise to database, creating a ExerciseLog if necessary, stays on Exercise recommender page
def add_from_recommender(request, exercise_name):

    today_log = None
    # Incase there has not been a workout log created for the current day
    try:
        
        exlog_count = ExerciseLog.objects.filter(user=request.user.id, date=datetime.date.today()).count()
        
        if exlog_count == 0:
        # Create a new exercise log for today for the current user
            today_log = ExerciseLog.objects.create(
                user=request.user,
                date=datetime.date.today(),
            )
        
        # There already is an existing exercise log for the current day
        else:
            today_log = ExerciseLog.objects.filter(user=request.user.id, date=datetime.date.today())[exlog_count-1]

    except Exception as e:
        print('ERROR', e)

    # Create the exercise
    Exercise.objects.create(
        exercise_log=today_log,
        exercise_name= exercise_name,
        num_sets=0,
        num_reps=0,
        exercise_weight=0,
    )

    # Stays on Exercises list page in case user wants to add more exercises to today's exercise log
    messages.success(request, "Exercise successfully added to today's workout log!!", extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ExlogDetailView(DetailView):
    model = ExerciseLog
    context_object_name = "exlog"

    # Getting extra context for the class-based view
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)        
        
        # The line below literally took me hours to figure out
        context['exercises'] = Exercise.objects.filter(exercise_log=self.object).iterator()
        return context

class DateInput(forms.DateInput):
    input_type = 'date'

class ExlogCreateView(LoginRequiredMixin, CreateView):
    model = ExerciseLog
    fields = ['date']

    def get_form(self):
        form = super(ExlogCreateView, self).get_form()
        initial_base = self.get_initial() 
        initial_base['date'] = timezone.now()
        form.initial = initial_base
        form.fields['date'].widget = DateInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Workout Log successfully added!", extra_tags='success')
        return super().form_valid(form)

# Class based view for Update
class ExlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExerciseLog
    fields = ['date']

    def get_form(self):
        form = super(ExlogUpdateView, self).get_form()
        initial_base = self.get_initial() 
        initial_base['date'] = timezone.now()
        form.initial = initial_base
        form.fields['date'].widget = DateInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Workout Log successfully updated!", extra_tags='success')
        return super().form_valid(form)

    # Test to see if current logged in user is the creator of the workout log
    def test_func(self):
        exlog = self.get_object()
        if self.request.user == exlog.user:
            return True
        return False

class ExlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ExerciseLog
    context_object_name = "exlog"
    success_url = '/exlog/'   
    def test_func(self):
        exlog = self.get_object()
        if self.request.user == exlog.user:

            if self.request.method == 'POST':
                messages.success(self.request, "Workout Log successfully removed!", extra_tags='success')
            return True
        return False

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    fields = ['exercise_name', 'num_sets', 'num_reps', 'exercise_weight']

    def form_valid(self, form):
        form.instance.exercise_log = ExerciseLog.objects.get(id=self.kwargs['pk'])
        messages.success(self.request, "Exercise successfully added!", extra_tags='success')
        return super().form_valid(form)


class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercise
    fields = ['num_sets', 'num_reps', 'exercise_weight']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Exercise successfully updated!", extra_tags='success')
        return super().form_valid(form)

    def test_func(self):
        exlog = self.get_object()
        if self.request.user == exlog.exercise_log.user:
            return True
        return False


class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Exercise
    
    def test_func(self):
        exlog = self.get_object()
        if self.request.user == exlog.exercise_log.user:
            if self.request.method == 'POST':
                success_url = "/app/"
                messages.success(self.request, "Exercise successfully removed!", extra_tags='success')
            return True
        return False
    
    def get_success_url(self):
        return '/exlog/log/' + str(self.get_object().exercise_log.id)