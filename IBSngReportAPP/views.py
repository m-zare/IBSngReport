from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import psycopg2
from psycopg2 import sql
from IBSngReport import configParser

@login_required
def index(request):
    db = configParser.config('database.ini', 'postgresql')

    conn = psycopg2.connect(database=db['database'], user=db['user'], password=db['password'], host=db['host'], port=db['port'])
    cur = conn.cursor()

    txt= """SELECT
                  users.user_id,
                  CASE WHEN normal_users.normal_username is NULL THEN '-' ELSE normal_users.normal_username END,
                  CASE WHEN groups.group_name is NULL THEN '-' ELSE groups.group_name END, isp.isp_name,
                  CASE WHEN connection_log_internet_details.remote_ip IS NULL THEN '-' WHEN connection_log_internet_details.remote_ip='' THEN '-' ELSE connection_log_internet_details.remote_ip END,
                  CASE WHEN uname.uname is NULL THEN '-' ELSE uname.uname END,
                  CASE WHEN users.status=0 THEN 'Package' ELSE 'Recharged' END,
                  CASE WHEN online_users.online_status is NULL THEN 'FAILED' ELSE online_users.online_status END,
                  CASE WHEN ucomment.ucomment is NULL THEN '-' ELSE ucomment.ucomment END,
                  CASE WHEN ulock.ulock is NULL THEN '-' ELSE ulock.ulock END
            FROM
                  users
            LEFT JOIN normal_users ON normal_users.user_id = users.user_id
            JOIN isp ON users.isp_id = isp.isp_id
            LEFT JOIN groups ON groups.isp_id = isp.isp_id AND users.group_id = groups.group_id
            LEFT JOIN ullog ON normal_users.user_id = ullog.user_id
            LEFT JOIN connection_log_internet_details ON ullog.last_log_id = connection_log_internet_details.connection_log_id
            LEFT JOIN online_users ON users.user_id = online_users.user_id
            LEFT JOIN uname ON users.user_id = uname.user_id
            LEFT JOIN ucomment ON users.user_id = ucomment.user_id
            LEFT JOIN ulock ON users.user_id = ulock.user_id"""
    cur.execute(txt)
    x = cur.fetchall()

    my_dict={
        'id':"User ID",
        'Iusername':"Internet Username",
        'group':"Group",
        'isp':"ISP",
        'ip':"Assign IP",
        'name':"Name",
        'status':"Status",
        'online':"Online",
        'comment':'Comment',
		'lock':'Locked',
        'total': len(x),
        'data': x
    }
    cur.close()
    conn.close()
    return render(request,'IBSngReportAPP/index.html',context=my_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Not Active!')
        else:
            print("username: {} and password: {} tried to login".format(username,password))
            return HttpResponse("Invalid Login!")
    else:
        return render (request, 'IBSngReportAPP/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))
