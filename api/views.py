from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ExperimentSerializer, ParticipantSerializer, ParticpantExperimentSerializer, ResearcherSeializer, NamedParticipantExperimentSerializer
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

@api_view(['PUT'])
def edit_participation(request, id):

    try:

        participation = ParticipantExperiment.objects.get(id = id)

        '''
        try:
            collect_data = request.data['collect_data']
        except KeyError:
            collect_data = participation.collect_data

        try:
            experiment_date = request.data['experiment_date']
        except KeyError:
            experiment_date = participation.experiment_date

        try:
            location = request.data['location']
        except KeyError:
            location = participation.location
        '''
        
        collect_data = request.data['collect_data']
        experiment_date = request.data['experiment_date']
        location = request.data['location']

        if not collect_data == '':
            participation.collect_data = collect_data

        if not experiment_date == '':
            participation.experiment_date = experiment_date

        if not location == '':
            participation.location = location

        participation.save()

    except:
        return Response(status=status.HTTP_304_NOT_MODIFIED)
    return Response(status=status.HTTP_200_OK)



### end of methods to edit

### methods to get everything
@api_view(['GET'])
def get_particiapnts(request):

    results = Participant.objects.raw("SELECT * FROM participants")

    serializer = ParticipantSerializer(results, many = True)

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

    serializer = ParticipantSerializer(data = request.data)

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
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## end of methods to add to events



### start of report generation

## report for experiment_participant

'''

Steps to generate report:

1. user can select date range that experiment took place and/or name of researcher conducting the experiment
2. the UI will display a list of experiments.
3. the user can select an experiment
3. the user will be shown participants in this experiment with
 # participants and # particiapnt who agreed to data collection and to be contacted

'''

@api_view(['POST'])
def get_experiments_with_date_and_researcher(request):

    start_date = request.data['start_date']
    end_date = request.data['end_date']
    researcher_id = request.data['researcher_id']


    has_researcher = (researcher_id == "")

    #print('id: ' + str(has_researcher))
    #has_researcher = (researcher_id == "10")

    #print('id: ' + str(has_researcher))


    if not has_researcher:

        print('has researcher')

        result_null = Experiment.objects.filter(end_date__isnull = True, start_date__gte=start_date, experimenter=researcher_id)


        result_no_null = Experiment.objects.filter(end_date__isnull = False, end_date__lte=end_date, 
                                                start_date__gte=start_date, experimenter=researcher_id)

        results = result_null | result_no_null
    
    else:

        print('no researcher')

        result_null = Experiment.objects.filter(end_date__isnull = True, start_date__gte=start_date)


        result_no_null = Experiment.objects.filter(end_date__isnull = False, end_date__lte=end_date, 
                                                start_date__gte=start_date)

        results = result_null | result_no_null

    ### return the experiments
    serializer = ExperimentSerializer(results, many = True)

    return Response(serializer.data)


@api_view(['POST'])
def get_report(request):

    ## particpant data
    experiment_id = request.data['experiment_id']
    participant_ids = ParticipantExperiment.objects.filter(experiment_id_id = experiment_id) ## all the participants, need names too
    serializer = NamedParticipantExperimentSerializer(participant_ids, many = True)


    ### get data_collection_statistic
    data_collection_true = Participant.objects.filter(id__in = participant_ids).filter(collect_data = True)
    ### get email_list_statistic
    email_list_true = Participant.objects.filter(id__in = participant_ids).filter(email_list = True)
    ### both email list and data collection is true
    data_and_email_true = Participant.objects.filter(id__in = participant_ids).filter(collect_data = True, email_list = True)
    ### get male and female participants statistic

    ids = []

    for p in participant_ids:
        ids.append(p.participant_id_id)


    males = Participant.objects.filter(id__in = ids).filter(sex = 'male')
    females = Participant.objects.filter(id__in = ids).filter(sex = 'female')

    '''
    males = []
    females = []

    with connection.cursor() as cursor:

            males = cursor.execute("SELECT * FROM participants WHERE sex = %s", ['male'])
            females = cursor.execute("SELECT * FROM participants WHERE sex = %s", ['female'])

            print(males.fetchone())
            print(females.fetchone())

            males = males.fetchall()
            females = females.fetchall()

            test =cursor.execute("SELECT DISTINCT(sex) FROM participants")

            print(test.fetchall())

            print(males)
            print(females)
    '''
    male_count = len(males)
    female_count = len(females)
    


    ## adding to response
    #augmented_serializer_data = list(serializer.data)

    augmented_serializer_data = {'participants': list(serializer.data)}

    augmented_serializer_data['statistics'] = ({'data_collection_count': len(data_collection_true), 'email_list_count': len(email_list_true),
                                      'data_and_email_count': len(data_and_email_true), 'male_count': male_count, 'female_count': female_count})



    return Response(augmented_serializer_data)





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

    with connection.cursor() as cursor:


        if data_collection:

            participant_ids = cursor.execute("SELECT participant_id_id FROM participant_experiment WHERE experiment_id_id = %s AND data_collection = %s", [experiment_id, data_collection])


            participant_ids = participant_ids.fetchall()

            participant_ids_list = []

            for tup in participant_ids:
                participant_ids_list.append(tup[0])

            results = Participant.objects.filter(id__in = participant_ids_list)
        else:


            participant_ids = cursor.execute("SELECT participant_id_id FROM participant_experiment WHERE experiment_id_id = %s", [experiment_id])

            participant_ids = participant_ids.fetchall()

            participant_ids_list = []

            for tup in participant_ids:
                participant_ids_list.append(tup[0])

            results = Participant.objects.filter(id__in = participant_ids_list)

        serializer = ParticipantSerializer(results, many = True)

        print(serializer.data)

        return Response(serializer.data)



@api_view(['GET'])
def filter_participant(request, id, data_collection = None):

    if data_collection == 'True' or data_collection == 'true':
        data_collection = True
        
    elif data_collection == 'False' or data_collection == 'false':
        data_collection = False

    #participant_id = request.data['participant_id']
    participant_id = id

    with connection.cursor() as cursor:


        if data_collection:

            experiment_ids = cursor.execute("SELECT experiment_id_id FROM participant_experiment WHERE participant_id_id = %s AND data_collection = %s", [participant_id, data_collection])


            experiment_ids = experiment_ids.fetchall()

            experiment_ids_list = []

            for tup in experiment_ids:
                experiment_ids_list.append(tup[0])

            results = Experiment.objects.filter(id__in = experiment_ids_list)
        else:


            experiment_ids = cursor.execute("SELECT experiment_id_id FROM participant_experiment WHERE participant_id_id = %s", [participant_id])

            experiment_ids = experiment_ids.fetchall()

            experiment_ids_list = []

            for tup in experiment_ids:
                experiment_ids_list.append(tup[0])

            results = Experiment.objects.filter(id__in = experiment_ids_list)

        serializer = ExperimentSerializer(results, many = True)

        print(serializer.data)

        return Response(serializer.data)

### end of report generation