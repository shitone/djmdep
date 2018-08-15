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
    return render(request, 'cimiss/awsarrival.html')


def awsarrivalc(request):
    return render(request, 'cimiss/awsarrival_c.html', {'child_page': 1})


@login_required()
def awsregsource(request):
    return render(request, 'cimiss/awsregsource.html')


def awsregsourcec(request):
    return render(request, 'cimiss/awsregsource_c.html', {'child_page': 1})


@login_required()
def regcenter(request):
    return render(request, 'cimiss/regcenter.html')


def regcenterc(request):
    return render(request, 'cimiss/regcenter_c.html', {'child_page': 1})


@login_required()
def awsbattery(request):
    return render(request, 'cimiss/awsbattery.html')


def awsbatteryc(request):
    return render(request, 'cimiss/awsbattery_c.html', {'child_page': 1})


@login_required()
def awshistory(request):
    return render(request, 'cimiss/awshistory.html')


def awshistoryc(request):
    return render(request, 'cimiss/awshistory_c.html', {'child_page': 1})


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


def initregcenter(request):
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


def getawshistory(request, daystr):
    now = datetime.datetime.utcnow()
    search_date = datetime.datetime.strptime(daystr, '%Y-%m-%d')
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    arrivals = AwsArrival.objects.filter(data_day=search_date.date())
    centerarrivals = RegCenterArrival.objects.filter(data_day=search_date.date())
    batterys = AwsBattery.objects.filter(data_day=search_date.date())
    sources = AwsSource.objects.all()
    historys = {}

    for key, sinfo in data.items():
        cts_array = [0 for i in range(24)]
        pqc_array = [0 for i in range(24)]
        reg_array = [0 for i in range(24)]
        battery_array = [0 for i in range(24)]
        station_num = sinfo["stationnum"]
        station_info_dict = {}
        station_info_dict["sname"] = sinfo["stationname"]
        station_info_dict["machine"] = sinfo["machine"]
        station_info_dict["area"] = sinfo["area"]
        station_info_dict["county"] = sinfo["county"]
        station_info_dict["cts"] = cts_array
        station_info_dict["pqc"] = pqc_array
        station_info_dict["reg"] = reg_array
        station_info_dict["battery"] = battery_array
        historys[station_num] = station_info_dict

    for arrival in arrivals:
        sno = arrival.station_number
        if sno in data:
            historys[sno]["cts"] = arrival.get_array()[0]
            historys[sno]["pqc"] = arrival.get_array()[1]

    for center in centerarrivals:
        sno = center.station_number
        if sno in data:
            historys[sno]["reg"] = center.get_array()

    for battery in batterys:
        sno = battery.station_number
        if sno in data:
            historys[sno]["battery"] = battery.get_array()

    for source in sources:
        sno = source.station_number
        if sno in data:
            historys[sno]["source"] = source.no_center

    hour_range = 24
    date_delta = search_date.date() - now.date()
    if date_delta.days == 0:
        hour_range = now.hour

    for key, his in historys.items():
        mdos = False
        center2cts = False
        uncenter = False
        city2center = False
        cityreason = False
        for hor in range(hour_range):
            if his["cts"][hor]==1 and his["pqc"][hor]==0:
                mdos = True
            if his["reg"][hor]==1 and his["cts"][hor]==0:
                center2cts = True
            if his["reg"][hor]==0 and his["cts"][hor]==0:
                uncenter = True
            if his["reg"][hor]==0 and his["cts"][hor]==1:
                city2center = True
            if his["source"]==1 and his["cts"][hor]==0:
                cityreason = True
        fault_str = ''
        if mdos:
            fault_str += '未过快速质控,'
        if center2cts:
            fault_str += '中心站未发CTS,'
        if uncenter:
            fault_str += '未到中心站,'
        if city2center:
            fault_str += '地市直传,'
        if cityreason:
            fault_str += '地市未直传,'
        his["fault"] = fault_str


    return HttpResponse(json.dumps(historys))

