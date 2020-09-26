from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse

from users.forms import UserRegisterForm, ForgotPasswordForm, ResetPasswordForm
from users.models import (
    User, 
    ForgotPassword, 
    ForgotPassword,
    Follower
)
from posts.models import Post


class RegisterView(TemplateView):

    form = UserRegisterForm
    template_name = 'public/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Your account has been created! You are now able to login.')
            return redirect('login')
        else:
            form = self.form(self.request.POST)
        return render(request, self.template_name , {'form': form})


class ForgotPasswordView(TemplateView):

    template_name = 'public/forgot_password.html'
    form = ForgotPasswordForm

    def get(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            ForgotPassword.objects.create(
                user = user
            )
            messages.success(self.request, 'Confirmation Sent to {}'.format(email))
            return redirect('forgot-password')
        context['form'] = form
        return self.render_to_response(context)


class ForgotPasswordConfirmView(TemplateView):

    template_name = 'public/reset_password.html'

    def get(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ResetPasswordForm()
        if self.request.user.is_authenticated:
            logout(request)
        else:
            context['form'] = form
            context['token'] = self.request.GET['token']
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        token = self.request.GET['token']
        token_instance = ForgotPassword.objects.get(token=token, status=ForgotPassword.PENDING)
        form = ResetPasswordForm(self.request.POST, instance=token_instance.user)
        
        if form.is_valid():
            form.save()
            token_instance.status = ForgotPassword.USED
            token_instance.save()
            messages.success(self.request, f'Successfully reset your password.')
            return redirect('login')
        else:
            context['form'] = form
            context['token'] = token
            return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "users/dashboard.html"

    def get_context_data(self, request, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        # TODO: Show only those posts that the authenticated user has access to.
        context['posts'] = Post.objects.filter(author=self.request.user).exclude(status=Post.ARCHIVED)
        return self.render_to_response(context)


class ProfileView(TemplateView):

    template_name = "public/profile.html"

    def get_context_data(self, request, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)

        try:
            user = User.objects.get(username=self.kwargs.get('username')) 
            context['user'] = user
            context['posts'] = Post.objects.filter(author=user).exclude(status=Post.ARCHIVED)
            return self.render_to_response(context)
        except:
            context['error'] = "Oopss. That page can't be found."
            return self.render_to_response(context)


class SettingsView(TemplateView):

    template_name = "public/settings.html"

    def get_context_data(self, request, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user).exclude(status=Post.ARCHIVED)
        context['users'] = User.objects.filter(is_active=True)[:5]
        return self.render_to_response(context)
  
class LandingView(TemplateView):

    template_name = "public/landing.html"

    def get_context_data(self, request, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class FollowView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        followed_id = int(self.kwargs.get('id', ''))
        if followed_id and self.request.user.id != followed_id:
            try:
                obj = Follower.objects.get(user=self.request.user,
                                           followed_id=followed_id)
            except Follower.DoesNotExist:
                obj = Follower(user=self.request.user,
                               followed_id=followed_id)
                obj.save()
                return redirect('settings')
        return redirect('settings')
        
