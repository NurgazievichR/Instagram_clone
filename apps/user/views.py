from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from apps.user.forms import UserRegistrationForm, UserModificationForm
from apps.user.models import CustomUser


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


class LogoutUser(RedirectView):
    url = 'http://127.0.0.1:8000/login/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class UpdateUser(FormView):
    form_class = UserModificationForm
    template_name = 'user/editprofile.html'

    #Тут я вручную написал обновление своего аккаунта
    # def form_valid(self, form):
    #     me = CustomUser.objects.get(username=self.request.user.username)
    #     me.username = form.data['username']
    #     me.first_name = form.data['first_name'] 
    #     me.last_name = form.data['last_name']
    #     me.bio = form.data['bio']
    #     if form.files['avatar']:
    #         me.avatar = form.files['avatar']
    #     me.save()
    #     return redirect('index')
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        me = CustomUser.objects.get(username=request.user.username)
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data.get('avatar'):
                me.avatar = form.cleaned_data.get('avatar')
            if form.cleaned_data.get('first_name'):      
                me.first_name = form.cleaned_data.get('first_name')
            if form.cleaned_data.get('last_name'):              
                me.last_name = form.cleaned_data.get('last_name')
            me.username = form.cleaned_data.get('username')
            if form.cleaned_data.get('bio'):              
                me.bio = form.cleaned_data.get('bio')
            me.save()
            return redirect('index')
        else:
            return self.form_invalid(form)



    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return self.render_to_response(self.get_context_data())


class ProfileDetailView(DetailView):
    # slug_url_kwarg эта переменная которую вводим в маршрутизаторе
    # slug_field это поле самой модели
    model = CustomUser
    context_object_name = 'user'
    template_name = 'user/profile.html'
    slug_url_kwarg = 'username'
    slug_field= 'username'


# def timer(num : int):
#     print(num)
#     if not num == 0:
#         return(timer(num - 1))




