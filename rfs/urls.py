"""rfs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from candidate import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('cand_register',views.cand_register,name='cand_register'),
    path('rec_register',views.rec_register,name='rec_register'),
    path('candlogin',views.candlogin,name='candlogin'),
    path('reclogin',views.reclogin,name='reclogin'),
    path('user_login',views.user_login,name='user_login'),
    path('canddashboard',views.canddashboard,name='canddashboard'),
    path('recdashboard',views.recdashboard,name='recdashboard'),
    path('candprofile',views.candprofile,name='candprofile'),
    path('recprofile',views.recprofile,name='recprofile'),
    path('postjob',views.postjob,name='postjob'),
    path('jobconfirm',views.jobconfirm,name='jobconfirm'),
    path('viewjob',views.viewjob,name='viewjob'),
    path('jobapply',views.jobapply,name='jobapply'),
    path('confirmapply',views.confirmapply,name='confirmapply'),
    path('viewapplications',views.viewapplications,name='viewapplications'),
    path('candapplication',views.candapplication,name='candapplication'),
    path('applicationstatus',views.applicationstatus,name='applicationstatus'),
    path('alljobs',views.alljobs,name='alljobs'),
    path('allappjobs',views.allappjobs,name='allappjobs'),
    path('user_logout',views.user_logout,name='user_logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
