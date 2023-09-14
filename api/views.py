from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, generics, permissions
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from .models import Stay, Review, Keyword,User
from .validations import custom_validation, validate_email, validate_password, validate_username
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, StaySerializer
from .custom_views import CustomAPIView

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
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogout(CustomAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class UserView(CustomAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    

class StayView(CustomAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def getAllStays(self, request): 
        stays = Stay.objects.all()
        serializer = StaySerializer(stays, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def getStay(self, request, id):
        stay = get_object_or_404(Stay,stay_id=id)
        serializer = StaySerializer(stay)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewView(APIView):
    permission_classes = (permissions.IsAuthenticated,)    
    def get_reviews_data(self,request,id):
        data = []
        review_list = Review.objects.all()
        for review in review_list: data.append(review)
        return Response(data, status=status.HTTP_200_OK)
    
    def get_review_numbernights(self,request,id):
        dict = {}
        numbernights_list = Review.objects.filter(stay_id=id).values_list('number_nights',flat=True)
        for numbernight in numbernights_list:
            if numbernight in dict:
                dict[numbernight] += 1
            else:
                dict[numbernight] = 1
        
        return Response(dict, status=status.HTTP_200_OK)
    
    def get_review_client_type(self,request,id):
        dict = {}
        client_type_list = Review.objects.filter(stay_id=id).values_list('client_type',flat=True)
        for client_type_ in client_type_list:
            if client_type_ in dict:
                dict[client_type_] += 1
            else:
                dict[client_type_] = 1
        return Response(dict, status=status.HTTP_200_OK)
    
    def get_latest_review(self,request,id):
        lat
        
#class KeywordView(APIView):
    
    #def getAllKeyWord(self,request):
    #(polaridad general del alojamiento)
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
    

