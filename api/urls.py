from django.urls import path
from rest_framework import routers 
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name ='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('admin', views.AdminViewAnalysis.as_view(), name='admin'),
    #path('', views.AnalusisView.as_view(), name= 'home'),
    path('analisis', views.StayView.as_view(method = 'getAllStays'), name = 'analisis'),
    path('analisis/<int:id>', views.StayView.as_view(method = 'getStay')),
    # path('stay_info', views.),
    path('review'), views.ReviewView.as_view(method='get_reviews_data'),
    #path('analisis/<int:id>', views.AnalsysisView.as_view(), name = 'analysis_id'),
    #path('comparar', views.CompareView.as_view(), name = 'compare')
    #path('comparar/<int:id1>+<int:id2>,')
]