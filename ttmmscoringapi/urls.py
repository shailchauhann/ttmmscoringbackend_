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
    path('portal_control', views.portal_control),
    path('investor_fetch', views.investor_fetch),
    path('startup_fetch', views.startup_fetch),
    path('funding_fetch', views.funding_fetch),
    path('startup_funding', views.startup_funding),
    path('funding_post', views.funding_post),
    path('', views.index, name ='index'),
    path('<int:question_id>/', views.detail, name ='detail'),
    path('<int:question_id>/results/', views.results, name ='results'),
    path('<int:question_id>/vote/', views.vote, name ='vote'),




    
]