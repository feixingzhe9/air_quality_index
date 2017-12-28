#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 获取国内城市 30天内 每天空气质量指数（AQI）
# 数据来源：中华人民共和国环境保护部
import requests
from bs4 import BeautifulSoup
import datetime

ref_url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action'
req_url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action'


def get_html_content(city='西安市', V_DATE='2016-01-01', E_DATE='2017-10-08'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': ref_url,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    data_dict = {
        'page.pageNo': '1',
        'xmlname': '1462259560614',
        'queryflag': 'close',
        'CITY': city,
        'isdesignpatterns': 'false',
        'V_DATE': V_DATE,
        'E_DATE': E_DATE,
    }
    r = requests.post(req_url, data=data_dict, headers=headers, timeout=60)
    return r.text


def date_format():
    dd = datetime.datetime.now()
    E_DATE = dd.strftime('%Y-%m-%d')
    SomeDaysAgo = (dd - datetime.timedelta(days=31))
    V_DATE = SomeDaysAgo.strftime('%Y-%m-%d')
    return (V_DATE, E_DATE)


def get_aqi_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    aqi_table = soup.find(id='GridView1')
    aqi_trs = aqi_table.find_all('tr')[1:]
    result = {}
    for aqi_tr in aqi_trs:
        aqi_tds = aqi_tr.find_all('td')
        aqi = aqi_tds[3].string
        dd = aqi_tds[6].string
        result[dd] = aqi
    return result


if __name__ == '__main__':
    city = input('请输入城市名称： ')
    (V, E) = date_format()
    content = get_html_content(city, V, E)
    result = get_aqi_info(content)
    print(city, '最近xx天空气质量指数如下：\n')
    aqi_sum = 0
    cnt = 0
    for key in sorted(result.keys()):
        print(key, '\t', result[key])
        aqi_sum = aqi_sum + int(result[key]) 
        cnt = cnt + 1

    average_aqi = aqi_sum / cnt 
    print(city, "average aqi is",average_aqi)
