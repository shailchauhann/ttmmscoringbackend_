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

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse




@api_view(["POST"])
def defaultbid(request):
    data = request.data
    adminusers = AdminUser.objects.filter(name=data['investor_name'])
    adminuser = adminusers[0]
    data_list = []
    fundings = Funding2.objects.filter(investor_name=adminuser)
    for funding in fundings:
        startup_name = funding.startup_name.name
        isfund = funding.startup_name.isfunded
        bid = funding.funding
        data = OrderedDict([('startup_name',startup_name),('bid',bid),('isfunded',isfund)])
        data_list.append(data)
    
    return Response(data_list)

@csrf_exempt
@api_view(["POST"])
def token(request):
    data = request.data
    adminusers = AdminUser.objects.filter(name=data['username'])
    if len(adminusers)==0:
        return JsonResponse({"success":False},safe=False)
    adminuser = adminusers[0]
    if adminuser.password != data['password']:
        return JsonResponse({"success":False},safe=False)
   
    return JsonResponse({"success":True,"admin_name":adminuser.name},safe=False)

@api_view(["POST"])
def bidding(request):
    data = request.data
    admins = AdminUser.objects.filter(name=data['investor_name'])
    startups = Startup.objects.filter(name=data['startup_name'])
    if len(admins)==0 | len(startups)==0:
        return JsonResponse({"success":False},safe=False)
    fund_amount = data['bid']
    admin = admins[0]
    startup = startups[0]
    previous_funding = Funding2.objects.filter(investor_name=admin,  startup_name=startup)
    if len(previous_funding)==0:
        funding = Funding2(investor_name = admin, startup_name = startup, funding = fund_amount)
        funding.save()
    else:
        prev_fund = previous_funding[0]
        prev_fund.funding = fund_amount
        prev_fund.save()
    
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
    previous_funding = Funding2.objects.filter(investor_name=admin,  startup_name=startup)
    if len(previous_funding)==0:
        funding = Funding2(investor_name = admin, startup_name = startup, funding = fund_amount, finalsubmit=True)
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
    startprogress = startup.showprogress
    # if len(startups)==0:
    #     return JsonResponse({"success":False},safe=False)
    # startup = startups[0]
    funding = Funding2.objects.filter(startup_name=startup)
    if len(funding)==0:
        return JsonResponse({"success":False},safe=False)
    for funds in funding:
        investor_name = funds.investor_name
        admins = AdminUser.objects.filter(name=investor_name.name)
        admin = admins[0]
        image_url = 'http://localhost:8000'+admin.image.url
        data = OrderedDict([('investor_name',admin.name),('image',image_url),('bid',funds.funding)])
        data_list.append(data)
    # data_list.append({'progress':startprogress})
    # data_list.append({"success":True})
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data_list)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def showprogress(request):
    data = request.data
    startups = Startup.objects.get(name=data['startup_name'])
    data_list = []
    data_list.append({"progress": startups.showprogress})
    # startup_ser = serializers.StartupSerializer(
    # startups, many=True)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data_list)

@api_view(["POST"])
# @permission_classes((AllowAny,))
def showinvestor(request):
    data = request.data
    startups = Startup.objects.get(name=data['startup_name'])
    data_list = []
    data_list.append({"isinvestor": startups.showinvestor})
    # startup_ser = serializers.StartupSerializer(
    # startups, many=True)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data_list)

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
    bids = Funding2.objects.filter(startup_name=startups)
    totalbid = 0
    if len(bids)==0:
        totalbid = 0
        # return Response('done')
    else:
        for bid in bids:
            totalbid += bid.funding
        if totalbid>=24:
            percentage="100%"
            startups.isfunded = True
        else:
            percent=int((totalbid/24)*100)
            percentage=str(percent)+'%'
            startups.isfunded = False
        # return Response('done2')
    data_list = []
    data = OrderedDict([('totalbid',totalbid),('percentage',percentage)])
    data_list.append(data)
    # token,created = Token.objects.get_or_create(user=user)
    # adminuser = AdminUser(name=data['username'])
    return Response(data_list)


@api_view(['GET'])
def portal_control(request):
    portal = PortalControl.objects.get(control_name='ttmm')
    portal_ser = serializers.PortalControlSerializer(portal,many=False)
    return Response(portal_ser.data)



@api_view(['GET'])
def investor_fetch(request):
    investor = AdminUser.objects.all()
    try:
        investor_ser = serializers.AdminSerializer(investor,many=True)
    except:
        investor_ser = serializers.AdminSerializer(investor,many=False)


    return Response(investor_ser.data)


@api_view(['GET'])
def startup_fetch(request):
    startup= Startup.objects.all()
    start_ser = serializers.StartupFetchSerializer(startup,many=True)
    return Response(start_ser.data)



@api_view(['GET'])
def funding_fetch(request):
    control = PortalControl.objects.get(control_name='ttmm')
    startup= Startup.objects.filter(name=control.current_startup)
    start_ser = serializers.StartupFetchSerializer(startup,many=True)
    return Response(start_ser.data)


@api_view(['GET'])
def startup_funding(request):
    control = PortalControl.objects.get(control_name='ttmm')
    startup= Funding2.objects.filter(startup_name=control.current_startup)
    try:
        start_ser = serializers.FundingFetchSerializer(startup,many=True)
    except:
        start_ser = serializers.FundingFetchSerializer(startup,many=False)



    return Response(start_ser.data)

@api_view(['POST'])
def funding_post(request):
    reqData = request.data
    username= reqData['username']
    startupname= reqData['startup']
    amount= reqData['amount']
    investor = AdminUser.objects.get(name=username)
    startup = Startup.objects.get(name=startupname)
    try:
        new_funding = Funding2.objects.get(investor_name=investor,startup_name=startup)
        new_funding.funding=amount
        new_funding.save()
    except:
        new_funding = Funding2.objects.create(investor_name=investor,startup_name=startup)
        new_funding.funding=amount
        new_funding.save()
    new_funding.save()
    ser_fund = serializers.FundingCreateSerializer(new_funding)
    
    return Response(ser_fund.data)
    return Response("Hello from backend")

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls / index.html', context)
 
# Show specific question and choices
 
 
def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls / detail.html', {'question': question})
 
# Get question and display results
 
 
def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls / results.html', {'question': question})
 
# Vote for a question choice
 
 
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls / detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args =(question.id, )))

