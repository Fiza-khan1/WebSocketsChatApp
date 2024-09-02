
from django.urls import path
from .views import UserRegisterView, UserLoginView

from . import views


urlpatterns = [
    path('test/',views.msgfromoutside,name='test'),
   path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/',views.UserLogoutView.as_view(), name='logout'),
    # path('<str:groupname>/',views.index,name='index'),
   
]


