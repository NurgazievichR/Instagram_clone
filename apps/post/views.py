from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.utils import timezone

from apps.like.models import Like
from apps.post.models import Post, Tag
from apps.save.models import Save
from apps.user.models import CustomUser
from apps.follower.models import Follower
from apps.post.mixins import SearchMixin, LikeAndSaveMixin
from apps.user.tasks import complaint
from apps.comment.models import Comment








@method_decorator(login_required, name='dispatch')
class PostListView(SearchMixin, LikeAndSaveMixin, generic.ListView):
    model = Post
    extra_context = {'title':'Instagram'}
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = Follower.objects.filter(from_user=self.request.user)
        ids = [i.to_user.id for i in subscriptions]
        context['posts'] = self.get_queryset().filter(owner_id__in = ids)
        context['user_stories'] = CustomUser.objects.filter(id__in = ids)
        context['r_posts'] = self.get_queryset().exclude(owner_id__in = ids).exclude(owner_id = self.request.user.id).order_by('-views')[:6]
        context['LikedByUserPosts'] = Like.objects.filter(user=self.request.user)
        context['SavedByUserPosts'] = Save.objects.filter(user=self.request.user)
        context['rec_users'] = CustomUser.objects.exclude(id__in = ids).order_by('-views')[:4]

        
        return context

    def post(self, request, *args, **kwargs):
        if 'follow_to' in request.POST:
            Follower.objects.create(from_user=request.user, to_user=CustomUser.objects.get(username=request.POST['follow_to']))
        if 'complaint' in request.POST:
            id = request.POST['complaint']
            request_user = request.user.username
            complaint.delay(id, request_user)
        return super().post(request, *args, **kwargs)



class FeaturedPosts(SearchMixin, generic.TemplateView):
    template_name = 'featured/featured.html'
    extra_context = {'title':'Saved'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Save.objects.filter(user=self.request.user)
        return context







class HashTagPosts(SearchMixin, generic.TemplateView):
    template_name: str = 'featured/featured.html'
    def get_context_data(self, **kwargs):
        h = self.kwargs['hashtag']
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(title=h)
        context['h_posts'] = Post.objects.filter(post_tags=tag)
        context['title'] = f'#{h}' 
        return context


    
    


class FeaturedPostsDetail(SearchMixin, generic.TemplateView):
    template_name = 'index.html'
    extra_context = {'title':'Saved Posts'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saved = Save.objects.filter(user=self.request.user)
        ids = [i.post.id for i in saved]
        context['posts'] =  Post.objects.filter(id__in = ids)
        if self.request.user.is_authenticated:
            context['LikedByUserPosts'] = Like.objects.filter(user=self.request.user)
            context['SavedByUserPosts'] = Save.objects.filter(user=self.request.user)   
        return context 

    def post(self, request, *args, **kwargs):
        user = request.user
        if 'save_id' in request.POST:
            post = Post.objects.get(id=request.POST.get('save_id'))
            saved = Save.objects.filter(post=post, user=user).count()
            if not saved:
                Save.objects.create(post=post, user=user)
            else:
                Save.objects.filter(post=post, user=user).delete()

        if 'like_id' in request.POST:
            post = Post.objects.get(id=request.POST.get('like_id'))
            liked = Like.objects.filter(post=post, user=user).count()
            if not liked:
                Like.objects.create(post=post, user=user)
            else:
                Like.objects.filter(post=post, user=user).delete()

        if 'complaint' in request.POST:
            id = request.POST['complaint']
            request_user = request.user.username
            complaint.delay(id, request_user)
        return HttpResponseRedirect(reverse('saved_posts_detail'))


class PostDetailView(SearchMixin, generic.DetailView):
    template_name = 'post_detail_view.html'
    model = Post
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk'])

        if self.request.user.is_authenticated:
            context['LikedByUserPosts'] = Like.objects.filter(user=self.request.user)
            context['SavedByUserPosts'] = Save.objects.filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        object.views += 1
        object.save()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
         
        if 'comment_delete' in request.POST:
            comment_id = request.POST['comment_delete']
            Comment.objects.get(id=comment_id).delete()

        if 'save_id' in request.POST:
            post = Post.objects.get(id=request.POST.get('save_id'))
            saved = Save.objects.filter(post=post, user=user).count()
            if not saved:
                Save.objects.create(post=post, user=user)
            else:
                Save.objects.filter(post=post, user=user).delete()

        if 'like_id' in request.POST:
            post = Post.objects.get(id=request.POST.get('like_id'))
            liked = Like.objects.filter(post=post, user=user).count()
            if not liked:
                Like.objects.create(post=post, user=user)
            else:
                Like.objects.filter(post=post, user=user).delete()
        
        if 'comment_button' in request.POST:
            comment = request.POST.get('comment') 
            if comment.strip() != '':
                user = request.user
                post = Post.objects.get(id=self.kwargs['pk'])  
                Comment.objects.create(user=user, post=post, body=comment)
        return redirect('detail_post_view', self.get_object().id)


        







def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('profileDetailPosts',f'{request.user}')
    

    
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.owner.username != request.user.username:
        raise Http404
    if 'update_post' in request.POST:
        post.title = request.POST['title']
        post.update_at = timezone.now()
        post.save()
        return redirect('detail_post_view', post.id)
    if 'tag_delete' in request.POST:
        tag_id = request.POST['tag_delete']
        post.update_at = timezone.now()
        post.save()
        post.post_tags.remove(Tag.objects.get(id=tag_id))



        
    if 'add_tag' in request.POST:
        tag  = request.POST['tag_name']
        post.update_at = timezone.now()
        post.save()
        if len(post.post_tags.all()) <8:
            if tag != '':
                if len(Tag.objects.filter(title=tag)) == 0:
                      tag = Tag.objects.create(title=tag)
                else:
                    tag = Tag.objects.get(title=tag)
                tag.post.add(post.id)


    return render(request, 'update_post.html', locals())
