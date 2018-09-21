#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.cimiss.models import AwsArrival, RegCenterArrival, AwsBattery, AwsBatteryThreshold
import datetime, urllib, json
import requests


def reg_notice_task():

    code2city = {
        '360100': '南昌', '360200': '景德镇', '360300': '萍乡', '360400': '九江', '360500': '新余',
        '360600': '鹰潭', '360700': '赣州', '360800': '吉安', '360900': '宜春', '361000': '抚州',
        '361100': '上饶'
    }

    #1：未过质控，报文有问题，2：未到报，3：电池电压异常
    notice_content = {
        '360100':{'1':[],'2':[],'3':[]},'360200':{'1':[],'2':[],'3':[]},'360300':{'1':[],'2':[],'3':[]},
        '360400':{'1':[],'2':[],'3':[]},'360500':{'1':[],'2':[],'3':[]},'360600':{'1':[],'2':[],'3':[]},
        '360700':{'1':[],'2':[],'3':[]},'360800':{'1':[],'2':[],'3':[]},'360900':{'1':[],'2':[],'3':[]},
        '361000':{'1':[],'2':[],'3':[]},'361100':{'1':[],'2':[],'3':[]}
    }

    now = datetime.datetime.utcnow()
    f = urllib.request.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    arrivals = AwsArrival.objects.filter(data_day=now.date())
    centerarrivals = RegCenterArrival.objects.filter(data_day=now.date())
    batterys = AwsBattery.objects.filter(data_day=now.date())
    thresholds = AwsBatteryThreshold.objects.all()
    station_maps = {}

    for key, sinfo in data.items():
        station_num = sinfo["stationnum"]
        info_dic = {}
        info_dic["ac"] = sinfo["areacode"][0:4] + '00'
        info_dic["pqc"] = 0
        info_dic["cts"] = 0
        info_dic["center"] = 0
        info_dic["bat"] = -1
        info_dic["bathresh"] = 0
        station_maps[station_num] = info_dic

    for ar in arrivals:
        sno = ar.station_number
        if sno in station_maps:
            station_maps[sno]["pqc"] = 0 if getattr(ar, 'p' + now.strftime('%H')) is None else getattr(ar, 'p' + now.strftime('%H'))
            station_maps[sno]["cts"] = 0 if getattr(ar, 'a' + now.strftime('%H')) is None else getattr(ar, 'a' + now.strftime('%H'))
    for ct in centerarrivals:
        sno = ct.station_number
        if sno in station_maps:
            station_maps[sno]["center"] = 0 if getattr(ct, 'c' + now.strftime('%H')) is None else getattr(ct, 'c' + now.strftime('%H'))
    for bat in batterys:
        sno = bat.station_number
        if sno in station_maps:
            station_maps[sno]["bat"] = 0 if getattr(bat, 'b' + now.strftime('%H')) is None else getattr(bat, 'b' + now.strftime('%H'))
    for thresh in thresholds:
        sno = thresh.station_number
        if sno in station_maps:
            station_maps[sno]["bathresh"] = thresh.battery_threshold

    for key, mapinfo in station_maps.items():
        try:
            if mapinfo["pqc"] == 0 and mapinfo["cts"] == 1:
                notice_content[mapinfo["ac"]]["1"].append(key)
            if mapinfo["cts"] == 0 and mapinfo["center"] == 0:
                notice_content[mapinfo["ac"]]["2"].append(key)
            if mapinfo["bat"] <= mapinfo["bathresh"] and mapinfo["bat"] != -1:
                notice_content[mapinfo["ac"]]["3"].append(key)
        except Exception as e:
            pass


    jiangxi_notice_1 = '各地市未过质控站点个数：'
    jiangxi_notice_2 = '各地市未到报站点个数：'
    headers = {"Content-Type": "application/x-www-form-urlencoded", }
    for key, noticeinfo in notice_content.items():
        notice_str = ''
        notice_str += '区域站报文内容疑似有误站点：' + json.dumps(noticeinfo['1']) + ';'
        jiangxi_notice_1 += code2city[key] + str(len(noticeinfo['1'])) + '个,'
        notice_str += '区域站未到报站点：' + json.dumps(noticeinfo['2']) + ';'
        jiangxi_notice_2 += code2city[key] + str(len(noticeinfo['2'])) + '个,'
        notice_str += '区域站电源低于阈值站点：' + json.dumps(noticeinfo['3']) + '。'
        value_range = [{'adminCode': [key]}]
        # value_range = [{'deptName': ['数据环境支持科']}]
        notice_data = {'appCode': 'WMS-WeChat', 'content': notice_str, 'valueRanges': value_range}
        r = requests.post(url='http://10.116.32.113:8080/mbi-manager-sso-server/api/wx/sendWxCpTxtMsgByUser',
                          data=urllib.parse.urlencode(notice_data), headers=headers)
    jiangxi_notice_data = {'appCode': 'WMS-WeChat', 'content': jiangxi_notice_1+jiangxi_notice_2, 'valueRanges': [{'deptName': ['数据环境支持科']}]}
    r = requests.post(url='http://10.116.32.113:8080/mbi-manager-sso-server/api/wx/sendWxCpTxtMsgByUser',
                      data=urllib.parse.urlencode(jiangxi_notice_data), headers=headers)
