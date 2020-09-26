from django.urls import path, re_path
from users.views import (
    FollowView
)

app_name = "post"

urlpatterns = [
    re_path(r'^follow/(?P<id>\d+)/$', FollowView.as_view(), name='follow-user'),
]