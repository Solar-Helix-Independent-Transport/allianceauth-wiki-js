from django.urls import include, path

from . import views

app_name = 'wikijs'

module_urls = [
    path('activate/', views.activate_wikijs, name='activate'),
    path('deactivate/', views.deactivate_wikijs, name='deactivate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('set_password/', views.set_password, name='set_password'),

]

urlpatterns = [
    path('wikijs/', include((module_urls, app_name), namespace=app_name))
]
