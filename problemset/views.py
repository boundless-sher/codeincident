from django.shortcuts import render, redirect
from .models import Problem, UserProblem
from leaderboard.models import Leaderboard
from django import forms 


class UserSubmitForm(forms.Form):
    user_output = forms.CharField(widget=forms.Textarea)


def create_or_get_session(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
        request.session['completed'] = False
    return request.session.session_key

# Create your views here.
def display_problem(request):
    if(request.session.get('handle') == None):
        request.session['handle'] = 'anonymous user'

    if(request.session.get('completed') == True):
        return redirect('upsolve-problems')

    if(request.method == 'POST'):
        form = UserSubmitForm(request.POST)
        if form.is_valid():
            user = create_or_get_session(request)
            user_problem = UserProblem.objects.get(id=request.session["current_problem"])
            user_problem.user_output = form.cleaned_data['user_output']
            user_problem.is_correct = user_problem.user_output == user_problem.problem.correct_output
            user_problem.save()
            return redirect('display-problem')

    problems = Problem.objects.all()
    user = create_or_get_session(request)
    current_user_problem = None
    for problem in problems:
        user_problem = UserProblem.objects.filter(user=user, problem=problem)
        if not user_problem:
            user_problem = UserProblem.objects.create(user=user, problem=problem)
        user_problem = UserProblem.objects.get(user=user, problem=problem) 
        if current_user_problem == None and user_problem.user_output == None:
            current_user_problem = user_problem
            
    if(current_user_problem == None):
        request.session['completed'] = True
        return redirect("finished-problemset")

    form = UserSubmitForm()
    context = {
        'current_problem': current_user_problem,
        'form': form,
    }
    print("current problem", current_user_problem.id)
    request.session["current_problem"] = current_user_problem.id
    return render(request, 'problemset/display_problem.html', context=context)

def finished_problemset(request):
    correct_solutions = UserProblem.objects.filter(user=create_or_get_session(request), is_correct=True).count()
    context = {
        'correct_solutions': correct_solutions,
        'total_problems': Problem.objects.count(),
    }
    request.session['correct_solutions'] = correct_solutions
    new_user = Leaderboard.objects.create(handle=request.session['handle'], score=correct_solutions)
    print(new_user)
    return render(request, 'problemset/finished_problemset.html', context=context)

def upsolve_problems_list(request):
    print(request.session.get('completed'), 'here')
    if(request.session.get('completed')) == None:
        print('here')
        return redirect('display-problem')
    problems = Problem.objects.all()
    context = {
        'problems': problems,
    }
    return render(request, 'problemset/upsolve_problems_list.html', context=context)

def upsolve_problem(request, pk):
    print('here')
    problem = Problem.objects.get(id=pk)
    user = create_or_get_session(request)
    user_problem = UserProblem.objects.get(user=user, problem=problem)
    if(request.method == "POST"):
        print('post')
        form = UserSubmitForm(request.POST)
        if form.is_valid():
            user_problem.user_output = form.cleaned_data['user_output']
            user_problem.is_correct = user_problem.user_output == user_problem.problem.correct_output
            user_problem.save()
        
    

    form = UserSubmitForm()
    print('form')

    context = {
        'problem': problem,
        'user_problem': user_problem,
        'form': form,
    }
    return render(request, 'problemset/upsolve_problem.html', context=context)