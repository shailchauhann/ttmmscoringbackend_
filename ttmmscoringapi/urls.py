from django.urls import path, include
from . import views
urlpatterns = [
    path('token', views.token),
    path('bidding', views.bidding),
    path('startups', views.startupsall),
    path('defaultbid', views.defaultbid),
    path('investors', views.investors),
    path('currentstartup', views.currentstartups),
    path('progress', views.progress),
    path('showprogress', views.showprogress),
    path('showinvestor', views.showinvestor),
]