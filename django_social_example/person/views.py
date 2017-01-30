from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import Person

import os


def load_data(request):
    """ Loading data from file and saving them to db. """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data.txt')
    file = open(file_path, 'r')
    Person.objects.all().delete()
    persons = []
    for line in file.read().splitlines():
        splitted = line.split(';')
        person_data = {
            'id': int(splitted[0]),
            'firstName': str(splitted[1]) if splitted[1] is not '' else None,
            'surname': str(splitted[2]) if splitted[2] is not '' else None,
            'age': int(splitted[3]) if splitted[3] is not '' else None,
            'gender': str(splitted[4])
        }
        person = Person(**person_data)
        persons.append(person)
    Person.objects.bulk_create(persons)

    file = open(file_path, 'r')
    for line in file.read().splitlines():
        splitted = line.split(';')
        friend_ids = []
        for fid in splitted[5].split(','):
            friend_ids.append(int(fid))

        person = Person.objects.get(pk=splitted[0])
        person.friends.add(*friend_ids)

    return HttpResponseRedirect(reverse('home-page'))


class HomePageView(TemplateView):
    """ Home view """
    template_name = 'index.html'
