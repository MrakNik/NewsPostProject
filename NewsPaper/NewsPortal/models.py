from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Author(models.Model):
    """Модель, содержащая объекты всех авторов"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
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
        return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Category(models.Model):
    """Категории новостей/статей - темы, которые они отражают (спорт, политика, образование и т.д.).
    Имеет единственное поле: название категории. Поле должно быть уникальным"""
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class PostCategory(models.Model):
    """Промежуточная модель для связи <многие ко многим>"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Под каждой новостью/статьёй можно оставлять комментарии,
    поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in_comm = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self, comment_rating=1):
        self.comment_rating = comment_rating
        self.comment_rating += 1
        self.save()

    def dislike(self, comment_rating=1):
        self.comment_rating = comment_rating
        self.comment_rating -= 1
        self.save()
