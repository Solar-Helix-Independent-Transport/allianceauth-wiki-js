from django.conf.urls import url, include

from . import views

app_name = 'wikijs'

module_urls = [
    url(r'^activate/$', views.activate_wikijs, name='activate'),
    url(r'^deactivate/$', views.deactivate_wikijs, name='deactivate'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^set_password/$', views.set_password, name='set_password'),

]

urlpatterns = [
    url(r'^wikijs/', include((module_urls, app_name), namespace=app_name))
]
