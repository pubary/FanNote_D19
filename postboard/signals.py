from django.db.models.signals import post_save
from django.dispatch import receiver

from postboard.models import Feedback
from users.utilits import accept_mail


@receiver(post_save, sender=Feedback)
def after_creation_feedback(sender, instance, **kwargs):
    user = instance.post.author
    try:
        accept_mail(user, instance)
    except:
        print(f'Ошибка отправки email пользователю {user} об оставлении отклика на его объявление')
