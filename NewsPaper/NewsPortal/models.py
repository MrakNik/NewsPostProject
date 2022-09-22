from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

from django.urls import reverse
from django.utils import timezone


class Author(models.Model):
    """Модель, содержащая объекты всех авторов"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        objects = models.Manager()
        self.user_rating = 0
        for post in Post.objects.filter(who_author__user=self.user):
            self.user_rating += post.post_rating * 3
            for comment in Comment.objects.filter(post=post):
                self.user_rating += comment.comment_rating
        for comment in Comment.objects.filter(user=self.user):
            self.user_rating += comment.comment_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Post(models.Model):
    """ Эта модель должна содержать в себе статьи и новости, которе создают пользователи.
    Каждый объект может иметь одну или несколько категорий."""
    article = 'AT'
    news = 'NS'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    who_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=article)
    time_in = models.DateTimeField(default=timezone.now)
    category_post = models.ManyToManyField('Category', through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    # Внутренний класс (Мета класс), который используется для определения модели.
    class Meta:
        # Настройка отображения имени модели в админ панели (ед число)
        verbose_name = 'Публикация'
        # Настройка отображения имени модели в админ панели (множ число)
        verbose_name_plural = 'Публикации'

    def like(self, post_rating=1):
        self.post_rating = post_rating
        self.post_rating += 1
        self.save()

    def dislike(self, post_rating=1):
        self.post_rating = post_rating
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:125]}...'

    def __str__(self):
        return f'{self.post_title}: {self.post_text[:10]}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwaegs):
        super().save(*args, **kwaegs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Category(models.Model):
    """Категории новостей/статей - темы, которые они отражают (спорт, политика, образование и т.д.).
    Имеет единственное поле: название категории. Поле должно быть уникальным"""
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    # Внутренний класс (Мета класс), который используется для определения модели.
    class Meta:
        # Настройка отображения имени модели в админ панели (ед число)
        verbose_name = 'Категория'
        # Настройка отображения имени модели в админ панели (множ число)
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.category_name}'


class CategorySubscribers(models.Model):
    # subscriber = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("category", "user")

    def __str__(self):
        return f'{self.user.username}: {self.category.category_name}'


class PostCategory(models.Model):
    """Промежуточная модель для связи <многие ко многим>"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.post_title}: {self.category.category_name}'


class Comment(models.Model):
    """Под каждой новостью/статьёй можно оставлять комментарии,
    поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in_comm = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    # Внутренний класс (Мета класс), который используется для определения модели.
    class Meta:
        # Настройка отображения имени модели в админ панели (ед число)
        verbose_name = 'Комментарий'
        # Настройка отображения имени модели в админ панели (множ число)
        verbose_name_plural = 'Комментарии'

    def like(self, comment_rating=1):
        self.comment_rating = comment_rating
        self.comment_rating += 1
        self.save()

    def dislike(self, comment_rating=1):
        self.comment_rating = comment_rating
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.username}: {self.post.post_title}'
