from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, RedirectView, ListView
from django.views.generic.edit import BaseFormView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q




from apps.follower.forms import FollowerForm
from apps.follower.models import Follower
from apps.like.models import Like
from apps.post.views import PostListView
from apps.save.models import Save
from apps.user.utils import clean_username, transliterate
from apps.post.models import Post, PostImage, Tag
from apps.user.forms import UserRegistrationForm, UserModificationForm
from apps.user.models import CustomUser
from apps.post.forms import AddPostForm
from apps.user.utils import get_id_by_username
from apps.post.mixins import SearchMixin, LikeAndSaveMixin


#Тут я наследовался от CreateView чтобы создавать нового пользователя в базе данных
class RegisterUser(CreateView): 
    form_class = UserRegistrationForm
    template_name = 'user/sign-up.html'
    #Эта метод вызывается при успешной проверки формы регистрации, он сохраняет пользователя,
    #после чего сразу авторизует пользователя благодаря функции login, после перенаправляет на главную страницу
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


#Наследовался от LoginView чтобы взять функционал View для авторизации
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/sign-in.html'
    
    def get_success_url(self):
        return reverse_lazy('index')

@method_decorator(login_required, name='dispatch')
class LogoutUser(RedirectView):
    url = 'http://127.0.0.1:8000/login/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UpdateUser(FormView):
    form_class = UserModificationForm
    template_name = 'user/editprofile.html'

    #Тут я вручную написал обновление своего аккаунта

    def post(self, request, *args, **kwargs):  
        
        me = CustomUser.objects.get(username=request.user.username)
        form = self.get_form()
        if clean_username(request):
            me.username = request.POST['username']
        else:
            return self.form_invalid(form)
        if form.is_valid():
            if form.cleaned_data.get('avatar') :
                me.avatar = form.cleaned_data.get('avatar')
            if form.cleaned_data.get('first_name'):      
                me.first_name = form.cleaned_data.get('first_name')
            if form.cleaned_data.get('last_name'):              
                me.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('bio'):              
                me.bio = form.cleaned_data.get('bio')
            me.save()
            return redirect('index')
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):

        class NUserModificationForm(self.form_class):   
            if request.user.first_name is not None:
                first_name = forms.CharField(widget=forms.TextInput(attrs={'value':f'{request.user.first_name}'}))
            if request.user.last_name is not None:
                last_name = forms.CharField(widget=forms.TextInput(attrs={'value':f'{request.user.last_name}'}))
            if request.user.bio is not None:
                bio = forms.CharField(widget=forms.TextInput(attrs={'value':f'{request.user.bio}'}))

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

        self.form_class = NUserModificationForm 
        form = self.form_class(instance=request.user)
        return self.render_to_response(self.get_context_data())










@method_decorator(login_required, name='dispatch')
class ProfileDetailView(SearchMixin , DetailView, BaseFormView):
    # slug_url_kwarg эта переменная которую вводим в маршрутизаторе
    # slug_field это поле самой модели
    model = CustomUser
    context_object_name = 'user'
    template_name = 'user/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    form_class = FollowerForm
    
    
    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['title'] = self.request.user.username   
        if Follower.objects.filter(from_user = self.request.user.id, to_user = self.get_object().id):
            context['follow_status'] = 'followed'
        else:
            context['follow_status'] = 'unfollowed'

        return context  
    
    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            profile = self.get_object()
            profile.views += 1
            profile.save()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.get_object().id != self.request.user.id:
            f = Follower.objects.filter(from_user = self.request.user.id, to_user = self.get_object().id)
            if not f:
                Follower.objects.create(from_user=self.request.user, to_user=self.get_object())
            else:
                f.delete()
        return super().get(self.request, self.args, self.kwargs)

        
@login_required
def addPost(request):
    context = {
        'form_post' : AddPostForm,
        
    }
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


    if request.method == 'POST':
        images = request.FILES.getlist('image')
        data = request.POST
        post_id = Post.objects.create(title=data['title'], owner=request.user, update_at=timezone.now(), slug=transliterate(data['title']))
        for image in  images:
            PostImage.objects.create(post=Post.objects.all()[0], image=image)


        if request.POST['tag'] != '':
            tags = [i.split()[0] for i in request.POST['tag'].split('#') if i != '']
            for i in tags[:8]:
                if len(Tag.objects.filter(title=i)) == 0:
                    tag = Tag.objects.create(title=i)
                else:
                    tag = Tag.objects.get(title=i)
                tag.post.add(post_id.id)
                
            

        return redirect('profile', request.user)
    return render(request,'add_publication.html', context=context)













@method_decorator(login_required, name='dispatch')
class ProfilePostsView(PostListView):

    def get_queryset(self):
        user = get_id_by_username(self.kwargs['username'])
        return super().get_queryset().filter(owner=user)

    def get_context_data(self, **kwargs):
        user = CustomUser.objects.get(username=self.kwargs['username'])
        context = super().get_context_data(**kwargs)
        context['title'] = f'Profile {user}'
        context['posts'] = Post.objects.filter(owner=user)
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
        return redirect('profileDetailPosts', self.kwargs['username'])




def page_not_found(request, exception):
    return render(request, 'page_not_found/p404.html', status=404)