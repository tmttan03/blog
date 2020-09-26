from django.urls import path, re_path
from posts.views import (
    PostDetailView, 
    ManagePostsView,
    CreatePostView,
    UpdatePostView,
    PublishPostView,
    ArchivePostView,
    DeletePostView
)

app_name = "post"

urlpatterns = [
    path(r'', ManagePostsView.as_view(), name='manage-posts'),
    re_path(r'^create/$', CreatePostView.as_view(), name='new-post'),
    re_path(r'^update/(?P<id>\d+)/$', UpdatePostView.as_view(), name='update-post'),
    re_path(r'^publish/(?P<id>\d+)/$', PublishPostView.as_view(), name='publish-post'),
    re_path(r'^archive/(?P<id>\d+)/$', ArchivePostView.as_view(), name='archive-post'),
    re_path(r'^delete/(?P<id>\d+)/$', DeletePostView.as_view(), name='delete-post'),
    re_path(r'^(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='detail-page'),
    
]