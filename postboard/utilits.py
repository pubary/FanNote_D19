from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from fannote.settings import MY_MAIL
from postboard.models import Feedback


def send_feedback(request, post):
    text = request.POST['feedback']
    user = request.user
    feedback = Feedback(text=text, post=post, author=user, is_active=False)
    feedback.save()
    try:
        notify_mail(user=user, feedback=feedback)
    except:
        print(f'Ошибка отправки email пользователю {user.username} о новом отклике на его объявление')


def notify_mail(*args, **kwargs):
    user = kwargs['user']
    feedback = kwargs['feedback']
    email = user.email
    html_content = render_to_string(
        'users/notify_mail.html',
        {
            'name': user.username,
            'feedback': feedback,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новом отклике',
        body=f'На Ваше объявление  поступил новый отклик',
        from_email=MY_MAIL,
        to=[email, ],
    )
    msg.attach_alternative(html_content, "text/html")
    # print(f" Отправка сообщения о новом отклике пользователю {user.username}")
    msg.send()

