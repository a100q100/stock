#-*- coding:utf8 -*-
import json
import pymysql
import csv
import requests

db = pymysql.connect("127.0.0.1","root","yungege_test","stock" )
cursor = db.cursor()

def get_info(id):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            "Cookie":"_ga=GA1.2.1197435973.1551018842; device_id=dd71de99dc275bf78a8853c89326d074; s=ej11t4gzin; xq_a_token=d8474141c84f89dfd8192ed057589c907247ad25; xq_a_token.sig=qQxckS03yaBOAH2A-PRiZ6RoIrc; xq_r_token=43957cca9e5babf3d6e6bfba4e8bd87d54b2b2b4; xq_r_token.sig=gfDc5JwKlyApNHlEy59tOERQoKw; _gid=GA1.2.573513587.1551876202; u=361551876202307; Hm_lvt_1db88642e346389874251b5a1eded6e3=1551714746,1551717050,1551760335,1551876202; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1551876202"}
    url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=" + id
    r = requests.get(url,headers=headers)
    data = r.json()
    t = data['data'][0]
    cur_price = t['current']
    percent = t['percent']
    market_capital = t['market_capital']
    float_market_capital = t['float_market_capital']

    sql = "update base set cur_price=%s,percent=%s,market_capital=%s,float_market_capital=%s where id='%s'" % \
       (cur_price,percent,market_capital,float_market_capital, id)
    
    #cursor.execute(sql)
    try:
       cursor.execute(sql)
    except:
       print(sql)

with open('list.csv','r',encoding='utf-8') as csvfile:
    read = csv.reader(csvfile)
    title = True
    for v in read:
        if title:
            title = False
            continue
        id = v[0]
        get_info(id)

db.commit()
db.close()

