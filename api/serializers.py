from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import Stay, Review, Keyword

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username','email','password']
    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'],password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj
    
class UserLoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        
        def check_user(self, clean_data):
            user = authenticate(username=clean_data['email'], password=clean_data['password'])
            if not user:
                raise ValidationError('user not found')
            return user  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username','email','is_staff']

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = ['stay_id','name', 'url', 'location', 'polarity']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['costumer_name','nationality', 
        'comment', 'room_type', 'number_nights',  
        'date_review', 'date_entry', 'client_type', 'polarity']
        
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['word', 'polarity', 'frecuency']
