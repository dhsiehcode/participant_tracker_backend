from django.db import models

# Create your models here.

class Participant(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField("date of birth")
    sex = models.CharField(max_length=10)
    occupation = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    email_list = models.BooleanField(default=False, verbose_name="agreed to be on email list")
    collect_data = models.BooleanField(default=False, verbose_name="agreed to have data for all experiment collected")




class Resercher(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    start_date = models.DateField("day this researcher started at the lab")
    end_date = models.DateField("day this researcher ended at the lab")


class Experiment(models.Model):

    name = models.CharField(verbose_name="name of experiment", max_length=50)
    description = models.CharField(verbose_name="description of experiment", max_length=200)
    start_date = models.DateField(verbose_name="the first day the experiment is run")
    end_date = models.DateField(verbose_name="the last day the experiment is run")
    irb_number = models.CharField("irb protocol number", max_length=50)
    experimenter = models.ForeignKey(Resercher, null=True, on_delete=models.SET_NULL)

class ParticipantExperiment(models.Model):

    participant_id = models.ForeignKey(Participant, on_delete=models.PROTECT)
    experiment_id = models.ForeignKey(Experiment, on_delete=models.PROTECT)

    collect_data = models.BooleanField("if we can collect data for this participant in this experiment", null=True)
    experiment_date = models.DateField("date experiment with this participant is conducted")
    location = models.CharField(max_length=20)



    ## since django doesn't allow multiple columns as primary key,
    ## I kept the auto ID and enforce unique constrain on 
    ## participant_id and experiment_id
    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['participant_id', 'experiment_id'], name='unique experiment participant')
        ]