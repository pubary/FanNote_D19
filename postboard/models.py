from django.db import models
from django.urls import reverse
from transliterate import slugify

from users.models import FunUser


class Category(models.Model):
    cat_name = models.CharField(max_length=63, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=63, null=False, verbose_name='URL',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['cat_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.cat_name}'


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время написания')
    author = models.ForeignKey(FunUser, on_delete=models.CASCADE, verbose_name='Автор',)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    # time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    # video = models.ImageField(upload_to='video/%Y/%m/%d/', blank=True, verbose_name='Видео')

    def __str__(self):
        return f'{self.title.title()[:30]}\n{self.category}\n{self.text[:60]}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-time']


class Feedback(models.Model):
    text = models.TextField(verbose_name='Текст отклика')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время написания')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='К объявлению')
    author = models.ForeignKey(FunUser, on_delete=models.CASCADE, verbose_name='Автор')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано',)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-time']

    def __str__(self):
        return f'{self.text[:30]}'

