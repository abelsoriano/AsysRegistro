from  django.urls import path

from login.views import *

urlpatterns = [
    # path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomePage.as_view(), name='index'),

]