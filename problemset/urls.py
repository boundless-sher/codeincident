from django.urls import path
from . import views

urlpatterns = [
  path('', views.display_problem, name='display-problem'),
  path('finished/', views.finished_problemset, name='finished-problemset'),
  path('upsolve/problems/', views.upsolve_problems_list, name='upsolve-problems'),
  path('upsolve/problems/<str:pk>/', views.upsolve_problem, name='upsolve-problem'),

]