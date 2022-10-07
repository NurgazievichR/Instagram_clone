from django.views import View
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse


from apps.like.models import Like
from apps.post.models import Post, Tag
from apps.save.models import Save

from apps.user.models import CustomUser

class SearchMixin(View):
    def get(self, request, *args, **kwargs):
        if 'search-button' in request.GET:
            finding_word = request.GET.get('search_word').split()[0]
            if finding_word[0]=='#':
                tags = Tag.objects.filter(Q(title__startswith=finding_word[1:]))
                print(tags)
                return render(request, 'users_list.html', {'tags':tags, 'title':'Hashtags'})
            else:
                if finding_word != '':
                        accounts = CustomUser.objects.filter(Q(username__icontains=finding_word) | Q(first_name__startswith=finding_word) | Q(last_name__startswith=finding_word)   )
                return render(request, 'users_list.html', locals())
        return super().get(request, *args, **kwargs)









class LikeAndSaveMixin(View):
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
        return HttpResponseRedirect(reverse('index'))