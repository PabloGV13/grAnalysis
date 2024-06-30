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
import json 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .scripts import normalize_url,stay_is_reviewed,create_new_stay, get_data, get_sentiment_analysis

#USUARIOS

class UserRegister(CustomAPIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Registrar un nuevo usuario.",
        request_body=UserRegisterSerializer,
        responses={
            201: UserRegisterSerializer,
            400: 'Invalid request'
        }
    )

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

    @swagger_auto_schema(
        operation_description="Iniciar sesión de usuario.",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response('Login Successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'tokens': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )),
            400: 'Invalid email or password'
        }
    )
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

    @swagger_auto_schema(
        operation_description="Cerrar sesión del usuario.",
        responses={
            200: 'Logout Successful'
        }
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

#Comprobacion de usuario actual#
class UserView(CustomAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,BasicAuthentication)

    @swagger_auto_schema(
        operation_description="Obtener datos del usuario actual.",
        responses={
            200: openapi.Response('User Data', UserSerializer),
            403: 'Forbidden'
        }
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    


#Lista de usuarios
@swagger_auto_schema(
    method='get',
    operation_description="Obtener todos los usuarios.",
    responses={
        200: UserSerializer(many=True),
        403: 'Forbidden'
    }
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])  #DEBERIA DE SER: IsAuthenticated
def getAllUsers(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



#Eliminar un usuario
@swagger_auto_schema(
    method='delete',
    operation_description="Eliminar un usuario por ID.",
    responses={
        200: 'User deleted',
        401: 'Invalid deletion of admin user',
        404: 'Not found'
    }
)
@api_view(['DELETE','GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])  #DEBERIA DE SER: IsAuthenticated
def deleteUser(request, id):
    user = User.objects.filter(user_id=id)
    user = user[0]
    username = user.username
    if(user.is_staff != True):
        user.delete()
        return Response(data = {"message": "User deleted"}, status=status.HTTP_200_OK)
    else:
        return Response(data = {"message": "Invalid deletion of admin user"},status=status.HTTP_401_UNAUTHORIZED)



#ALOJAMIENTOS

#Lista de alojamientos
@swagger_auto_schema(
    method='get',
    operation_description="Obtener todos los alojamientos analizados.",
    responses={
        200: StaySerializer(many=True),
        403: 'Forbidden request',
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getAllStays(request): 
    stays = Stay.objects.filter(is_analysed=True)
    serializer = StaySerializer(stays, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Obtener un alojamiento
@swagger_auto_schema(
    method='get',
    operation_description="Obtener un alojamiento por ID.",
    responses={
        200: StaySerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getStay(request, id):
    stay = get_object_or_404(Stay,stay_id=id)
    serializer = StaySerializer(stay)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Publicar una solicitud de alojamiento
@swagger_auto_schema(
    method='post',
    operation_description="Solicitar un nuevo alojamiento.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='Stay URL')
        }
    ),
    responses={
        201: openapi.Response('Request made successfully.'),
        401: openapi.Response('Invalid URL'),
        403: openapi.Response('Stay request')
    }
)
@api_view(('POST',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def postRequestedStay(request):
    url_ = request.data.get('url')
    url = normalize_url(url_)

    if(url == "URL invalida"):
        return Response(data = {"message": "La URL es invalida."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        (id_,is_reviewed) = stay_is_reviewed(url)
        if is_reviewed:
            return Response(data = {"message": "El alojamiento ya está registrado."}, status=status.HTTP_403_FORBIDDEN)
        else:
            create_new_stay(url)
            return Response(data = {"message": "Se ha realizado la solicitud con éxito."}, status=status.HTTP_201_CREATED)

#Obtener Solicitudes de alojamientos
@swagger_auto_schema(
    method='get',
    operation_description="Obtener todas las solicitudes de alojamientos no analizados.",
    responses={
        200: StaySerializer(many=True),
        404: 'Not found'
    }
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getRequestedStay(request):
    staysRequested = Stay.objects.filter(is_analysed=False)
    serializer = StaySerializer(staysRequested, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Eliminar solicitud alojamiento
@swagger_auto_schema(
    method='delete',
    operation_description="Eliminar una solicitud de alojamiento por ID.",
    responses={
        200: openapi.Response('Request deleted'),
        404: 'Not found'
    }
)
@api_view(['DELETE','GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])  #DEBERIA DE SER: IsAuthenticated
def deleteStay(request, id):
    stay = get_object_or_404(Stay, stay_id = id)
    stay.delete()
    return Response(data = {"message": "Solicitud eliminada"}, status=status.HTTP_200_OK)
    
    
#Realizar analisis del alojamiento
@swagger_auto_schema(
    method='post',
    operation_description="Realizar el análisis de un alojamiento por ID.",
    responses={
        200: openapi.Response('Analysis performed successfully.'),
        404: 'Not found'
    }
)
@api_view(('POST',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def postStayAnalysis(request, id):
    stay = get_object_or_404(Stay, stay_id=id)
    get_data(stay)
    get_sentiment_analysis(stay)
    return Response(data = {"message": "Se ha realizado el análisis con éxito."}, status=status.HTTP_200_OK)



    
    






# class ReviewView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)    




#Diccionario con el numero de noches(diagrama tarta)
@swagger_auto_schema(
    method='get',
    operation_description="Obtener un diccionario con el número de noches de las reviews.",
    responses={
        200: openapi.Response('Dictionary with the number of nights.'),
        404: 'Not found'
    }
)
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
@swagger_auto_schema(
    method='get',
    operation_description="Obtener un diccionario con el tipo de clientes.",
    responses={
        200: openapi.Response('Dictionary with types of clients'),
        404: 'Not found'
    }
)
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

#Obtener la review más reciente
@swagger_auto_schema(
    method='get',
    operation_description="Obtener la review más reciente.",
    responses={
        200: ReviewSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_latest_review(request,id):
    latest_date = Review.objects.filter(stay_id=id).aggregate(latest_date=Max('date_review'))['latest_date']
    latest_review = Review.objects.filter(stay_id=id, date_review=latest_date).first()
    serializer = ReviewSerializer(latest_review)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Obtener la review más antigua
@swagger_auto_schema(
    method='get',
    operation_description="Obtener la review más antigua.",
    responses={
        200: ReviewSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_oldest_review(request,id):
    oldest_date = Review.objects.filter(stay_id=id).aggregate(oldest_date=Min('date_review'))['oldest_date']
    oldest_review = Review.objects.filter(stay_id=id, date_review=oldest_date).first()
    serializer = ReviewSerializer(oldest_review)
    return Response(serializer.data, status=status.HTTP_200_OK)



#Obtener la review más positiva
@swagger_auto_schema(
    method='get',
    operation_description="Obtener la review con una polaridad más positiva.",
    responses={
        200: ReviewSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_mostPostive_review(request,id):
    positive_polarity = Review.objects.filter(stay_id=id).aggregate(positive_polarity=Max('polarity'))['positive_polarity']
    positive_review = Review.objects.filter(stay_id=id,polarity=positive_polarity).first()
    serializer = ReviewSerializer(positive_review)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Obtener la review más negativa
@swagger_auto_schema(
    method='get',
    operation_description="Obtener la review con una polaridad más negativa.",
    responses={
        200: ReviewSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def get_mostNegative_review(request,id):
    negative_polarity = Review.objects.filter(stay_id=id).aggregate(negative_polarity=Min('polarity'))['negative_polarity']
    negative_review = Review.objects.filter(stay_id=id,polarity=negative_polarity).first()
    serializer = ReviewSerializer(negative_review)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# Palabras mas positivas
@swagger_auto_schema(
    method='get',
    operation_description="Obtener las 10 palabras más positivas sobre un alojamiento.",
    responses={
        200: KeywordSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getTopPolarityKeyWords(request,id):
    reviews = Review.objects.filter(stay_id = id)
    top_keywords = Keyword.objects.filter(id_review__in=reviews).order_by('-polarity')[:10]
    serializer = KeywordSerializer(top_keywords, many = True) 
    return Response(serializer.data, status=status.HTTP_200_OK)


#Palabras mas negativas
@swagger_auto_schema(
    method='get',
    operation_description="Obtener las 10 palabras más negativas sobre un alojamiento.",
    responses={
        200: KeywordSerializer,
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getLowestPolarityKeywords(request,id):
    reviews = Review.objects.filter(stay_id=id)
    lowest_keywords = Keyword.objects.filter(id_review__in=reviews).order_by('polarity')[:10]
    serializer = KeywordSerializer(lowest_keywords, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#BAG OF WORDS
@swagger_auto_schema(
    method='get',
    operation_description="Obtener un diccionario con las palabras más frecuentes.",
    responses={
        200: openapi.Response('Dictionary with the most frequent words'),
        404: 'Not found'
    }
)
@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def getBagOfWords(request,id):
    reviews = Review.objects.filter(stay_id=id)
    keywords = Keyword.objects.filter(id_review__in=reviews)
    bag_of_words = {keyword['word']:keyword['frecuency'] for keyword in keywords}
    return Response(bag_of_words, status=status.HTTP_200_OK)


#STAYS MAP


@api_view(('GET',))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
@xframe_options_exempt
def getStaysMap(request):
    geolocator = Nominatim(user_agent="my_geocoder")
    stays = Stay.objects.all()
    
    if not stays:
        return render(request, 'error.html', {'error_message': 'No hay alojamientos disponibles.'})

    default_location = geolocator.geocode(stays[0].location)
    
    if default_location is None or (default_location.latitude, default_location.longitude) == (None, None):
        return render(request, 'error.html', {'error_message': 'No se pudo obtener la ubicación del alojamiento predeterminado.'})

    m = folium.Map(location=[default_location.latitude, default_location.longitude], zoom_start=12)
    
    for stay in stays:
        try:
            stay_location = geolocator.geocode(stay.location)
            if stay_location and stay_location.latitude and stay_location.longitude:
                folium.Marker([stay_location.latitude, stay_location.longitude], popup=stay.name).add_to(m)
            else:
                print(f"Ubicación no encontrada para: {stay.name}")
        except Exception as e:
            print(f"Error al geocodificar la ubicación para: {stay.name}, error: {e}")

    map_html = m._repr_html_()
    return render(request, 'mapa.html', {'map_html': map_html})



#Admin

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

    

