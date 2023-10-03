from django.urls import path
from rest_framework import routers 
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name ='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('admin', views.AdminViewAnalysis.as_view(), name='admin'),

    
    #Ruta de usuario
    path('usuario', views.example_view, name='usuario'),    
    
    #Rutas para StayView
    path('stays', views.getAllStays, name = 'get-all-stays'),
    path('stays/<int:id>', views.getStay,name = 'get-stay'),
    
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
]