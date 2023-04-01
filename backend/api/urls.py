from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from .views import *

urlpatterns = [
    path("orgs/<int:pk>/", OrgAPIDetail.as_view(), name="orgs_detail"),
    path("orgs/new/", OrgAPICreate.as_view(), name="create_org"),
    path('user/new/', CreateUserView.as_view(), name='create_user'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/token_auth/', obtain_auth_token, name='api_token_auth'),
]
