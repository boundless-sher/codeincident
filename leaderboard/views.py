from django.shortcuts import render
from .models import Leaderboard

# Create your views here.
def leaderboard_view(request):
    leaderboard = Leaderboard.objects.all()
    context = {
        'leaderboard': leaderboard
    }
    return render(request, 'leaderboard/leaderboard.html', context=context)