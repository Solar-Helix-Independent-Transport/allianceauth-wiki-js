from django.urls import re_path, include

from . import views

app_name = 'wikijs'

module_urls = [
    re_path(r'^activate/$', views.activate_wikijs, name='activate'),
    re_path(r'^deactivate/$', views.deactivate_wikijs, name='deactivate'),
    re_path(r'^reset_password/$', views.reset_password, name='reset_password'),
    re_path(r'^set_password/$', views.set_password, name='set_password'),

]

urlpatterns = [
    re_path(r'^wikijs/', include((module_urls, app_name), namespace=app_name))
]
