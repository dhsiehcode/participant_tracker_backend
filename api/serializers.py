from rest_framework import serializers
from .models import Participant, Experiment, ParticipantExperiment, Resercher


class ParticipantSeriaizer(serializers.ModelSerializer):

    class Meta:

        model = Participant
        fields = ('id', 'first_name', 'last_name', 'dob', 'sex', 
                  'occupation', 'email', 'email_list', 'collect_data')


class ExperimentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Experiment
        fields = ('id', 'name', 'description', 'start_date',
                  'end_date', 'irb_number', 'experimenter')


class ParticpantExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantExperiment 
        fields = ('id', 'participant_id', 'experiment_id',
                  'collect_data', 'experiment_date', 'location')


class ResearcherSeializer(serializers.ModelSerializer):

    class Meta:
        model = Resercher
        fields = ('id', 'first_name', 'last_name', 'start_date', 'end_date')

