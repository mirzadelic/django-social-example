from django.conf.urls import url

from views import HomePageView, load_data


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home-page'),
    url(r'^load_data/$', load_data, name='load-data'),
]
