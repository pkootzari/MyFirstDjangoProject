from django.urls import path
from . import views


app_name = 'company'
urlpatterns = [
    path('', views.homePage, name='login'),
    path('userpage/', views.userPage, name='userpage'),
    path('newuser/', views.newUser, name='newuser'),
    path('neworder/', views.newOrder, name='neworder'),
    path('newservice/', views.newService, name='newservice'),
    path('logout/', views.logout, name='logout'),
    path('newticket/', views.newTicket, name='newticket'),
    path('ticket/', views.ticketReview, name='ticketreview')
]
