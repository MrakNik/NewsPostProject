from django.contrib import admin

from .models import Author, Category, Post, PostCategory, Comment, CategorySubscribers


def like_plus_five(modeladmin, request, queryset):
    # функция накрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating + 5
        posts.save()


def like_minus_five(modeladmin, request, queryset):
    # функция  скрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating - 5
        posts.save()


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('id', 'post_title', 'position', 'who_author', 'post_rating',)
    list_filter = ('category_post', 'who_author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('post_title',)  # тут всё очень похоже на фильтры из запросов в базу
    actions = [like_plus_five, like_minus_five]  # добавляем действия в список


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


class CategorySubscribersAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user')


# Register your models here.
admin.site.register(CategorySubscribers, CategorySubscribersAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
