from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework import status, generics, permissions
from django.db.models import Max,Min,Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Stay, Review, Keyword,User
from .validations import custom_validation, validate_email, validate_password, validate_username
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, StaySerializer, ReviewSerializer, KeywordSerializer
from .tokens import create_jwt_pair_for_user
from .custom_views import CustomAPIView
from geopy.geocoders import Nominatim
from ratelimiter import RateLimiter
import folium


class UserRegister(CustomAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(CustomAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            tokens = create_jwt_pair_for_user(user)
            login(request, user)
            response = {"message": "Login Successfull", "is_admin": user.is_staff,"tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data = {"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
    


class UserLogout(CustomAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class UserView(CustomAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,BasicAuthentication)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
#Comprobacion de usuario actual#
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])  #DEBERIA DE SER: IsAuthenticated
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

    
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getAllStays(request): 
    stays = Stay.objects.all()
    serializer = StaySerializer(stays, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getStay(request, id):
    stay = get_object_or_404(Stay,stay_id=id)
    serializer = StaySerializer(stay)
    return Response(serializer.data, status=status.HTTP_200_OK)

# class ReviewView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)    

#Diccionario con el numero de noches(diagrama tarta)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_review_numbernights(request,id):
    dict = {}
    numbernights_list = Review.objects.filter(stay_id=id).values_list('number_nights',flat=True)
    for numbernight in numbernights_list:
        if numbernight in dict:
            dict[numbernight] += 1
        else:
            dict[numbernight] = 1

    n = numbernights_list.count()
    for key in dict:
        dict[key] = float((dict[key]*100)/n) 
    
    return Response(dict, status=status.HTTP_200_OK)


#Diccionario con el tipo de cliente (diagrama tarta)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_review_client_type(request,id):
    dict = {}
    client_type_list = Review.objects.filter(stay_id=id).values_list('client_type',flat=True)
    for client_type_ in client_type_list:
        if client_type_ in dict:
            dict[client_type_] += 1
        else:
            dict[client_type_] = 1

    n = client_type_list.count()
    for key in dict:
        dict[key] = float((dict[key]*100)/n) 
    
    return Response(dict, status=status.HTTP_200_OK)

@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_latest_review(request,id):
    latest_date = Review.objects.aggregate(latest_date=Max('date_review'))['latest_date']
    latest_review = Review.objects.filter(stay_id=id, date_review=latest_date).first()
    serializer = ReviewSerializer(latest_review)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_oldest_review(request,id):
    oldest_date = Review.objects.aggregate(oldest_date=Min('date_review'))['oldest_date']
    oldest_review = Review.objects.filter(stay_id=id, date_review=oldest_date).first()
    serializer = ReviewSerializer(oldest_review)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_mostPostive_review(request,id):
    positive_polarity = Review.objects.aggregate(positive_polarity=Max('polarity'))['positive_polarity']
    positive_review = Review.objects.filter(stay_id=id,polarity=positive_polarity).first()
    serializer = ReviewSerializer(positive_review)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_mostNegative_review(request,id):
    negative_polarity = Review.objects.aggregate(negative_polarity=Min('polarity'))['negative_polarity']
    negative_review = Review.objects.filter(stay_id=id,polarity=negative_polarity).first()
    serializer = ReviewSerializer(negative_review)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    

# class KeywordView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)    

# Palabras mas positivas
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getTopPolarityKeyWords(request,id):
    reviews = Review.objects.filter(stay_id = id)
    top_keywords = Keyword.objects.filter(id_review__in=reviews).order_by('-polarity')[:10]
    serializer = KeywordSerializer(top_keywords, many = True) 
    return Response(serializer.data, status=status.HTTP_200_OK)


#Palabras mas negativas
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getLowestPolarityKeywords(request,id):
    reviews = Review.objects.filter(stay_id=id)
    lowest_keywords = Keyword.objects.filter(id_review__in=reviews).order_by('polarity')[:10]
    serializer = KeywordSerializer(lowest_keywords, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#BAG OF WORDS
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getBagOfWords(request,id):
    reviews = Review.objects.filter(stay_id=id)
    keywords = Keyword.objects.filter(id_review__in=reviews)
    bag_of_words = {keyword['word']:keyword['frecuency'] for keyword in keywords}
    return Response(bag_of_words, status=status.HTTP_200_OK)


#STAYS MAP

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
@xframe_options_exempt
def getStaysMap(request):
    geolocator = Nominatim(user_agent="my_geocoder")
    #reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    stays = Stay.objects.all()
    default_location = geolocator.geocode(stays[0].location)
    if (default_location.latitude, default_location.longitude) != (None,None):
        m = folium.Map(location=[default_location.latitude, default_location.longitude], zoom_start = 12)
        for stay in stays:
            stay_location = geolocator.geocode(stay.location)
            if stay_location.latitude != None and stay_location.longitude != None:
                folium.Marker([stay_location.latitude,stay_location.longitude], popup=stay.name).add_to(m)
        
        map_html = m._repr_html_()

        return render(request, 'mapa.html',{'map_html': map_html})
    
    else:
        return render(request, 'error.html',{'error_message':'No se puedieron obtener las coordenadas de algun alojamiento'})


    







    #Admin

    #def get_keywords(self,request):
    #(Bag of words)
    #

    #def get_relevant_comments(self,request):
    #(top 10 comentarios destacados)
    #

    #def get_number_nights(self,request):
    #(diagrama con el numero de noches)
    #

    #def get_room_type(self,request):
    #(diagrama con el los distintos tipos de habitacion)
    #

    #def get_date(self,request):
    #(diagrama con la fecha de entrada de los residentes)
    #

    #def get_nationality(self,request):
    #(mapa de calor de europa nacionalidades/porcentaje de nacionalidades)
    #

    


class AdminViewAnalysis(CustomAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    #def get_stay_list(self,request):
    #   serializer = StaySerializer(request.stay)
    #   return Response({'': serializer.data}, status=status.HTTP_200_OK)

    #def get_reviews_data(self,request):
    #(lista de reviews para la pagina principal de analisis)
    #
    
    #def get_polarity(self,request):
    #(polaridad general del alojamiento)
    #

    #def get_keywords(self,request):
    #(Bag of words)
    #

    #def get_relevant_comments(self,request):
    #(top 10 comentarios destacados)
    #

    #def get_number_nights(self,request):
    #(diagrama con el numero de noches)
    #

    #def get_room_type(self,request):
    #(diagrama con el los distintos tipos de habitacion)
    #

    #def get_date(self,request):
    #(diagrama con la fecha de entrada de los residentes)
    #

    #def get_nationality(self,request):
    #(mapa de calor de europa nacionalidades/porcentaje de nacionalidades)
    #


#class UserHomePage(CustomAPIView):
    

