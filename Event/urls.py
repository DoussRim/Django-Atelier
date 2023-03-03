from django.urls import path
# from . import views
from.views import *
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('index/',index),
    path('affiche/<str:classe>',affiche),
    path('AfficheEvt/',ListEvt),
    # path('List/',ListEvtGeneric.as_view(),template_name="")
    path('List/',ListEvtGeneric.as_view(),name="Aff"),
    path('Detail/<str:title>',Detail,name='D'),
    path('Ajout/',AjoutEvt,name="Add"),
    path('AjoutGen/',Ajout.as_view()),
    path('DetailGen/<int:pk>',DetailGeneric.as_view(),name="DD"),
    path('login/',LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',LogoutView.as_view())
]
