from django.urls import path,re_path
from IBSngReportAPP import views

app_name = 'IBSngReport'

urlpatterns = [
    
    re_path(r'^user_login/$',views.user_login,name='user_login'),
]
