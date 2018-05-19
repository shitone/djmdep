from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.cimiss.models import AwsArrival, AwsSource, RegCenterArrival, AwsBattery
import datetime
import urllib
import json

# Create your views here.


@login_required()
def awsarrival(request):
    return render(request, 'awsarrival.html')


def awsarrivalc(request):
    return render(request, 'awsarrival_c.html', {'child_page':1})


@login_required()
def awsregsource(request):
    return render(request, 'awsregsource.html')


def awsregsourcec(request):
    return render(request, 'awsregsource_c.html', {'child_page':1})


@login_required()
def regcenter(request):
    return render(request, 'regcenter.html')


def regcenterc(request):
    return render(request, 'regcenter_c.html', {'child_page':1})


@login_required()
def awsbattery(request):
    return render(request, 'awsbattery.html')


def awsbatteryc(request):
    return render(request, 'awsbattery_c.html', {'child_page':1})


def initaws(request):
    now = datetime.datetime.utcnow()
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    q = Q()
    q.connector = 'AND'
    q.children.append(('data_day', now.date()))
    q.children.append(('a'+now.strftime('%H'), 1))
    arrivals = AwsArrival.objects.filter(q)
    srecieves = []

    for arrival in arrivals:
        srecieve = {}
        if arrival.station_number in data:
            sinfo = data[arrival.station_number]
            srecieve["sno"] = sinfo["stationnum"]
            srecieve["sname"] = sinfo["stationname"]
            srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
            srecieve["lon"] = sinfo["lontiude"]
            srecieve["lat"] = sinfo["lattiude"]
            srecieve["original"] = getattr(arrival, 'a'+ now.strftime('%H'))
            srecieve["pqc"] = getattr(arrival, 'p'+ now.strftime('%H'))
            srecieves.append(srecieve)
            del data[arrival.station_number]

    for key, sinfo in data.items():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["original"] = 0
        srecieve["pqc"] = 0
        srecieves.append(srecieve)

    return HttpResponse(json.dumps(srecieves))


def initawssource(request):
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    sources = AwsSource.objects.all()
    awss = []

    for source in sources:
        aws = {}
        if source.station_number in data:
            sinfo = data[source.station_number]
            aws["sno"] = sinfo["stationnum"]
            aws["sname"] = sinfo["stationname"]
            aws["areacode"] = sinfo["areacode"][0:4] + '00'
            aws["lon"] = sinfo["lontiude"]
            aws["lat"] = sinfo["lattiude"]
            aws["machine"] = sinfo["machine"]
            aws["county"] = sinfo["county"]
            aws["nocenter"] = source.no_center
            awss.append(aws)

        return HttpResponse(json.dumps(awss))


def initregcenter():
    now = datetime.datetime.utcnow()
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    ctslist = []
    centerlist = []

    q = Q()
    q.connector = 'AND'
    q.children.append(('data_day', now.date()))
    q.children.append(('a'+now.strftime('%H'), 1))
    ctsarrivals = AwsArrival.objects.filter(q)

    q = Q()
    q.connector = 'AND'
    q.children.append(('data_day', now.date()))
    q.children.append(('c'+now.strftime('%H'), 1))
    centerarrivals = RegCenterArrival.objects.filter(q)

    for ca in ctsarrivals:
        ctslist.append(ca.station_number)
    for cta in centerarrivals:
        centerlist.append(cta.station_number)

    srecieves = []
    for key, sinfo in data.items():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["cts_arrival"] = 0
        srecieve["center_arrival"] = 0
        if sinfo["stationnum"] in ctslist:
            srecieve["cts_arrival"] = 1
        if sinfo["stationnum"] in centerlist:
            srecieve["center_arrival"] = 1
        srecieves.append(srecieve)

    return HttpResponse(json.dumps(srecieves))


def initawsbattery(request):
    now = datetime.datetime.utcnow()
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    batterys = AwsBattery.objects.filter(data_day=now.date())
    srecieves = []

    for battery in batterys:
        srecieve = {}
        if battery.station_number in data:
            sinfo = data[battery.station_number]
            srecieve["sno"] = sinfo["stationnum"]
            srecieve["sname"] = sinfo["stationname"]
            srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
            srecieve["lon"] = sinfo["lontiude"]
            srecieve["lat"] = sinfo["lattiude"]
            srecieve["machine"] = sinfo["machine"]
            srecieve["county"] = sinfo["county"]
            battery_value = getattr(battery, 'b' + now.strftime('%H'))
            if battery_value is None:
                srecieve["battery_value"] = -1
            else:
                srecieve["battery_value"] = battery_value
            srecieves.append(srecieve)
            del data[battery.station_number]

    for key, sinfo in data.items():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["machine"] = sinfo["machine"]
        srecieve["county"] = sinfo["county"]
        srecieve["battery_value"] = -1
        srecieves.append(srecieve)

    return HttpResponse(json.dumps(srecieves))