from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import include, url

from users.views import (
    RegisterView,
    DashboardView,
    ForgotPasswordView,
    ForgotPasswordConfirmView,
    ProfileView,
    LandingView,
    SettingsView
)

urlpatterns = [

    re_path(r'^admin/', admin.site.urls),

    re_path(r'^$', LandingView.as_view(), name='landing'),

    # Public 

    re_path(r'^accounts/login/', auth_views.LoginView.as_view(
        template_name='public/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    re_path(
        r'^logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    re_path(r'^register/', 
            RegisterView.as_view(), 
            name='register'),

    re_path(r'^forgot-password/', 
            ForgotPasswordView.as_view(), 
            name='forgot-password'),

    re_path(r'^reset-password/', 
            ForgotPasswordConfirmView.as_view(), 
            name='reset-password'),

    # Private

    re_path(r'^dashboard/', 
            DashboardView.as_view(), 
            name='dashboard'),

    re_path(r'^settings/', 
            SettingsView.as_view(), 
            name='settings'),

    re_path(r'^post/', 
            include('posts.urls', 
            namespace="post")), 

    re_path(r'^user/', 
            include('users.urls', 
            namespace="user")),   

    # Root Pages

    url(r'^@(?P<username>[^/]+)/$', 
        ProfileView.as_view(), 
        name='profile'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
