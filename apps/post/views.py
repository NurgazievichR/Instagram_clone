from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import CreateView
from apps.like.models import Like

from apps.post.models import Post
from apps.like.forms import LikeForm
from apps.save.forms import SaveForm

class PostListView(generic.ListView):
    queryset = Post.objects.all()
    extra_context = {'title':'Instagram'}
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ('-create_at')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likeForm'] = LikeForm()
        context['saveForm'] = SaveForm()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        likeForm = LikeForm(request.POST)
        saveForm = SaveForm(request.POST)
        print('post is going to be brought')
        post = Post.objects.get(id=request.POST.get('post_id'))
        print('Пост запрос сделан')

        if likeForm.is_valid():
            print('Like is_valid')
            liked = Like.objects.filter(post=post, user=user).count()
            if not liked:
                print('no likes')
                Like.objects.create(post=post, user=user)
            else:
                Like.objects.filter(post=post, user=user).delete()
     
    
        return HttpResponseRedirect(reverse('index'))


        # if likeForm.is_valid():
        #     user = request.user
        #     post = Post.objects.get(id=request.POST.get('post_id'))
        #     liked = Like.objects.filter(post=post, user=user).count()

        #     if not liked:
        #         Like.objects.create(post=post, user=user)
        #     else:
        #         Like.objects.filter(post=post, user=user).delete()
            
        #     return HttpResponseRedirect(reverse('index') )

    



    
    

    
