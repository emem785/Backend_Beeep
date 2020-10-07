from django.conf.urls import include, url
from useraccounts import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('register',  views.register,name='register'),
#     path('login', views.loginView, name='login'),
#     path('logout', auth_views.logout),
#  ]

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('mobile_register_civilian', views.mobile_register_civilian, name='mobile_register_civilian'),
    path('mobile_register_lawyer', views.mobile_register_lawyer, name='mobile_register_lawyer'),
    path('mobile_verify_code', views.mobile_verify_code, name='mobile_verify_code'),
    path('mobile_signin', views.mobile_signin, name='mobile_signin'),
    path('get_verification_code/<str:phone>', views.get_verification_code, name='get_verification_code'),
    path('login_as/<int:phone>', views.login_as_view, name='login_as'),
    path('logout', auth_views.LogoutView.as_view(template_name="/login.html"), name='logout'),
    path('logout', auth_views.LogoutView.as_view(template_name="/login.html"), name='logout'),
    path('update_password/', views.update_password, name='update_password')
    # path('mobile_register',  views.mobile_register, name='mobile_register'),
    # path('mobile_signin', views.mobile_signin, name='mobile_signin'),
    # path('user', views.user, name='user'),
    # path('test', views.test, name='test'),
    # path('create_user', views.create_user, name='create_user'),
    # path('get_users', views.get_users, name='get_users'),
    # path('logout', auth_views.logout),
]
