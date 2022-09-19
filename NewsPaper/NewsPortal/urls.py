from django.urls import path
from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostList, PostDetail, NewsCreate, ArticleCreate, ArticleUpdate, NewsUpdate, ArticleDelete, \
   NewsDelete, CategoryList, add_subscribe, del_subscribe, CategoryDetail

urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('cats/', cache_page(60)(CategoryList.as_view()), name='cats'),

   path('category/<int:pk>', cache_page(60 * 5)(CategoryDetail.as_view()), name='category_detail'),

   # Функция-представление для подписки на выбранную категорию
    path('category/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    # Функция-представление для отписки от выбранной категории
    path('category/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]
