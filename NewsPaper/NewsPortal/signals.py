from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Category, Post, CategorySubscribers
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=Post.category_post.through)
def categories_changed(sender, instance, action, pk_set, **kwargs):
    if action == "article_create":
        email_list = []
        # Подписчики на разделы, к которым относится статья
        subscribers = CategorySubscribers.objects.filter(category_id__in=pk_set).values('user_id').distinct()
        for i in subscribers:
            email_list.append(User.objects.get(id=i['user_id']).email)
        subject = f'{instance.title} {instance.time_in.strftime("%d %m %Y")}'
        html_content = render_to_string(
            'mail_to_subscriber.html',
            {
                'post_title': instance.title,
                'post_text': instance.text,
                'username': 'подписчик',
                'post_id': instance.pk
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='ogr.nick@yandex.ru',
            to=email_list,
        )
        msg.attach_alternative(html_content, "post_text/html")  # добавляем html
        msg.send()  # отсылаем


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_subscribers_post(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.post_title} {instance.time_in.strftime("%d %m %Y")}'
    else:
        subject = f'Post changed for {instance.post_title} {instance.time_in.strftime("%d %m %Y")}'
