from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    """ Person model """
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    firstName = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=gender_choices)
    friends = models.ManyToManyField(
        'self', symmetrical=True, blank=True)

    @property
    def full_name(self):
        """ Property for generating full_name """
        return '%s %s' % (self.firstName, self.surname)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

    @property
    def friends_of_friends(self):
        """ Property for list of friends of friends """
        persons = Person.objects.filter(pk__in=self.friends.all()).values_list(
            'friends', flat=True).distinct()
        return persons

    @property
    def suggested_friends(self):
        """ Property for list of suggested friends """
        exclude_pks = list(self.friends.all().values_list('pk', flat=True))
        exclude_pks.append(self.pk)

        suggested_friends = []
        for person in Person.objects.exclude(pk__in=exclude_pks):
            if person.friends.filter(pk__in=exclude_pks).count() >= 2:
                suggested_friends.append(person.pk)
        return suggested_friends
