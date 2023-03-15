import secrets
import string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from fannote.settings import MY_MAIL


def confirm_code():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password


def confirm_mail(user):
    email = user.email
    html_content = render_to_string(
        'users/confirm_mail.html',
        {
            'name': user.username,
            'code': user.code,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Подтверждение регистрации',
        body=f'Код для активации вашей учетной записи',
        from_email=MY_MAIL,
        to=[email, ],
    )
    msg.attach_alternative(html_content, "text/html")
    # print(f" Отправка кода для подтверждения регистрации пользователя {user.username}")
    msg.send()


def accept_mail(user, feedback):
    email = user.email
    html_content = render_to_string(
        'users/accept_mail.html',
        {
            'name': user.username,
            'feedback': feedback,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Отклик принят',
        body=f'Ваш отклик на объявление принят',
        from_email=MY_MAIL,
        to=[email, ],
    )
    msg.attach_alternative(html_content, "text/html")
    # print(f" Отправка сообщения о принятии отклика пользователя {user.username}")
    msg.send()

