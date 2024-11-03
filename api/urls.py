from django.urls import path
from . import views

urlpatterns = [
    ## getting add models of said type
    path('researchers/', views.get_researchers),
    path('experiments/', views.get_experiments),
    path('participants/', views.get_particiapnts),
    path('participant_experiment/', views.get_participant_experiment),

    ## deleting 
    path('participant_experiment/<int:id>/', views.delete_experiment_participation), 


    ## methods to edit researcher/experiments/participants
    path('researcher/<int:id>', views.edit_researcher),
    path('experiment/<int:id>', views.edit_experiment),
    path('participant/<int:id>', views.edit_participant),

    ## creating researcher/experiment/participant/expriment participation
    path('researcher/', views.add_researcher),
    path('experiment/', views.add_experiment),
    path('participant/', views.add_participant),
    path('participation/', views.add_participation),


    ## gets reports
    path('filter_experiment/<int:id>/<data_collection>/', views.filter_experiment),
    path('filter_experiment/<int:id>/', views.filter_experiment),
    path('filter_participant/<int:id>/<data_collection>/', views.filter_participant),
    path('filter_participant/<int:id>/', views.filter_participant)
]