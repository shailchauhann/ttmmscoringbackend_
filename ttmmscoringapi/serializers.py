from rest_framework import serializers
from .models import *

class StartupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Startup
        fields = ('name','image','totalbid','current','done')

class FundingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Funding
        fields = ('investor_name','startup_name','funding','finalsubmit')