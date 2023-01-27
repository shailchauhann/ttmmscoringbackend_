from rest_framework import serializers
from .models import *
from . import models



class StartupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Startup
        fields = ('name','image','totalbid','current','done')

class FundingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Funding
        fields = ('investor_name','startup_name','funding','finalsubmit')


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminUser
        # fields = '__all__'
        fields = ('name','image')


class Funding2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Funding2
        fields = ('investor_name','startup_name','funding')


class PortalControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PortalControl
        fields = '__all__'


class FundingCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Funding2
        fields = '__all__'

class StartupFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Startup
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminUser
        fields = '__all__'

class FundingFetchSerializer(serializers.ModelSerializer):
    investor_name = InvestorSerializer(many=False)
    class Meta:
        model = models.Funding2
        # fields = '__all__'
        fields = ('investor_name','startup_name','funding')
