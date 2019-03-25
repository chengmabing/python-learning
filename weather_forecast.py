# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:55:57 2017

@author: mabing.cheng
"""

from pyquery import PyQuery as pq
import itchat
import datetime


def nickname_to_id(nickname,tag):
    #tag = 0 表示单个用户， tag = 1 表示群聊
    if tag == 0:
        pyitem = itchat.search_friends(name = nickname)
    elif tag == 1:
        pyitem = itchat.search_chatrooms(name = nickname)
    else:
        print("请输入正确参数！\n")
        return None
    return pyitem[0].UserName

receiver = {'婷婷':['chengdu'], '家人':['anqing','beijing','shanghai'], 'T-Mobile2017new':['shanghai'],'江钰婷':['anqing'], '摩西':['shanghai'], '小离':['guangzhou'],'倪莹莹':['yuyao']}
city_d = {'chengdu':'成都', 'anqing':'安庆', 'beijing':'北京', 'shanghai':'上海', 'ankang':'安康', 'guangzhou':'广州', 'yuyao':'余姚'}

itchat.auto_login(hotReload=True)
#itchat.auto_login(hotReload=true)
itchat.dump_login_status()


def get_weather(city):
    web_head = 'http://weather.sina.com.cn/'
    URL = web_head + city
    weather_html = pq(URL,encoding="utf-8")
    temp_range = weather_html('.wt_fc_c0_i_temp')('p').eq(0).text()
    temp_ls = temp_range.split('/')
    temp_max = temp_ls[0].lstrip().rstrip()
    temp_min = temp_ls[1].lstrip().rstrip()
    curr_temp = weather_html('.slider_degree').text()
    weather_bar = weather_html('.slider_detail')('p').text()
    weather_ls = weather_bar.split('|')
    pollution_index = weather_html('.slider_warn_i_tt')('p').text()
    air_quality = weather_html('.slider_warn_val3')('p').text()
    curr_date = weather_html('.slider_ct_date')('p').text()
    update_date = weather_html('.slider_ct_time').text()

    conition = weather_ls[0].lstrip().rstrip()
    wind = weather_ls[1].lstrip().rstrip()
    humidity = weather_ls[2].lstrip().rstrip()

    weather = city_d[city] + '  ' + curr_date + '\n' + '今天' + conition + ', ' + wind + '\n' + temp_min + '~' + temp_max + ', 当前温度'+ curr_temp + '\n相对' + humidity + '\n污染指数:   ' + pollution_index + '\n空气质量:   ' + air_quality + '\n(数据更新时间' + update_date + ')'
    return weather

def time_diff(send_time):
    send_time_list = send_time.split(':')
    hh = int(send_time_list[0])
    mm = int(send_time_list[1])
    curr_time = datetime.datetime.now()
    if hh < curr_time.hour:
        return (curr_time.hour-hh)*60+curr_time.minute-mm
    elif hh > curr_time.hour:
        return (hh-curr_time.hour)*60+mm-curr_time.minute
    else:
        return abs(mm-curr_time.minute)

def send_weather(nickname,tag, send_time):
    if time_diff(send_time) < 1:
        user_id = nickname_to_id(nickname,tag)
        for city in receiver[nickname]:
            itchat.send(msg=get_weather(city), toUserName=user_id)

def send_text(nickname,tag):
    user_id = nickname_to_id(nickname,tag)
    itchat.send(msg='test',toUserName=user_id)

if __name__ == '__main__':
    send_weather('小离',0,'17:00')
    send_weather('家人',1,'17:00')
	#send_weather('家人',1,'19:00')
    send_weather('T-Mobile2017new',1,'16:00')
    send_weather('倪莹莹',0,'16:00')
	#send_weather('倪莹莹',0,'19:00')
    send_weather('婷婷',0,'17:00')
    #send_weather('摩西',0,'18:50')
    send_text('摩西',0)


