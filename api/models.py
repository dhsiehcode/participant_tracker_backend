from django.db import models

# Create your models here.

class Participant(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField("date of birth")
    sex = models.CharField(max_length=10) ## expects lowercase from frontend
    occupation = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    email_list = models.BooleanField(default=False, verbose_name="agreed to be on email list")
    collect_data = models.BooleanField(default=False, verbose_name="agreed to have data for all experiment collected")

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        db_table = 'participants'




class Researcher(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    start_date = models.DateField("day this researcher started at the lab")
    end_date = models.DateField("day this researcher ended at the lab", null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        db_table = 'researchers'


class Experiment(models.Model):

    name = models.CharField(verbose_name="name of experiment", max_length=50)
    description = models.TextField(verbose_name="description of experiment")
    start_date = models.DateField(verbose_name="the first day the experiment is run")
    end_date = models.DateField(verbose_name="the last day the experiment is run", null=True)
    irb_number = models.CharField("irb protocol number", max_length=50)
    experimenter = models.ForeignKey(Researcher, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'experiments'

class ParticipantExperiment(models.Model):

    participant_id = models.ForeignKey(Participant, on_delete=models.PROTECT)
    experiment_id = models.ForeignKey(Experiment, on_delete=models.PROTECT)

    collect_data = models.BooleanField("if we can collect data for this participant in this experiment", null=True)
    experiment_date = models.DateField("date experiment with this participant is conducted")
    location = models.CharField(max_length=20)

    def __str__(self):
        return str(self.participant_id) + " " + str(self.experiment_id)



    ## since django doesn't allow multiple columns as primary key,
    ## I kept the auto ID and enforce unique constrain on 
    ## participant_id and experiment_id
    class Meta: 
        db_table = 'participant_experiment'
        constraints = [
            models.UniqueConstraint(fields=['participant_id', 'experiment_id'], name='unique experiment participant')
        ]