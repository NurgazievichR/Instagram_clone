import time
from celery import shared_task
from django.core.mail import send_mail
from apps.user.models import Activity, CustomUser
from django.utils import timezone

from instagramClone.celery import app
from apps.post.models import Post, Tag
from apps.story.models import Story


@shared_task
def send_email_task(email):
    send_mail('Celery Task!', 'Ramazan is the smartest', 'zalalidinovroma@gmail.com',[email],fail_silently=False)
    send_mail('Жалоба',  )

@app.task
def complaint(id, request_user):
    post = Post.objects.get(id=id)
    owner = post.owner
    admins = CustomUser.objects.filter(is_staff=True)
    print('yes')
    for i in admins:
        send_mail('Жалоба', f'Пришла жалоба от пользователя {request_user}, на пост с id={id}, владелец которого {owner}\nhttp://localhost:8000/post_detail_view/{id}/', 'zalalidinovroma@gmail.com', recipient_list=[f'{i.email}'])
        print(f'Отправлено пользователю {i.email}')


@shared_task()
def checkTag():
    tags = Tag.objects.all()
    for tag in tags:
        if len(tag.post.all()) == 0:
            tag.delete()

@app.task()
def delete_story(id_story):
    print(id_story)
    time.sleep(600)
    story = Story.objects.get(id=id_story)
    story.delete()



@shared_task()
def create_activity():
    last = Activity.objects.last()
    ids = Activity.objects.all().last().pk
    last_ = Activity.objects.filter(id=ids)
    if last.date != timezone.now().date():
        Activity.objects.create(today=0, all_time=last_[0].all_time, date=timezone.now().date())