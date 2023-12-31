"""
URL configuration for qr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
app_name = "core"
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name = "home"),
    path("add",views.add,name = "addcollage"),
    path("forms/<slug>",views.forms,name = "forms"),
    path("register/",views.register,name = "register"),
    path("login/",views.user_login,name = "login"),
    path('logout/',views.user_logout,name = 'logout'),
    path('viewstudents/',views.viewStudents,name = 'viewStudents'),
    path('detailview/<int:pk>',views.detailview,name = 'detailview'),
    path('delete/<int:pk>',views.deletecollage,name = 'delete'),
    path('searchdata/',views.searchdata,name = 'searchdata'),
    path('searchcollage/',views.searchcollage,name = 'searchcollage'),
    path('students/colllage/<slug>',views.student,name = "student"),
    path('first-time-login/changepassword',views.change,name = "change")
    ,path('changepassword',views.changepassword,name = "changepassword"),
    path('updateuser/<pk>',views.updateuser,name = "updateuser"),
    path('deleteuser/<pk>',views.deleteuser,name = "deleteuser"),
    path('viewuser',views.viewuser,name = "viewuser"),
    
    
]
