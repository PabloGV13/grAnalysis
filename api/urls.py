from django.urls import path
from rest_framework import routers 
from . import views

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)


urlpatterns = [
    path('register', views.UserRegister.as_view(), name ='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('admin', views.AdminViewAnalysis.as_view(), name='admin'),

    
    #Rutas de usuario 
    path('users', views.getAllUsers, name = 'get-all-users'),  
    path('delete/user/<int:id>', views.deleteUser, name = 'delete-user'),
    
    #Rutas para StayView
    path('stays', views.getAllStays, name = 'get-all-stays'),
    path('stays/<int:id>', views.getStay,name = 'get-stay'),
    path('stays/map', views.getStaysMap, name = 'get-stay-map'),
    path('stays/post_request_stay', views.postRequestedStay, name = 'post-requested-stay'), 
    path('stays/get_request_stay', views.getRequestedStay, name = 'get-request-stay'),
    path('stays/post_stay_analysis/<int:id>', views.postStayAnalysis, name = 'get-request-stay'),
    
    #Rutas para ReviewView
    path('reviews/numbernights/<int:id>', views.get_review_numbernights, name='get-review-numbernights'),
    path('reviews/clienttype/<int:id>', views.get_review_client_type, name='get-review-clienttype'),
    path('reviews/latest/<int:id>', views.get_latest_review, name='get-latest-review'),
    path('reviews/oldest/<int:id>', views.get_oldest_review, name='get-oldest-review'),
    path('reviews/mostpositive/<int:id>', views.get_mostPostive_review, name='get-mostpositive-review'),
    path('reviews/mostnegative/<int:id>', views.get_mostNegative_review, name='get-mostnegative-review'),

    #Rutas para KeywordView
    path('keywords/toppolarity/<int:id>', views.getTopPolarityKeyWords, name='get-toppolarity-keywords'),
    path('keywords/lowestpolarity/<int:id>', views.getLowestPolarityKeywords, name='get-lowestpolarity-keywords'),
    path('keywords/bagofwords/<int:id>', views.getBagOfWords, name='get-bagofwords'),
    
    # path('stay_info', views.),
    #path('review', views.ReviewView.as_view(method='get_reviews_data'), name = 'review'),
    #path('analisis/<int:id>', views.AnalsysisView.as_view(), name = 'analysis_id'),
    #path('comparar', views.CompareView.as_view(), name = 'compare')
    #path('comparar/<int:id1>+<int:id2>,')

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]