from  django.urls import path

from login.views import *

urlpatterns = [
    # path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('home/', dashboard_unificado , name='index'),
    path('registro/', registro, name='registro'),

]