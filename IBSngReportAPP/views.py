from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import sql
from IBSngReport import configParser

def index(request):
    db = configParser.config('database.ini', 'postgresql')

    conn = psycopg2.connect(database=db['database'], user=db['user'], password=db['password'], host=db['host'], port=db['port'])
    cur = conn.cursor()

    txt= "SELECT users.user_id, CASE WHEN normal_users.normal_username is NULL THEN '-' ELSE normal_users.normal_username END, CASE WHEN voip_users.voip_username is NULL THEN '-' ELSE voip_users.voip_username END, round(users.credit,0), CASE WHEN groups.group_name is NULL THEN '-' ELSE groups.group_name END, isp.isp_name, CASE WHEN connection_log_internet_details.remote_ip IS NULL THEN '-' WHEN connection_log_internet_details.remote_ip='' THEN '-' ELSE connection_log_internet_details.remote_ip END, CASE WHEN usernam.nam is NULL THEN '-' ELSE usernam.nam END, CASE WHEN users.status=0 THEN 'Package' ELSE 'Recharged' END,CASE WHEN online_users.online_status is NULL THEN 'FAILED' ELSE online_users.online_status END FROM users LEFT JOIN normal_users ON normal_users.user_id = users.user_id JOIN isp ON users.isp_id = isp.isp_id LEFT JOIN groups ON groups.isp_id = isp.isp_id AND users.group_id = groups.group_id LEFT JOIN slog ON normal_users.user_id = slog.user_id LEFT JOIN connection_log_internet_details ON slog.last_log_id = connection_log_internet_details.connection_log_id LEFT JOIN online_users ON users.user_id = online_users.user_id LEFT JOIN voip_users ON users.user_id = voip_users.user_id LEFT JOIN usernam ON users.user_id = userNam.user_id"

    cur.execute(txt)
    x = cur.fetchall()

    my_dict={
        'id':"User ID",
        'Iusername':"Internet Username",
        'Vusername':"VoIP Username",
        'credit':"Credit",
        'group':"Group",
        'isp':"ISP",
        'ip':"Assign IP",
        'name':"Name",
        'status':"Status",
        'online':"Online",
        'total': len(x),
        'data': x
    }
    cur.close()
    conn.close()
    return render(request,'IBSngReportAPP/index.html',context=my_dict)
