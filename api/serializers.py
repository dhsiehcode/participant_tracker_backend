from rest_framework import serializers
from .models import Participant, Experiment, ParticipantExperiment, Researcher






class ParticipantSerializer(serializers.ModelSerializer):

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
        model = Researcher
        fields = ('id', 'first_name', 'last_name', 'start_date', 'end_date')


class DataCollectionCountField(serializers.RelatedField):

    def to_representation(self, data_collection_count):
        return '%d' % data_collection_count


class ContactCountField(serializers.RelatedField):

    def to_representation(self, contact_count):
        return '%d' % contact_count


class NamedParticipantExperimentSerializer(serializers.ModelSerializer):

    participant_id = ParticipantSerializer()
    experiment_id = ExperimentSerializer()

    class Meta:
        model = ParticipantExperiment
        fields = ('id', 'participant_id', 'experiment_id', 'collect_data', 'experiment_date', 'location')
        #fields = ('id', 'participant_id', 'experiment_id', 'collect_data', 'experiment_date', 'location', 'participant', 'experiment')



        





