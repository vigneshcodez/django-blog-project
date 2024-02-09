from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('registerpage', views.registerpage, name='registerpage'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('logoutpage', views.logoutpage, name='logoutpage'),
    path('topicspage/', views.topicspage, name='topicspage'),
    path('topicspage/<str:name>', views.topicarticlepage, name='topicarticlepage'),
    path('topicspage/<str:cname>/<str:aname>',
         views.detailedview, name='detailedview'),
    path('fav', views.fav, name='fav'),
    path('savedpage', views.savedpage, name='savedpage'),
    path('remove_favourite/<str:fid>',
         views.remove_favourite, name='remove_favourite'),

]
