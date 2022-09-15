from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, CategorySubscribers
from django.contrib import messages
from django.template.loader import render_to_string
from .tasks import email_task
from django.db import models


class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'AT'
        return super().form_valid(form)


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'NS'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'AT'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'NS'
        return super().form_valid(form)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Category
    template_name = 'cats.html'
    context_object_name = 'cats'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
        category_id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Категория)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context


@login_required
def add_subscribe(request, *args, **kwargs):
    # получаем первичный ключ выбранной категории
    pkr = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:',Category.objects.get(pk=pk) )
    # добавляем в выбранную категорию, в поле "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(id=pk).subscribers.add(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/posts/cats')


# функция-представление обернутая в декоратор
# для удаления пользователя из списка подписчиков
@login_required
def del_subscribe(request, **kwargs):
    # получаем первичный ключ выбранной категории
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    # удаляем в выбранной категории, из поля "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/posts/cats')


def sending_emails_to_subscribers(instance):
    sub_text = instance.post_text
    sub_title = instance.post_title
    # получаем нужный объект модели Категория через рк Пост
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category_post.pk)
    # получаем список подписчиков категории
    subscribers = category.subscribers.all()

    # проходимся по всем подписчикам в списке
    for subscriber in subscribers:
        # создание переменных, которые необходимы для таски
        subscriber_username = subscriber.username
        subscriber_useremail = subscriber.email
        html_content = render_to_string('news/mail.html',
                                        {'user': subscriber,
                                         'title': sub_title,
                                         'text': sub_text[:50],
                                         'post': instance})
        # функция для таски, передаем в нее все что нужно для отправки подписчикам письма
        email_task(subscriber_username, subscriber_useremail, html_content)
    return redirect('/posts/')
