from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from fannote.settings import MY_MAIL
from postboard.models import Post
from .models import FunUser


@shared_task
def news_mail():
    last_week = datetime.now(timezone.utc) - timedelta(days=7)
    posts = Post.objects.filter(time__gt=last_week).values('id').exists()
    if posts:
        msg_data = {}
        msg_data['last_week'] = last_week
        users = FunUser.objects.all()
        t = 17
        for user in users:
            if user.email:
                msg_data['name'] = user.username
                msg_data['email'] = user.email
                print(f'{t} Создание еженедельника для: {msg_data["email"]}')
                send_news_mail.apply_async([msg_data], countdown=t)
                t += 17


@shared_task
def send_news_mail(msg_data):
    last_week = msg_data['last_week']
    posts = Post.objects.filter(time__gt=last_week).values('pk', 'title', 'time')
    msg_data['posts'] = posts
    html_content = render_to_string(
        'users/news_mail.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Объявления за неделю',
        body=f'Новые объявления на нашем сайте',
        from_email=MY_MAIL,
        to=[msg_data['email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f" Отправка еженедельника на {msg_data['email']}")
    msg.send()

