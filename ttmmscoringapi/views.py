from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from typing import OrderedDict
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import serializers

# Create your views here.
@api_view(["POST"])
# @permission_classes((AllowAny,))
def defaultbid(request):
    data = request.data
    adminusers = AdminUser.objects.filter(name=data['investor_name'])
    adminuser = adminusers[0]
    data_list = []
    fundings = Funding.objects.filter(investor_name=adminuser)
    # users = User.objects.filter(username=data['username'])
    for funding in fundings:
        startup_name = funding.startup_name.name
        bid = funding.funding
        data = OrderedDict([('startup_name',startup_name),('bid',bid)])
        data_list.append(data)
    # funding_ser = serializers.FundingSerializer(fundings, many=True)
    # token,created = Token.objects.get_or_create(user=user)
    return Response(data_list)

@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def token(request):
    data = request.data
    adminusers = AdminUser.objects.filter(name=data['username'])
    # users = User.objects.filter(username=data['username'])
    if len(adminusers)==0:
        return JsonResponse({"success":False},safe=False)
    adminuser = adminusers[0]
    if adminuser.password != data['password']:
        return JsonResponse({"success":False},safe=False)
    # token,created = Token.objects.get_or_create(user=user)
    return JsonResponse({"success":True,"admin_name":adminuser.name},safe=False)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def bidding(request):
    data = request.data
    admins = AdminUser.objects.filter(name=data['investor_name'])
    startups = Startup.objects.filter(name=data['startup_name'])
    if len(admins)==0 | len(startups)==0:
        return JsonResponse({"success":False},safe=False)
    fund_amount = data['bid']
    admin = admins[0]
    startup = startups[0]
    previous_funding = Funding.objects.filter(investor_name=admin,  startup_name=startup)
    if len(previous_funding)==0:
        funding = Funding(investor_name = admin, startup_name = startup, funding = fund_amount)
        funding.save()
    else:
        prev_fund = previous_funding[0]
        prev_fund.funding = fund_amount
        prev_fund.save()
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return JsonResponse({"success":True},safe=False)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def finalbid(request):
    data = request.data
    admins = AdminUser.objects.filter(name=data['investor_name'])
    startups = Startup.objects.filter(name=data['startup_name'])
    if len(admins)==0 | len(startups)==0:
        return JsonResponse({"success":False},safe=False)
    fund_amount = data['bid']
    admin = admins[0]
    startup = startups[0]
    previous_funding = Funding.objects.filter(investor_name=admin,  startup_name=startup)
    if len(previous_funding)==0:
        funding = Funding(investor_name = admin, startup_name = startup, funding = fund_amount, finalsubmit=True)
        funding.save()
    else:
        prev_fund = previous_funding[0]
        prev_fund.funding = fund_amount
        prev_fund.finalsubmit = True
        prev_fund.save()
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return JsonResponse({"success":True},safe=False)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def investors(request):
    data = request.data
    data_list = []
    # admins = AdminUser.objects.filter(name=data['investor_name'])
    startup = Startup.objects.get(name=data['startup_name'])
    # if len(startups)==0:
    #     return JsonResponse({"success":False},safe=False)
    # startup = startups[0]
    funding = Funding.objects.filter(startup_name=startup)
    if len(funding)==0:
        return JsonResponse({'sucess',False},safe=False)
    for funds in funding:
        investor_name = funds.investor_name
        admins = AdminUser.objects.filter(name=investor_name.name)
        admin = admins[0]
        image_url = 'http://localhost:8000/'+admin.image.url
        data = OrderedDict([('investor_name',admin.name),('image',image_url),('bid',funds.funding)])
        data_list.append(data)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return JsonResponse(data_list, safe=False)

@api_view(["GET"])
# @permission_classes((AllowAny,))
def startupsall(request):
    startups = Startup.objects.all()
    startup_ser = serializers.StartupSerializer(
    startups, many=True)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(startup_ser.data)

@api_view(["GET"])
# @permission_classes((AllowAny,))
def currentstartups(request):
    startups = Startup.objects.filter(current=True)
    startup = startups[0]
    # data_list= []
    name = startup.name
    # data_list.append(name)
    data2 = OrderedDict([('startup_name',name)])
    startup_ser = serializers.StartupSerializer(
    startups, many=True)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data2)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def progress(request):
    data = request.data
    startups = Startup.objects.get(name=data['startup'])
    # ser = serializers.StartupSerializer(startups, many=True)
    bids = Funding.objects.filter(startup_name=startups)
    totalbid = 0
    if len(bids)==0:
        totalbid = 0
        # return Response('done')
    else:
        for bid in bids:
            totalbid += bid.funding
        if totalbid>=24:
            percentage="100%"
        else:
            percent=int((totalbid/24)*100)
            percentage=str(percent)+'%'
        # return Response('done2')
    data_list = []
    data = OrderedDict([('totalbid',totalbid),('percentage',percentage)])
    data_list.append(data)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data_list)