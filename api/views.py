from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ExperimentSerializer, ParticipantSeriaizer, ParticpantExperimentSerializer, ResearcherSeializer
from .models import Experiment, Participant, ParticipantExperiment, Researcher
from rest_framework.decorators import api_view
from django.db import connection



### working off experiment participant table


### method to edit
### can only add end date to researcher and experiment
### can edit participant to change their preferences for email list and data collection

@api_view(['PUT'])

def edit_researcher(request, id):

    try:

        #researcher =  Researcher.objects.get(id = request.data['id'])
        researcher =  Researcher.objects.get(id = id)

        ## just hope it works here
        researcher.end_date = request.data['end_date']

        researcher.save()

    except:
        return Response(status=status.HTTP_304_NOT_MODIFIED)

    return Response(status=status.HTTP_200_OK)



@api_view(['PUT'])
def edit_experiment(request, id):

    try:

        #experiment = Experiment.objects.get(id = request.data['id'])
        experiment = Experiment.objects.get(id = id)

        ## just hope it works here

        experiment.end_date = request.data['end_date']

        experiment.save()

    except:

        return Response(status=status.HTTP_304_NOT_MODIFIED)

    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])

def edit_participant(request, id):

    try:

        #participant = Participant.objects.get(id = request.data['id'])
        participant = Participant.objects.get(id = id)

        ## try getting email list choice
        try:

            email_collection = request.data['email_list']

        except KeyError:
            email_collection = participant.email_list

        participant.email_list = email_collection

        ## try getting 
        try: 

            data_collection = request.data['collect_data']

        except KeyError:
            data_collection = participant.collect_data

        participant.collect_data = data_collection

        participant.save()

    except:

        return Response(status=status.HTTP_304_NOT_MODIFIED)
    
    return Response(status=status.HTTP_200_OK)


### end of methods to edit

### methods to get everything
@api_view(['GET'])
def get_particiapnts(request):

    results = Participant.objects.raw("SELECT * FROM participants")

    serializer = ParticipantSeriaizer(results, many = True)

    return Response(serializer.data)


@api_view(['GET'])
def get_experiments(request):

    results = Experiment.objects.raw("SELECT * FROM experiments")

    serializer = ExperimentSerializer(results, many = True)

    return Response(serializer.data)


@api_view(['GET'])
def get_researchers(request):

    results = Researcher.objects.raw("SELECT * FROM researchers")

    serializer = ResearcherSeializer(results, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def get_participant_experiment(request):

    results = ParticipantExperiment.objects.raw("SELECT * FROM participant_experiment")

    serializer = ParticpantExperimentSerializer(results, many = True)

    return Response(serializer.data)
### end of methods to get everything


### method to delete, can only delete participantion in experiment. 

@api_view(['DELETE'])
def delete_experiment_participation(request, id):

    ### get the experiment and participant  

    #id = request.data['id']

    with connection.cursor() as cursor:

        #try:
        #result = cursor.execute("SELECT * FROM participant_experiment WHERE id = %s", [id])
        #if result.fetchall():
            print(f'delete id {id}')
            cursor.execute("DELETE FROM participant_experiment WHERE id = %s", [id])

        #else:
        #except:
            #return Response(status=status.HTTP_404_NOT_FOUND)
        
    return Response(status=status.HTTP_200_OK)

## end of method to delete  


## methods to add new events


# add participant
@api_view(['POST'])
def add_participant(request):

    print('add participant called')

    serializer = ParticipantSeriaizer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# add experiment
@api_view(['POST'])
def add_experiment(request):

    serializer = ExperimentSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# add researcher
@api_view(['POST'])
def add_researcher(request):

    serializer = ResearcherSeializer(data = request.data)


    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# adds a participation in experiment

@api_view(['POST'])
def add_participation(request):

    ## get participant_id and experiment_id, assume they exist
    experiment_id = request.data['experiment_id']
    participant_id = request.data['participant_id']


    ## attempt to get participant and experiment and create them if they exist
    experiment = Experiment.objects.get(id = experiment_id)
    participant = Participant.objects.get(id = participant_id)

    ## 

    serializer = ParticpantExperimentSerializer(data = request.data)


    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## end of methods to add to events



### start of report generation

## report for experiment_participant

'''
can filter by the following

1. experiment (say a list of all participants for this experiment) + data collection (say participant who agree to have data collected)
2. participant  (say list all the experiments what a particular person has participated in) + data collection  (say participant who agree to have data collected)


'''


@api_view(['GET'])
def filter_experiment(request, id, data_collection = None):

    if data_collection == 'True' or data_collection == 'true':
        data_collection = True
        
    elif data_collection == 'False' or data_collection == 'false':
        data_collection = False

    #experiment_id = request.data['experiment_id']
    experiment_id = id

    if data_collection:

        results = ParticipantExperiment.objects.filter(experiment_id = experiment_id).filter(data_collection = data_collection)

        #results = ParticipantExperiment.objects.raw()
    
    else:
        results = ParticipantExperiment.objects.filter(experiment_id = experiment_id)

    
    serializer = ParticpantExperimentSerializer(results, many = True)

    return Response(serializer.data)



@api_view(['GET'])
def filter_participant(request, id, data_collection = None):

    if data_collection == 'True' or data_collection == 'true':
        data_collection = True
        
    elif data_collection == 'False' or data_collection == 'false':
        data_collection = False

    #participant_id = request.data['participant_id']
    participant_id = id

    if data_collection:

        results = ParticipantExperiment.objects.filter(participant_id = participant_id).filter(data_collection = data_collection)

    else:

        results = ParticipantExperiment.objects.filter(participant_id)

        
    serializer = ParticpantExperimentSerializer(results, many = True)

    return Response(serializer.data)

### end of report generation