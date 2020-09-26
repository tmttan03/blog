from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView

from posts.forms import CreatePostForm, UpdatePostForm
from posts.models import Post


class PostDetailView(TemplateView):

    template_name = "posts/detail.html"

    def get(self, request, *args, **kwargs):
        try:
            post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        except:
            post = None
        return render(self.request, self.template_name, {'post': post})


class ManagePostsView(LoginRequiredMixin, TemplateView):

    template_name = "users/manage_post.html"

    def get_context_data(self, request, **kwargs):
        context = super(ManagePostsView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)
        return self.render_to_response(context)


class CreatePostView(LoginRequiredMixin, TemplateView):

    template_name = "posts/create.html"
    form = CreatePostForm

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form(self.request.POST, self.request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = self.request.user
            new_post.save()
            return redirect('post:manage-posts')
        context['form'] = form
        return self.render_to_response(context)


class UpdatePostView(LoginRequiredMixin, TemplateView):

    template_name = "posts/update.html"
    form = UpdatePostForm

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        context['form'] = self.form(instance=current_post)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        form = self.form(self.request.POST, self.request.FILES, instance=current_post)
        if form.is_valid():
            form.save()
            return redirect('post:manage-posts')
        context['form'] = form
        return self.render_to_response(context)


class PublishPostView(LoginRequiredMixin, TemplateView):

    template_name = "posts/modals/publish.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        context['post'] = current_post
        context['publish'] = True
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        current_post.status = Post.PUBLISHED
        current_post.save()
        return redirect('post:manage-posts')


class ArchivePostView(LoginRequiredMixin, TemplateView):

    template_name = "posts/modal/archive.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        context['post'] = current_post
        context['archive'] = True
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        current_post.status = Post.ARCHIVED
        current_post.save()
        return redirect('post:manage-posts')


class DeletePostView(LoginRequiredMixin, TemplateView):

    template_name = "posts/modals/delete.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        context['post'] = current_posts
        context['delete'] = True
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('id'))
        current_post.delete()
        return redirect('post:manage-posts')