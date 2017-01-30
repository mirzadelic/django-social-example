from django.conf.urls import url, include
from rest_framework import viewsets, serializers, routers
from models import Person


class PersonSerializer(serializers.ModelSerializer):
    """ Serializer for Person model. """
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Person
        fields = (
            'id', 'firstName', 'surname', 'full_name', 'age', 'gender',
            'friends', 'friends_of_friends', 'suggested_friends'
        )


class PersonViewSet(viewsets.ModelViewSet):
    """ API view for Person model. """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        queryset = super(PersonViewSet, self).get_queryset()
        name = self.request.query_params.get('firstName', None)
        if name is not None:
            queryset = queryset.filter(firstName__contains=name)
        return queryset


router = routers.DefaultRouter()
router.register(r'person', PersonViewSet)


urlpatterns = [
    url('^', include(router.urls)),
]
