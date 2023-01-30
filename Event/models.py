from django.db import models
from django.utils.timezone import datetime
from Person.models import Person
# Create your models here.
class Event(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    image=models.ImageField()
    category_choices=(
        ('Musique','M'),
        ('Cinema','C'),
        ('Sport','S'))
    category=models.CharField(max_length=8,choices=category_choices)
    state=models.BooleanField(default=False)
    nbe_participant=models.IntegerField(default=0)
    event_date=models.DateField()
    creation_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    organizer=models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        #on_delete=models.SET_NULL,
        #null=True
        #related_name="organisateur"             
    )
    participation=models.ManyToManyField(
        Person,
        related_name="participations",
        through="Event_Participation"
    )
    class Meta:
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    event_date__gte=datetime.now()),
                    name='Date doit être sup à date sys'
                )
        ]
class Event_Participation(models.Model):
     person=models.ForeignKey(Person,on_delete=models.CASCADE)
     event=models.ForeignKey(Event,on_delete=models.CASCADE)
     participation_date=models.DateField(auto_now=True)
     class Meta:
         unique_together=('person','event')