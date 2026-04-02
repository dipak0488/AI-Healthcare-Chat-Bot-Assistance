from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name="login"),   # Default login page
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('home/', views.home, name="home"),
    path('logout/', views.user_logout, name="logout"),
    path('chat/', views.chatbot, name="chat"),
    path('get/', views.get_response, name="get_response"),
    path('report/', views.download_report, name="report"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-register-otp/', views.verify_register_otp, name='verify_register_otp'),
    
]
