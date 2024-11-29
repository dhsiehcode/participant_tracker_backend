from django.urls import path
from . import views

urlpatterns = [
    ## getting add models of said type
    path('researchers/', views.get_researchers),
    path('experiments/', views.get_experiments),
    path('participants/', views.get_particiapnts),
    path('participant_experiment/', views.get_participant_experiment),

    ## deleting 
    path('participant_experiment/<int:id>', views.delete_experiment_participation), 


    ## methods to edit researcher/experiments/participants/participation
    path('researcher/<int:id>', views.edit_researcher),
    path('experiment/<int:id>', views.edit_experiment),
    path('participant/<int:id>', views.edit_participant),
    path('participation/<int:id>', views.edit_participation),

    ## creating researcher/experiment/participant/expriment participation
    path('researcher/', views.add_researcher),
    path('experiment/', views.add_experiment),
    path('participant/', views.add_participant),
    path('participation/', views.add_participation),

    path('filter_by_date_researcher/', views.get_experiments_with_date_and_researcher),
    path('get_report/', views.get_report)
]